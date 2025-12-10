import sys
import subprocess
import argparse

import os
import shutil
import tempfile

import re
from datetime import datetime, timezone
import json

import time
import threading

from http.server import HTTPServer, SimpleHTTPRequestHandler

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from jinja2 import Environment, FileSystemLoader
from markdown import Markdown
import yaml
import xml.etree.ElementTree as ET

from feedgen.feed import FeedGenerator

from colorama import Fore, Style, init

init()

SITE_DIR = "site"
BUILD_DIR = "build"
BUILD_DEV_DIR = "build-dev"
TEMPLATES_DIR = os.path.join(SITE_DIR, "templates")
BLOG_DIR = os.path.join(SITE_DIR, "blog")

BLOG_INDEX_TEMPLATE = "blog_index.html"
BLOG_POST_TEMPLATE = "blog_post.html"
DEFAULT_TEMPLATE = "base.html"

SITE_URL = "https://gijs6.nl"
SITE_TITLE = "Gijs6"
SITE_DESCRIPTION = "A big mess of fun pages, interesting projects, my own thoughts and opinions and more."
AUTHOR_NAME = "Gijs6"
AUTHOR_EMAIL = "me@gijs6.nl"

FRONT_MATTER_PATTERN = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def parse_front_matter(content):
    match = FRONT_MATTER_PATTERN.match(content)
    if match:
        return yaml.safe_load(match.group(1)) or {}, content.split("---", 2)[2].strip()
    return {}, content


def warn(message):
    print(f"{Fore.YELLOW}WARNING: {message}{Style.RESET_ALL}")


def get_git_commit_info():
    try:
        output = subprocess.check_output(
            ["git", "log", "-1", "--format=%h %H %ct"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if output:
            parts = output.split()
            if len(parts) == 3:
                short_hash = parts[0]
                long_hash = parts[1]
                commit_ts = int(parts[2])
                commit_dt = datetime.fromtimestamp(commit_ts, tz=timezone.utc)
                return {
                    "hash": {"short": short_hash, "long": long_hash},
                    "dt": {
                        "date": {
                            "long": commit_dt.strftime("%B %d, %Y"),
                            "short": commit_dt.strftime("%Y-%m-%d"),
                        },
                        "time": commit_dt.strftime("%H:%M:%S"),
                        "iso": commit_dt.isoformat(),
                    },
                }
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        pass
    return None


def get_data():
    now = datetime.now(timezone.utc)
    return {
        "last_commit": get_git_commit_info(),
        "now": {
            "date": {
                "long": now.strftime("%B %d, %Y"),
                "short": now.strftime("%Y-%m-%d"),
            },
            "time": now.strftime("%H:%M:%S"),
            "iso": now.isoformat(),
        },
    }


def infer_page_metadata(rel_path):
    # For index.html, canonical path is "/" not "/index"
    if rel_path == "index.html":
        canonical_path = "/"
    else:
        canonical_path = "/" + os.path.splitext(rel_path)[0]

    # Active page is derived from the first path component or filename
    active_page = rel_path.split("/")[0].replace(".html", "").replace(".md", "")

    # Map "index" to "home" for navigation purposes
    if active_page == "index":
        active_page = "home"

    return active_page, canonical_path


def process_blog(build_dir, template_env, md_processor, data):
    posts = []
    blog_slugs = set()

    if not os.path.exists(BLOG_DIR):
        return posts

    for filename in os.listdir(BLOG_DIR):
        if not filename.endswith(".md"):
            continue

        slug = filename.replace(".md", "")
        if slug in blog_slugs:
            warn(f"Duplicate blog slug: {slug}")
        blog_slugs.add(slug)

        filepath = os.path.join(BLOG_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        metadata, markdown_content = parse_front_matter(content)
        html_content = md_processor.convert(markdown_content)
        md_processor.reset()

        date_str = metadata.get("date")
        if date_str:
            if isinstance(date_str, str):
                created_date = datetime.strptime(date_str, "%Y-%m-%d").replace(
                    tzinfo=timezone.utc
                )
            else:
                created_date = datetime.combine(date_str, datetime.min.time()).replace(
                    tzinfo=timezone.utc
                )
        else:
            try:
                output = subprocess.check_output(
                    ["git", "log", "--follow", "--format=%H %ct", "--", filepath],
                    text=True,
                    stderr=subprocess.DEVNULL,
                ).strip()
                if output:
                    first_commit_ts = int(output.split("\n")[-1].split()[1])
                    created_date = datetime.fromtimestamp(
                        first_commit_ts, tz=timezone.utc
                    )
                else:
                    created_date = None
                    warn(f"No date found for blog post: {filename}")
            except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
                created_date = None
                warn(f"No date found for blog post: {filename}")

        post = {
            "title": metadata.get("title", slug.replace("-", " ").title()),
            "slug": slug,
            "content": html_content,
            "filepath": filepath,
            "created": created_date,
        }

        if created_date:
            post["date"] = created_date.strftime("%Y-%m-%d")
            post["date_iso"] = created_date.isoformat()

        posts.append(post)

    posts.sort(
        key=lambda p: p.get("created") or datetime.min.replace(tzinfo=timezone.utc),
        reverse=True,
    )

    # Derive blog section name from BLOG_DIR (e.g., "site/blog" -> "blog")
    blog_section = os.path.basename(BLOG_DIR)
    blog_dir = os.path.join(build_dir, blog_section)
    os.makedirs(blog_dir, exist_ok=True)

    with open(os.path.join(blog_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(
            template_env.get_template(BLOG_INDEX_TEMPLATE).render(
                posts=posts,
                active_page=blog_section,
                canonical_path=f"/{blog_section}/",
                data=data,
            )
        )

    for post in posts:
        post_path = os.path.join(blog_dir, f"{post['slug']}.html")
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(
                template_env.get_template(BLOG_POST_TEMPLATE).render(
                    post=post,
                    active_page=blog_section,
                    canonical_path=f"/{blog_section}/{post['slug']}",
                    data=data,
                )
            )

    fg = FeedGenerator()
    fg.title(f"{SITE_TITLE} - {blog_section}")
    fg.description(SITE_DESCRIPTION)
    fg.id(SITE_URL)
    fg.link(href=f"{SITE_URL}/{blog_section}", rel="alternate")
    fg.language("en")
    fg.author(name=AUTHOR_NAME, email=AUTHOR_EMAIL, uri=SITE_URL)

    for post in posts:
        fe = fg.add_entry()
        fe.title(post["title"])
        fe.link(href=f"{SITE_URL}/{blog_section}/{post['slug']}")
        fe.id(f"{SITE_URL}/{blog_section}/{post['slug']}")
        fe.description(post["content"])
        if post.get("created"):
            fe.pubDate(post["created"])
            fe.updated(post["created"])

    with open(os.path.join(blog_dir, "rss.xml"), "wb") as f:
        f.write(fg.rss_str(pretty=True))
    with open(os.path.join(blog_dir, "atom.xml"), "wb") as f:
        f.write(fg.atom_str(pretty=True))

    json_feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": f"{SITE_TITLE} - {blog_section}",
        "home_page_url": f"{SITE_URL}/",
        "feed_url": f"{SITE_URL}/{blog_section}/feed.json",
        "description": SITE_DESCRIPTION,
        "author": {"name": AUTHOR_NAME, "url": SITE_URL},
        "items": [
            {
                "id": f"{SITE_URL}/{blog_section}/{post['slug']}",
                "url": f"{SITE_URL}/{blog_section}/{post['slug']}",
                "title": post["title"],
                "content_html": post["content"],
                "date_published": post.get("date_iso"),
            }
            for post in posts
            if post.get("date_iso")
        ],
    }

    with open(os.path.join(blog_dir, "feed.json"), "w", encoding="utf-8") as f:
        json.dump(json_feed, f, indent=4, ensure_ascii=False)

    return posts


def process_site_files(build_dir, template_env, md_processor, data):
    seen_outputs = {}

    for root, dirs, files in os.walk(SITE_DIR):
        dirs[:] = [
            d for d in dirs if os.path.join(root, d) not in [TEMPLATES_DIR, BLOG_DIR]
        ]

        for filename in files:
            filepath = os.path.join(root, filename)

            if filepath.startswith(TEMPLATES_DIR) or filepath.startswith(BLOG_DIR):
                continue
            if filename.startswith("."):
                continue

            rel_path = os.path.relpath(filepath, SITE_DIR)
            if rel_path.endswith(".md"):
                output_path = os.path.join(build_dir, rel_path[:-3] + ".html")
            else:
                output_path = os.path.join(build_dir, rel_path)

            if output_path in seen_outputs:
                warn(
                    f"Duplicate output: {output_path} (from {filepath} and {seen_outputs[output_path]})"
                )
            seen_outputs[output_path] = filepath

            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            if filepath.endswith(".md"):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                metadata, markdown_content = parse_front_matter(content)
                html_content = md_processor.convert(markdown_content)
                md_processor.reset()

                template_name = metadata.get("template")
                if not template_name:
                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(html_content)
                    continue

                try:
                    active_page, canonical_path = infer_page_metadata(rel_path)

                    page_data = {"content": html_content}
                    page_data.update(metadata)
                    if "active_page" not in page_data:
                        page_data["active_page"] = active_page
                    if "canonical_path" not in page_data:
                        page_data["canonical_path"] = canonical_path

                    template = template_env.get_template(template_name)
                    rendered = template.render(page=page_data, data=data)

                    with open(output_path, "w", encoding="utf-8") as f:
                        f.write(rendered)
                except Exception as e:
                    warn(f"Failed to render {filepath}: {e}")

            elif filepath.endswith(".html"):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                metadata, html_content = parse_front_matter(content)

                if metadata:
                    template_name = metadata.get("template", DEFAULT_TEMPLATE)
                    try:
                        active_page, canonical_path = infer_page_metadata(rel_path)

                        page_data = {"content": html_content}
                        page_data.update(metadata)
                        if "active_page" not in page_data:
                            page_data["active_page"] = active_page
                        if "canonical_path" not in page_data:
                            page_data["canonical_path"] = canonical_path

                        template = template_env.get_template(template_name)
                        rendered = template.render(page=page_data, data=data)
                    except Exception as e:
                        warn(f"Failed to render {filepath}: {e}")
                        continue
                else:
                    try:
                        active_page, canonical_path = infer_page_metadata(rel_path)
                        template = template_env.from_string(content)
                        rendered = template.render(
                            active_page=active_page,
                            canonical_path=canonical_path,
                            data=data,
                        )
                    except Exception as e:
                        warn(f"Failed to render {filepath}: {e}")
                        continue

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(rendered)

            else:
                shutil.copy2(filepath, output_path)


def generate_sitemap(build_dir, posts):
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    blog_section = os.path.basename(BLOG_DIR)

    def add_url(loc, lastmod=None):
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = loc
        if lastmod:
            ET.SubElement(url, "lastmod").text = lastmod

    add_url(f"{SITE_URL}/")
    if posts:
        add_url(f"{SITE_URL}/{blog_section}/")

    for post in posts:
        lastmod = post["created"].strftime("%Y-%m-%d") if post.get("created") else None
        add_url(f"{SITE_URL}/{blog_section}/{post['slug']}", lastmod=lastmod)

    for root, _, files in os.walk(build_dir):
        for filename in files:
            if not filename.endswith(".html"):
                continue
            if filename in ["404.html", "index.html"]:
                continue

            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, build_dir)

            if rel_path.startswith(blog_section):
                continue

            url_path = "/" + rel_path.replace("\\", "/").replace(".html", "")
            add_url(f"{SITE_URL}{url_path}")

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="    ")
    tree.write(
        os.path.join(build_dir, "sitemap.xml"),
        encoding="utf-8",
        xml_declaration=True,
    )


class BuildHandler(FileSystemEventHandler):
    def __init__(self, build_func):
        self.build_func = build_func
        self.last_build = 0

    def on_modified(self, event):
        if event.is_directory or "build" in event.src_path:
            return
        now = time.time()
        if now - self.last_build < 1:
            return
        self.last_build = now

        if os.path.basename(event.src_path) == "engine.py":
            print(
                f"\n{Fore.YELLOW}Build script changed! Restarting...{Style.RESET_ALL}\n"
            )
            os.execv(sys.executable, [sys.executable] + sys.argv)

        rel_path = os.path.relpath(event.src_path)
        timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
        print(
            f"\n{Fore.BLUE}[{timestamp}]{Style.RESET_ALL} {Fore.YELLOW}File changed:{Style.RESET_ALL} {rel_path}\n"
        )
        self.build_func()


class BuildHTTPServer(SimpleHTTPRequestHandler):
    directory = BUILD_DIR

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=self.directory, **kwargs)

    def log_message(self, format, *args):
        request_line = args[0]
        parts = request_line.split()

        if len(parts) >= 2:
            method = parts[0]
            path = parts[1]
        else:
            method = ""
            path = request_line

        if method == "GET":
            method_color = Fore.CYAN
        elif method == "POST":
            method_color = Fore.YELLOW
        elif method == "PUT":
            method_color = Fore.MAGENTA
        elif method == "DELETE":
            method_color = Fore.RED
        else:
            method_color = Fore.WHITE

        status = args[1] if len(args) > 1 else "000"
        if status.startswith("2"):
            status_color = Fore.GREEN
        elif status.startswith("3"):
            status_color = Fore.CYAN
        elif status.startswith("4"):
            status_color = Fore.YELLOW
        else:
            status_color = Fore.RED

        timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
        print(
            f"{Fore.BLUE}[{timestamp}]{Style.RESET_ALL}  {method_color}{Style.BRIGHT}{method}{Style.RESET_ALL}  {Fore.WHITE}{path}{Style.RESET_ALL}  {status_color}{status}{Style.RESET_ALL}"
        )

    def do_GET(self):
        path = self.translate_path(self.path)

        if self.path.endswith("/") or self.path == "":
            index_path = os.path.join(path, "index.html")
            if os.path.isfile(index_path):
                self.path = (
                    self.path.rstrip("/") + "/index.html"
                    if not self.path.endswith("index.html")
                    else self.path
                )
                return super().do_GET()

        if os.path.isfile(path):
            return super().do_GET()

        if not self.path.endswith("/") and "." not in os.path.basename(self.path):
            html_path = path + ".html"
            if os.path.isfile(html_path):
                self.path += ".html"
                return super().do_GET()

        not_found_path = os.path.join(self.directory, "404.html")
        if os.path.isfile(not_found_path):
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(not_found_path, "rb") as f:
                self.wfile.write(f.read())
            return

        self.send_error(404, "File not found")


def build(output_dir=None):
    if output_dir is None:
        output_dir = BUILD_DIR

    start_time = time.time()
    print(f"{Fore.CYAN}=> Building site <={Style.RESET_ALL}")

    print("> Setting up environment... ", end="", flush=True)
    setup_start = time.time()
    temp_build_dir = tempfile.mkdtemp()
    template_env = Environment(loader=FileSystemLoader([SITE_DIR, TEMPLATES_DIR]))
    md_processor = Markdown(extensions=["meta", "tables", "fenced_code"])
    data = get_data()
    setup_time = time.time() - setup_start
    print(f"{Fore.GREEN}done ({setup_time * 1000:.0f}ms){Style.RESET_ALL}")

    print("> Processing blog posts... ", end="", flush=True)
    blog_start = time.time()
    posts = process_blog(temp_build_dir, template_env, md_processor, data)
    blog_time = time.time() - blog_start
    print(f"{Fore.GREEN}{len(posts)} posts ({blog_time * 1000:.0f}ms){Style.RESET_ALL}")

    print("> Processing site files... ", end="", flush=True)
    files_start = time.time()
    process_site_files(temp_build_dir, template_env, md_processor, data)
    files_time = time.time() - files_start
    print(f"{Fore.GREEN}done ({files_time * 1000:.0f}ms){Style.RESET_ALL}")

    print("> Generating sitemap... ", end="", flush=True)
    sitemap_start = time.time()
    generate_sitemap(temp_build_dir, posts)
    sitemap_time = time.time() - sitemap_start
    print(f"{Fore.GREEN}done ({sitemap_time * 1000:.0f}ms){Style.RESET_ALL}")

    print("> Finalizing build... ", end="", flush=True)
    finalize_start = time.time()
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    shutil.move(temp_build_dir, output_dir)
    finalize_time = time.time() - finalize_start
    print(f"{Fore.GREEN}done ({finalize_time * 1000:.0f}ms){Style.RESET_ALL}")

    total_time = time.time() - start_time
    print(
        f"{Fore.GREEN}Build complete in {total_time * 1000:.0f}ms!{Style.RESET_ALL}\n"
    )


def serve(port=8000):
    print(f"{Fore.BLUE}=== Development Server ==={Style.RESET_ALL}\n")

    build(output_dir=BUILD_DEV_DIR)

    observer = Observer()
    handler = BuildHandler(lambda: build(output_dir=BUILD_DEV_DIR))
    observer.schedule(handler, SITE_DIR, recursive=True)
    observer.schedule(handler, ".", recursive=False)
    observer.start()

    class DevHTTPServer(BuildHTTPServer):
        directory = BUILD_DEV_DIR

    server = HTTPServer(("localhost", port), DevHTTPServer)
    threading.Thread(target=server.serve_forever, daemon=True).start()

    print(
        f"{Fore.GREEN}Server running at {Style.BRIGHT}http://localhost:{port}{Style.RESET_ALL}"
    )
    print(f"{Fore.CYAN}Serving from: {Style.BRIGHT}{BUILD_DEV_DIR}/{Style.RESET_ALL}")
    print(
        f"{Fore.MAGENTA}Watching: {Style.BRIGHT}{SITE_DIR}/{Style.RESET_ALL} and engine.py"
    )
    print(f"\n{Fore.YELLOW}Press Ctrl+C to stop{Style.RESET_ALL}\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}Stopping server...{Style.RESET_ALL}")
        observer.stop()
        server.shutdown()
        observer.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build static site for gijs6.nl")
    parser.add_argument(
        "command",
        nargs="?",
        default="build",
        choices=["build", "serve"],
        help="Command to run (default: build)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for server (default: 8000)",
    )

    args = parser.parse_args()

    if args.command == "serve":
        serve(args.port)
    else:
        build()

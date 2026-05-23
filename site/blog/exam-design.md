---
title: The new Dutch exam design is worse
date: 2026-05-24
---

<style>
    figure {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: var(--spacing-md);
        margin: 0;
        justify-content: space-between
    }

    figure img {
        max-width: 340px;
        width: 100%;
        flex: 1 1 260px
    }

    figure:has(img:only-child) img {
        max-width: 100%
    }

    figcaption {
        flex-basis: 100%;
        font-style: italic
    }
</style>

The Dutch national exams are getting redesigned. The Board for Tests and Examinations (<abbr title="College voor Toetsen en Examens" lang="nl">CvTE</abbr>) has been running pilots since <time datetime="2025">2025</time>, starting with the Spanish exam for <abbr title="hoger algemeen voortgezet onderwijs" lang="nl">havo</abbr>. This year even more exams use the new layout, including the English exam for <abbr title="voorbereidend wetenschappelijk onderwijs" lang="nl">vwo</abbr>, which I took this year.

The current design has been around since <time datetime="2007">2007</time>, so a refresh makes sense. The <span lang="nl">CvTE</span> says the main driver is new accessibility regulations. But having taken the new exam myself, I don't think it's an improvement at all.

For those unfamiliar with Dutch national exams: the design is pretty plain. No fancy shapes, just black 11pt Arial with sometimes some gray borders. You can see the <a href="https://www.examenblad.nl/2025/vwo/vakken/talen/engels-vwo" hreflang="nl"><time datetime="2025">2025</time> English <span lang="nl">vwo</span> exam</a> for reference.

<figure>
    <img src="https://cdn.gijs6.nl/blog/exam-design/25-01.png" alt="Cover of the 2025 vwo English exam.">
    <img src="https://cdn.gijs6.nl/blog/exam-design/25-02.png" alt="First questions page of the 2025 exam.">
    <figcaption>The <time datetime="2025">2025</time> design: cover and first questions page</figcaption>
</figure>

Honestly, this design is fine. There's room for improvement (the line-height is a bit tight, and the cover is not always clear), but it does its job. Everything that needs to be communicated is communicated, clearly and without any distractions.

That's what exam design should do. The goal isn't to look good or feel modern; it's to get information across as clearly as possible to as many candidates as possible. <strong>A good exam design goes completely unnoticed.</strong>

So when you compare the old design to the <a href="https://www.examenblad.nl/2026/vwo/vakken/talen/engels-vwo" hreflang="nl">new one</a>, the problems become obvious pretty quickly.

<figure>
    <img src="https://cdn.gijs6.nl/blog/exam-design/26-01.png" alt="Cover of the 2026 vwo English exam.">
    <img src="https://cdn.gijs6.nl/blog/exam-design/26-02.png" alt="First questions page of the 2026 exam.">
    <figcaption>The <time datetime="2026">2026</time> design: cover and first questions page</figcaption>
</figure>

The new design is full of visual clutter. There are decorative diagonal shapes on the cover, text with weird borders snaking around it, icons, text blocks with gray backgrounds, gray text all over the place, and the word <span lang="nl">"Vraag"</span> printed in front of every single question number. None of this adds information. It just adds noise, which is exactly what you don't want when someone is trying to concentrate.

The accessibility argument is also hard to take seriously when you look at the gray background blocks they've introduced. Those blocks actually have worse contrast than anything in the old design. For some of the blocks, contrast ratio is around 6.89:1, which actually **fails** <abbr title="Web Content Accessibility Guidelines">WCAG</abbr> AAA. The old design, boring as it was, had black text on white paper.

Then there's the bold text problem. In the new design, all questions are printed in bold. The idea is probably to make the questions stand out from the text surrounding them. But questions sometimes need emphasis within them too, and the way the <span lang="nl">CvTE</span> solved that was to make that text *even bolder*. In practice, the difference is almost invisible. My English teacher pointed this out to me after the exam; I hadn't noticed it while actually sitting the test (which is exactly the problem).

<figure>
    <img src="https://cdn.gijs6.nl/blog/exam-design/26-03.png" alt="Close-up of question 8 from the 2026 exam.">
</figure>

And then there's the points. In the old design, the number of points for each question was shown before the question number, so you could easily look at a page and immediately get a sense of how the points were across questions. In the new design, the points are in parentheses after the question. Scanning a page to plan your time is now noticeably harder.

What frustrates me most is the irony of it all. The <span lang="nl">CvTE</span> redesigned these exams specifically for accessibility reasons, and in doing so introduced contrast failures, bad visible emphasis, and a more cluttered layout. The old design wasn't exciting, but it was legible. That used to be enough.

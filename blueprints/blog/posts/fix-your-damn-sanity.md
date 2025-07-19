---
title: An OS to fix your damn sanity
---

# An OS to fix your damn sanity (and it's not fucking macOS)

*This rant (sorry, I mean blogpost) contains some strong language*

<p id="os-message" style="display: none;"></p>

<script src="https://cdn.jsdelivr.net/npm/ua-parser-js@1/dist/ua-parser.min.js"></script>
<script>
    const parser = new UAParser();
    const os = parser.getOS().name;

    let message = "";

    if (os === "Linux") {
        message = "You're already on Linux. Good. You're one of the few sane ones. Stick around, maybe you'll enjoy the rant :)";
    }

    const el = document.getElementById("os-message");
    el.innerHTML = "<strong>" + message + "</strong>";
    el.style.display = "unset";
</script>

Let's just be honest for a second. If you're even a little techy, there's a point where you have to stop tolerating bullshit. And when it comes to operating systems, the amount of bullshit is fucking huge. So here's my take; honest, slightly ranty, and yes, probably what you needed to hear a really long time ago.

Switch. If you are even slightly technical, just switch. Switch to Ubuntu, Debian, Arch (preferably), Gentoo, anything. I am definitely not the first person to tell you this, but just switch, dammit. Stop making excuses.

Windows has just imploded. The change between the Windows versions is completely mental. XP and 7 are just amazing. Just great. Unmatched design, great user experience, everything. But Microsoft thought it was better to just fuck up their OS, put popups and AI every-fucking-where. Windows is broken, but well, it is easy to use for non-techy people. And PowerShell is a great shell. But there is just so, so much wrong with Windows (they even removed the BSOD?!?!). Developing on Windows is doable (WSL is actually really great), but it's not the best. The system gets in your way, tries to suffocate you with updates, installs crap without your consent, and overall just treats you like an idiot. And sure, it works. It's "fine". But "fine" isn't good enough anymore. Especially not if you're writing code, doing actual work, or just want your machine to be nice to you instead of treating you like a fucking child.

And don't even get me started about macOS. I have to admit, the hardware in the MacBooks is quite good (apart from the damn ports; how the fuck can you build a modern laptop without any fucking USB-A ports???? USB-C is great, but you can't just straight up remove USB-A ports??! And also not even HDMI(!??!?!?!?!), no audio jack, no Ethernet (alright MacBooks aren't the only ones without Ethernet, but still), nothing...). But apart from the hardware, macOS is just unusable. The window manager is the worst ever made, and it seems like Apple's favourite hobby is just making your life harder<!--(did I say harder? I mean *fucking suicidal* (oh wow I just said that, YEAH I DID, DEAL WITH IT))-->. (Apart from the ecosystem, like the integration with other Apple devices can be really good, but that is the last exception I'm making.) It is just fucking unusable. AND THE KEYBOARDS!!! I completely agree that the normal keyboard layout (and then I'm mostly talking about the Ctrl, Super, and Alt keys) is messy and very illogical, but it is just what people are used to. And then Apple has the *cOmManD* and *oPtIoN* key, and when you plug in an Apple keyboard, THE ALT AND SUPER KEYS ARE SWAPPED AROUND??? Oh, and if I'm talking about keyboards, let's talk about the worst design the world has ever seen: Apple's Magic Mouse. It is the answer to the question "how can we design a mouse that is unusable, ugly, messes up your wrist, and that you can't use when it is charging?"  
And writing software for Apple products is even worse. I recently had to build an extension, so I wanted to make it available for Safari (well, I didn't want that at all, but I had to). Of course, I couldn't install Safari on my own machine (Arch), of course I couldn't, imagine if Apple would make your life easy. I had to get a MacBook. JUST MAKE YOUR BROWSER AVAILABLE ON EVERYTHING. If you want to, you can install Microsoft Edge on Linux and on macOS. You really can. (If you want to, you should immediately contact a medical professional, but you can!). But no, I had to use Xcode and just omg holy shit I hate Apple so much (I don't know if you have noticed).  
So if you have a MacBook or just another device that runs macOS, throw it out the window and buy something sensible. Since you were using Apple products, the rest will feel so fucking cheap for you. And guess what; the quality is also better (I know that is hard for Apple users to even imagine, but it is very much the fucking reality)!

Linux gives you actual control. Real control. Your system doesn't fight you; it helps you. You decide how things work. And that scares people. But once you get used to it, there's no way you're going back to an OS that constantly fucks with you. No big decisions made for you (well apart from the distro I guess). No forced updates at 3AM. No bullshit "let's restart your machine just when you wanted to be productive because we said so".

I used Windows since I was very small. And it is what I was used to. I didn't want to switch to Linux, because well, change is messy. But I did. And holy shit, the difference is so little. If you just use a great desktop environment (Cinnamon is amazing), the change is really, really small. And with the internet as your friend, you can really find your way around on Linux. Even drivers are rarely a problem nowadays. Hardware support is way better than it used to be. AND HOLY SHIT PACKAGE MANAGERS ARE AMAZING. No more fucking around with `.msi` and random installers, just `paru -S <your favourite package>` or whatever package manager you're using. Installing anything is just fucking clean and simple.

Even for gaming, Linux is not as bad as people think. I have only had one game so far that just refused to work on Linux, but all the other games work just fine. And I know, I don't play big MMOGs, and I know some of those big titles don't run on Linux. But, with Proton, and all other stuff, you can get 90% of your stuff running without pain. The other 10%? Deal with it or dual boot. Or go outside. Touch some grass. I don't care. And honestly, Valve is pushing Linux gaming harder than Microsoft ever did for its own platform. Steam Deck runs an Arch derivative, and it's doing just fine, thanks Valve :).

So yeah. You don't need to be a senior software engineer that has 20 years of experience in making an OS in assembly to use Linux. It's not some obscure system. It's just better. More stable, more transparent, more respectful of your time, your hardware, and your sanity. If you're still using Windows or macOS, ask yourself two things: are you mentally stable (just kidding) and are you really okay with how bad things have gotten? You deserve better.

Just switch. You'll thank yourself later. And if not, at least you'll stop screaming at your OS every damn day.

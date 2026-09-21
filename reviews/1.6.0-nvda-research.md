# NVDA Research for NVDA Coach

Date of research: 20 September 2026.
Coach version reviewed: 1.5.7, minimumNVDAVersion 2024.1, lastTestedNVDAVersion 2026.1.1, 45 lessons in six chapters.

## How this was verified

Every command and setting below was checked against the primary documents, not from memory. I downloaded and read the full text of:

- NVDA 2026.2 User Guide: https://download.nvaccess.org/releases/2026.2/documentation/en/userGuide.html
- NVDA "What's New" changelog, full history: https://download.nvaccess.org/releases/2026.2/documentation/en/changes.html
- NVDA 2024.1 User Guide, used to test whether a thing changed or was never right: https://download.nvaccess.org/releases/2024.1/documentation/en/userGuide.html
- NV Access release index: https://www.nvaccess.org/category/news/releases/
- NVDA 2026.2 announcement: https://www.nvaccess.org/post/nvda-2026-2/
- NVDA 2026.3 beta 1 announcement: https://www.nvaccess.org/post/nvda-2026-3beta1/
- NVDA Roadmap: https://www.nvaccess.org/post/nvda-roadmap/
- In-Process, 8 September 2026: https://www.nvaccess.org/post/in-process-8th-september-2026/

Where I could not verify something I say so. I did not check the Add-on Store listing page itself, and I did not run any NVDA build, so every claim here is documentation-based.

---

# Part 1: Where NVDA is now

## Current version

The current stable release is **NVDA 2026.2, released 31 August 2026** (https://www.nvaccess.org/category/news/releases/ and https://www.nvaccess.org/post/nvda-2026-2/).

**NVDA 2026.3 beta 1 was released 7 September 2026** (https://www.nvaccess.org/post/nvda-2026-3beta1/). No stable date for 2026.3 is published. NV Access describes a pattern where a beta follows a stable release by about a week (https://www.nvaccess.org/post/in-process-8th-september-2026/), so 2026.3 stable is likely inside the next few months, but that is my inference, not a published date.

The Coach's `lastTestedNVDAVersion` of 2026.1.1 is one stable release behind.

## Release timeline since the Coach's minimum

| Version | Date | Headline |
|---|---|---|
| 2024.1 | - | Coach's minimum. Added the Audio settings panel, opened with NVDA+control+u |
| 2024.2 | - | Sound split (NVDA+alt+s); browse mode `p` for paragraph; synth ring large-step keys |
| 2024.3 | - | Add-on update notifications on startup; Unicode normalization |
| 2024.4 | - | Configurable multiple key press timeout; braille formatting options |
| 2025.1 | 2025 | NVDA Remote Access built in. **Breaks add-on compatibility** |
| 2025.2 | 13 Aug 2025 | Browse mode heading quick nav extended to levels 7, 8, 9; language reporting |
| 2025.3 | 15 Sep 2025 | Add-on Store sorting; Remote Access and braille fixes |
| 2025.3.1 / .2 / .3 | Oct 2025 to Feb 2026 | Patch releases |
| 2026.1 | 6 May 2026 | MathCAT built in; new **Privacy and Security** settings category; drops Windows 8.1, 32-bit Windows, Windows 10 on ARM. **Breaks add-on compatibility** |
| 2026.1.1 | 20 May 2026 | Security patch |
| 2026.2 | 31 Aug 2026 | Built-in **Magnifier**; **NVDA+x** repeat last spoken information; touch browse mode; automatic braille scrolling; undo after factory reset |

Dates are from https://www.nvaccess.org/category/news/releases/. The 2024.x dates are not on that page and I did not chase them separately; the feature attributions come from the changelog.

### Add-on compatibility note

2025.1 and 2026.1 each carry an "Important notes: this release breaks compatibility with existing add-ons" entry in the changelog. **2026.2 has no such note** and its "Changes for Developers" section contains only component updates and additive changes. So NVDA Coach 1.5.7, with lastTested 2026.1.1, should load on 2026.2 without being disabled. That is an inference from the absence of a compatibility-break entry, not a statement NV Access made. It is worth confirming on a real 2026.2 install before relying on it.

## What NVDA gained since 2024.1 that a beginner now meets

These are all verified in the 2026.2 User Guide. None of them are taught by the Coach.

**Repeat last spoken information. NVDA+x.** "Repeats the last information spoken by NVDA. Pressing twice shows it in a browseable window." New in 2026.2. NV Access placed it in the basic frequently-used commands table in the Quick Start section of the guide, which is a strong signal about how fundamental they consider it.

**Cycle speech mode. NVDA+s.** Four modes: Talk (default), On-demand, Off, Beeps. On-demand speaks only when you issue a reporting command and stays silent on focus changes. A beginner who hits NVDA+s by accident lands in a mode where NVDA appears broken. There is also a setting, "Modes available in the Cycle speech mode command", that lets a user remove modes from the cycle.

**Direct settings shortcuts.** The guide states "Some settings categories have dedicated shortcut keys." Verified openers: NVDA+control+g General, NVDA+control+v Speech, NVDA+control+s Select Synthesizer, NVDA+control+a Select Braille Display, NVDA+control+u Audio, NVDA+control+w Magnifier, NVDA+control+k Keyboard, NVDA+control+m Mouse, NVDA+control+o Object Presentation, NVDA+control+b Browse Mode, NVDA+control+d Document Formatting. Also ctrl+tab and shift+ctrl+tab move between settings categories from anywhere in the dialog.

**Report link destination. NVDA+k.** "Pressing once speaks the destination URL of the link at the current caret or focus position. Pressing twice shows it in a window for more careful review."

**Magnifier.** New in 2026.2. NVDA+shift+w starts and stops it, NVDA+control+w opens its settings. Zoom from 100 to 5000 percent, default 200. Colour filtering, focus tracking modes. Fullscreen only for now. Cannot run at the same time as Screen Curtain.

**Multiple key press timeout.** In Keyboard settings since 2024.4. Configures how long NVDA waits before a second press of the same key counts as a new gesture rather than a double press. The changelog says this "may be especially useful for people with dexterity impairment."

**Browse mode heading levels 1 to 9.** Extended from 1 to 6 in 2025.2.

**Browse mode paragraph quick nav, `p`.** Added 2024.2.

**Privacy and Security settings category.** New in 2026.1. Screen Curtain moved here from Vision. Logging level and usage statistics moved here from General.

**Settings tree has grown.** Current top-level categories are General, Speech, Select Synthesizer, Synth settings ring, Braille, Select Braille Display, Audio, Privacy and Security, Vision, Magnifier, Keyboard, Mouse, Touch Interaction, Review Cursor, Object Presentation, Input Composition, Browse Mode, Document Formatting, Document Navigation, Math Settings, Add-on Store Settings, Remote Access Settings, Windows OCR Settings, Advanced Settings.

**Add-on Store gained visible machinery.** Startup notification of available add-on updates since 2024.3, checked daily. VirusTotal scan results and per-add-on changelogs since 2026.1. Sorting by minimum and last-tested NVDA version since 2025.3.

**Object navigation flattened view.** NVDA+numpad9 and NVDA+numpad3 on desktop, NVDA+shift+[ and NVDA+shift+] on laptop. This is older than the Coach's minimum, added in 2023.2, so it is a gap rather than a change, but it is the single most useful thing missing from the Coach's object navigation chapter.

**Undo after factory reset.** New in 2026.2. An Undo button appears after resetting NVDA to factory defaults.

## What the Coach teaches that has gone stale

This is the section that matters most. Six items. Three are factually wrong today; three are drift.

### 1. Laptop object navigation key is wrong. Severity: high.

`object_navigation.json`, lesson "Read the Current Navigator Object", both steps, and `keyboard_reference.json`, lesson "Desktop vs Laptop Keyboard Layout", where it is used as the worked example of how the two layouts differ.

The Coach teaches "NVDA+NumPad5 (desktop layout) or NVDA+Shift+Comma (laptop layout)" and even explains where the comma key is.

The 2026.2 User Guide's object navigation table gives:

| Name | Desktop key | Laptop key |
|---|---|---|
| Report current object | NVDA+numpad5 | NVDA+shift+o |

I checked the 2024.1 User Guide as well. It says NVDA+shift+o too. So this was never correct, it is not a change NVDA made. I could find no command anywhere in the 2026.2 guide bound to NVDA+shift+comma. The only use of shift+comma is browse mode "Move to start of container", with no NVDA modifier.

A laptop-layout learner following this lesson presses a key that does nothing, twice, in the lesson that is supposed to teach them the command, and again in the lesson that teaches them how layouts work. Fix this first.

### 2. NVDA+Ctrl+U is described as something it is not. Severity: high.

`nvda_settings.json`, lesson "Change the Audio Output Device", both steps.

The Coach says NVDA+Ctrl+U "opens the audio output device picker, letting you choose which audio device NVDA uses for speech without opening the Settings dialog", and then in a hands-on step, "A dialog will appear with a list of audio output devices. Use the Up and Down Arrow keys to move through the list... press Escape to close the dialog without making a change."

The 2026.2 User Guide heading is "Open Audio settings", key NVDA+control+u. It opens the Audio **category of the NVDA Settings dialog**, which contains Output device, Audio Ducking Mode, volume options and more. It is not a standalone picker, arrowing does not move through a device list until the learner is on the Output device combo box, and Escape cancels the whole Settings dialog.

The changelog shows this was introduced in **2024.1**, the Coach's own minimum version: "This can be opened with NVDA+control+u" and "The settings to change audio output device and toggle audio ducking have been moved to the new Audio settings panel from the Select Synthesizer dialog." So the description has been wrong for the entire supported range. This is a "Try it now" step, so the learner hears something that does not match what they were told.

### 3. The "Reset to defaults" button in Speech settings does not exist. Severity: medium.

`nvda_settings.json`, lesson "The Synth Settings Ring", final step: "use the Reset to defaults button in the Speech settings panel."

The 2026.2 User Guide's description of the NVDA Settings dialog names only Apply, OK and Cancel. I found no per-category reset button anywhere in the guide. What does exist is "Reset Configuration To Factory Defaults" in the NVDA menu, and NVDA+control+r, which resets to last saved on one press and to factory defaults on three presses. As of 2026.2 a factory reset offers an Undo button.

I am confident there is no Speech-panel reset button in the documentation. I cannot rule out that one exists and is undocumented, so verify in the app before rewriting.

### 4. Audio ducking option name has drifted. Severity: low.

`nvda_settings.json`, lesson "Control Audio Ducking" calls the three modes "no ducking, duck while speaking, and always duck", and recommends "Duck While Speaking".

The guide's actual option strings are "No Ducking", "Duck when outputting speech and sounds", and "Always duck". A learner hunting a combo box for the phrase the Coach gave them will not find it.

Also worth adding to that lesson: audio ducking is only available in an installed copy, not portable or temporary, and since 2026.1 it is not available with SAPI 4 or 32-bit SAPI 5 voices.

### 5. Heading levels are now 1 to 9, not 1 to 6. Severity: low.

`browse_mode.json`, lesson "Jump to Heading Levels": "you can press a number from 1 to 6 to jump directly to a heading of that level."

Extended to 1 through 9 in NVDA 2025.2. Nothing breaks, the lesson is just incomplete. One-word fix.

### 6. Manifest metadata. Severity: low.

`lastTestedNVDAVersion = 2026.1.1` against a current stable of 2026.2. Bump it after testing on 2026.2.

### What I checked and found still correct

Worth recording so nobody re-audits it. All verified against the 2026.2 User Guide: NVDA+n menu, NVDA+t title, NVDA+f12 time and date, NVDA+shift+b battery, NVDA+tab report focus, NVDA+1 input help, control to stop speech and shift to pause, NVDA+upArrow / NVDA+l read line, NVDA+downArrow / NVDA+a say all, NVDA+shift+upArrow / NVDA+shift+s read selection, NVDA+f report formatting, NVDA+space browse and focus toggle, NVDA+f7 Elements List, NVDA+control+f find with NVDA+f3 and NVDA+shift+f3, control+alt+arrows for table cells, single letter nav h k f d l, NVDA+numpad5 desktop object read, NVDA+numpad8 / numpad2 / numpad4 / numpad6 and their laptop equivalents NVDA+shift+upArrow / downArrow / leftArrow / rightArrow, NVDA+numpadMinus and NVDA+backspace move to focus object, NVDA+shift+numpadMinus and NVDA+shift+backspace move focus to review position, all synth settings ring keys including the PageUp and PageDown large steps, and the NVDA menu path Preferences then Settings. The Coach's object navigation chapter is accurate apart from item 1 above, and the synth ring lesson is accurate apart from item 3.

## Where NVDA is heading

From the official roadmap, last updated 6 May 2026 (https://www.nvaccess.org/post/nvda-roadmap/).

Short term, meaning most likely to land within a year: general stability work on long-standing freezes and crashes, braille improvements for single-line displays, **import and export of configuration**, and an **installer redesign using MSIX**.

Medium term: Magnifier cursor tracking, a corporate deployment mode, a secure add-on runtime with limited system access, OCR model selection, wider Microsoft Office UIA support, and end-to-end encryption for Remote Access.

Long term: on-device image description, braille font attributes on multi-line displays, video call readiness, and machine-learning UI element recognition.

Confirmed in flight for 2026.3 (https://www.nvaccess.org/post/nvda-2026-3beta1/): performance and caching work, context menus and keyboard shortcuts in the Configuration Profiles, Input Gestures and Speech Dictionaries dialogs, the ability to modify an existing gesture directly in the Input Gestures dialog, a modernised browseable message window, and expanded touch gestures including two-flick combinations and screen-edge gestures.

Relevant to the Coach specifically: NV Access have updated their own "Basic Training for NVDA" module with **magnifier content and sections on reviewing spoken information** (https://www.nvaccess.org/post/in-process-8th-september-2026/). That is NV Access independently concluding that the Magnifier and NVDA+x belong in beginner training. It is also the clearest signal of where the Coach's direct comparison point is moving.

Also announced: windowed and docked Magnifier modes are planned once the fullscreen mode is polished. So any Magnifier lesson written now will need revisiting.

---

# Part 2: What NVDA Coach should add

Ranked by value to a beginner. Lesson counts are rough.

## Priority 0: Fix the six stale items

Not an addition, but it outranks every addition below. Items 1 and 2 in particular are hands-on steps where the learner presses a key and hears something other than what the Coach promised, which teaches them to distrust the tool. Roughly half a day of editing, no new lesson architecture. Items 1, 2 and 3 should be verified in a live NVDA 2026.2 before the rewrite.

## 1. Speech modes and repeating what NVDA just said

**Teaches:** NVDA+x to repeat the last thing NVDA said, pressed twice to open it in a browseable window. Then NVDA+s to cycle the four speech modes, what Talk, On-demand, Off and Beeps each do, and how to get back to Talk.

**Chapter:** Getting Started. Naturally extends the existing "Stop NVDA from Talking" lesson into a three-lesson arc on controlling what NVDA says.

**Lessons:** 2.

**Why a beginner needs it:** "What did it just say?" is the most common thing a new screen reader user asks out loud, and until 2026.2 the answer was "nothing, you missed it." NVDA+x is the answer and it is three weeks old, so no existing training material a student might have covers it. The speech-mode half is the other side of the same coin: a beginner who fat-fingers NVDA+s lands in On-demand or Off, concludes NVDA is broken, and calls for help. The Coach currently teaches control and shift for stopping and pausing but never explains that NVDA has a mode at all. NV Access adding "reviewing spoken information" to Basic Training this month is independent confirmation this is the right call.

**Caveat:** NVDA+x needs 2026.2. Either gate the lesson or word it as "if you are on NVDA 2026.2 or later". Given the Coach's minimum is 2024.1 this matters.

## 2. Getting around NVDA Settings faster

**Teaches:** The direct settings shortcuts, principally NVDA+control+k for Keyboard, NVDA+control+v for Speech, NVDA+control+u for Audio, NVDA+control+g for General. Then ctrl+tab and shift+ctrl+tab to move between categories, and first-letter navigation in the category list. Also a short orientation to what is in the tree now, including Privacy and Security and Magnifier.

**Chapter:** Customizing NVDA.

**Lessons:** 1, possibly 2 if the settings-tree tour is separated.

**Why a beginner needs it:** Customizing NVDA is the thinnest chapter at 4 lessons and it is the chapter that ends the course, so it is what the learner remembers. Right now three separate lessons walk the student through "NVDA+N, then P, then S, then find the category", which is four keystrokes and a list hunt for something that has a single shortcut. Teaching NVDA+control+k in the keyboard-layout lesson makes that lesson shorter and better. This also fixes item 2 in the staleness list as a side effect, because NVDA+control+u stops being an odd special case and becomes one of a family.

## 3. Knowing where a link goes before you follow it

**Teaches:** NVDA+k to speak a link's destination URL, pressed twice for a browseable window. Why "click here" and "read more" links are a problem. Checking a link before activating it.

**Chapter:** Browse Mode and the Web. Extends "Navigate by Link", which currently teaches k, shift+k and tab and stops there.

**Lessons:** 1, or 3 extra steps folded into the existing link lesson.

**Why a beginner needs it:** Link text and link destination are different things, and a new user has no way to discover that. This is also the one place in the whole course where a safety habit can be taught without lecturing: the ability to check a destination before activating is the practical defence against a phishing link in an email. Cheap to add, disproportionate value.

## 4. The Add-on Store

**Teaches:** NVDA+n then t then a. The Available, Installed, Updatable and Incompatible tabs. Installing, updating, and what the startup "add-on updates available" notification means. What the compatibility warning means when an add-on has not been tested with your NVDA version.

**Chapter:** New short chapter, or appended to Customizing NVDA.

**Lessons:** 2.

**Why a beginner needs it:** The learner has already used the Add-on Store, because that is where most of them got NVDA Coach. NVDA checks for add-on updates daily and notifies on startup, so a beginner will meet a notification they do not understand within their first week. The compatibility warning in particular produces support calls, and is the exact mechanism that would block the Coach itself after an NVDA release that breaks the add-on API, as 2025.1 and 2026.1 both did.

**Honest caveat:** this is the recommendation I am least certain about. It is arguably a Windows-software-management skill rather than a screen reader skill, and it is hard to drill because the Coach cannot safely make a student install something. Write it as guided walkthrough rather than hands-on, or skip it.

## 5. Making double-press commands work for you

**Teaches:** That many NVDA commands do something different when pressed twice or three times, that this is a timing window, and that the window is adjustable in Keyboard settings under "Multiple key press timeout".

**Chapter:** Your Keyboard, or Customizing NVDA.

**Lessons:** 1, or a few steps added to an existing keyboard lesson.

**Why a beginner needs it:** The Coach already depends on double-press in at least five lessons: NVDA+t twice to spell the title, NVDA+f12 twice for the date, NVDA+numpad5 twice to spell an object, NVDA+f twice for a formatting window, and NVDA+x twice if recommendation 1 is built. A student with a tremor, arthritis, or simply an unhurried touch fails all of those silently and has no idea why. Since the Coach is explicitly built for absolute beginners and used by AT instructors with older learners, the setting that makes those commands reachable belongs in the course rather than buried in the guide. This is the recommendation with the best value-to-effort ratio after the fixes.

## 6. Object navigation without the hierarchy

**Teaches:** Flattened view. NVDA+numpad9 and NVDA+numpad3 on desktop, NVDA+shift+[ and NVDA+shift+] on laptop. Moving through every object in a window in order without having to reason about what contains what.

**Chapter:** Object Navigation.

**Lessons:** 1.

**Why a beginner needs it:** Containment is the hardest idea in chapter 5, and the Coach's own final lesson admits object navigation is an advanced tool most people rarely need. Flattened view is the beginner-friendly version: sweep the window, hear everything, no pyramid required. It works on the Coach's existing minimum of 2024.1, since it landed in 2023.2, so there is no version gate. Place it before "Move Up and Down Levels" so the student has a working technique before they meet the theory.

## 7. Round out the browse mode quick-navigation set

**Teaches:** `p` for paragraph, `g` for graphic, and the existence of the full single-letter set, including the specific form-control keys b, x, c, r and e that sit underneath the general `f`. Plus the heading-levels correction from 1 to 6 up to 1 to 9.

**Chapter:** Browse Mode and the Web.

**Lessons:** 1.

**Why a beginner needs it:** The Coach teaches five of roughly eighteen single-letter keys, which leaves the student thinking that is all there is. `p` in particular is the one they will use daily on article pages and it was added in 2024.2. Low effort because the practice page already exists.

## 8. The Magnifier

**Teaches:** NVDA+shift+w to start and stop, NVDA+control+w for settings, zoom level, colour filtering, and that it cannot run alongside Screen Curtain.

**Chapter:** Customizing NVDA.

**Lessons:** 1.

**Why:** It is the headline feature of the current release and NV Access has already added it to Basic Training. For the Coach's primary audience of blind learners it is not relevant, but the README positions the Coach for AT instructors and TVIs, who also teach low-vision students, and for whom "NVDA now has a magnifier built in" is genuinely new information.

**Honest caveat:** it is fullscreen-only today and NV Access has said windowed and docked modes are coming, so anything written now will need a rewrite within a year or so. Write it thin and factual, or defer until the docked modes land. I would defer.

## Not worth doing

**Remote Access (2025.1).** Genuinely significant and it is built into NVDA now, but it is a support and teaching tool, not a beginner skill. It requires two machines and another person, so it cannot be drilled. An instructor will teach it live if they need it.

**MathCAT and math reading (2026.1).** Real and built in, but a beginner does not encounter math content until well past this course, and the Coach would need math practice content it does not have.

**Braille.** The README already lists a braille display module as planned, and that is the right framing. It is a product, not a chapter, it needs hardware the learner may not own, and NV Access is actively changing braille behaviour every release including automatic scrolling in 2026.2. Keep it parked.

**Sound split, NVDA+alt+s (2024.2).** A preference, not a skill. If you want it, make it one step inside the audio lesson. Not its own lesson.

**Touch gestures (expanded in 2026.2 and again in 2026.3).** Only applies to Windows touchscreen devices, small share of the Coach's audience, and the gesture set is actively changing between releases. Skip unless someone asks.

**Unicode normalization, language reporting, spelling errors as sounds, natural pause after punctuation.** All real settings, none of them things a beginner needs to be taught. They belong in the user guide, which the Coach already teaches students to open.

## Summary of the recommended build

| Rank | Addition | Chapter | Lessons |
|---|---|---|---|
| 0 | Fix the six stale items | Across four chapters | 0 new |
| 1 | Speech modes and NVDA+x | Getting Started | 2 |
| 2 | Settings shortcuts and the settings tree | Customizing NVDA | 1 to 2 |
| 3 | NVDA+k, where a link goes | Browse Mode | 1 |
| 4 | Add-on Store | New or Customizing | 2 |
| 5 | Multiple key press timeout | Your Keyboard | 1 |
| 6 | Object navigation flattened view | Object Navigation | 1 |
| 7 | Rest of the quick-nav keys | Browse Mode | 1 |
| 8 | Magnifier, or defer | Customizing NVDA | 1 |

Taking priority 0 plus recommendations 1, 2, 3, 5 and 6 gives roughly 6 to 7 new lessons and brings the Coach to about 52. That set contains no version-gated content except NVDA+x, requires no new lesson machinery, and covers everything a 2026 beginner will actually hit in their first month.

# Factual corrections in NVDA Coach 1.6.0

Read this before translating anything in `nvda_settings.json`,
`browse_mode.json`, `keyboard_reference.json`, `reading_text.json` or
`getting_started.json`.

During the 1.6.0 review we checked the commands NVDA Coach teaches against
NVDA's own documentation, command by command. Ten of them were wrong. Some
had been wrong since before your language was added, which means the error
was faithfully translated into every language. That is not your mistake. It
is ours, and this note exists so it stops here.

Every correction below was verified on 2026-09-20 against NVDA's Commands
Quick Reference:
<https://download.nvaccess.org/documentation/keyCommands.html>

---

## 1. The laptop key for reading the current object — already fixed

**This one is done. No action needed from you.** It is listed because you may
notice your file changed and wonder who changed it.

NVDA Coach taught `NVDA+Shift+Comma` as the laptop-layout command for
"report current navigator object". That key is bound to nothing in NVDA. The
correct command is `NVDA+Shift+O`.

This was the worst of the ten. A student on a laptop pressed the key, nothing
happened, and nothing told them why - in the lesson whose whole purpose is
teaching them that laptop layout differs from desktop. The step's
`expectedGestures` value was wrong too, though that field is not currently
read by any code, so it changed nothing on its own.

It has been corrected in every language, including yours, along with the
sentences that existed only to explain where the comma key was. If the new
wording in your language reads badly, please change it — the constraint is
only that it must say `NVDA+Shift+O` and, where it locates the key, that O is
in the top row of letters between I and P.

---

## 2. `NVDA+Ctrl+U` — corrected in English, still wrong in your language

**What the lesson says now, in your language:** that `NVDA+Ctrl+U` opens an
audio output device picker, letting you choose the device "without opening
the Settings dialog".

**What NVDA actually does:** `NVDA+Ctrl+U` opens the **Audio category of the
NVDA Settings dialog**. There is no separate picker. The output device is one
of the settings in that category.

The English now reads:

> NVDA+Ctrl+U opens the Audio category of the NVDA Settings dialog, where the
> output device is one of the settings you can change.

This matters more than the others because it is a hands-on step — the student
is told what to expect and then sees something different.

**File:** `nvda_settings.json`

---

## 3. The "Reset to defaults" button — corrected in English, still wrong in your language

**What the lesson says now:** that the Speech category has a "Reset to
defaults" button restoring speech settings to factory values.

**What NVDA actually does:** there is no such button. The Settings dialog has
OK, Cancel and Apply. Resetting is done with `NVDA+Ctrl+R`: once reverts to
your last saved configuration, three times restores factory defaults.

A student will hunt for a button that is not there and conclude they have
misunderstood the dialog.

The English now reads:

> The Speech category has no reset button. To put every NVDA setting back to
> how it shipped, press NVDA+Ctrl+R three times: once reverts to your last
> saved configuration, and three times restores factory defaults.

**Note for your language:** `NVDA+Ctrl+R` is the command in every layout. Only
the surrounding description needs translating.

**File:** `nvda_settings.json`

---

## 4. Heading levels go up to 9, not 6 — corrected in English

**What the lesson says now:** in browse mode, press 1 to 6 to jump to headings
of that level.

**What NVDA actually does:** 1 to 9. The quick reference reads "1 to 9:
headings at levels 1 to 9 respectively."

A small thing, but a student taught "up to 6" will not know 7, 8 and 9 exist.

The English now reads:

> Press 1 to jump to level 1 headings, 2 for level 2, and so on up to 9.

**File:** `browse_mode.json`

---

## 5. The audio ducking option name

NVDA's option is **Audio Ducking Mode**, with modes for no ducking, ducking
when outputting speech and sounds, and always ducking. The lesson refers to
"Duck While Speaking" as though that were the label.

If your language's NVDA translation has official wording for the Audio
Ducking Mode option and its modes, please use that wording, since the student
will hear NVDA say it. This is the one correction where matching NVDA's own
translation in your language matters more than matching our English.

**File:** `nvda_settings.json`

---

## 6. A lesson 7 of 8 announced as the last in its chapter

In `reading_text.json`, the end of "Select and Highlight Text" said:

> Next up is the last lesson in this chapter: Navigate by Paragraph and Page

Navigate by Paragraph and Page is lesson 7 of 8. The very next lesson's own
closing text then correctly says "One more lesson remains in this chapter:
Check Font and Formatting", so the chapter contradicted itself two screens
apart. The English now reads "Next up is Navigate by Paragraph and Page,
lesson 7 of 8 in this chapter".

This is the same class of bug the 1.5.5 release fixed in other chapters. It
survived here.

**File:** `reading_text.json`

---

## 7. A checkbox named differently in the lesson and in the window

`getting_started.json` told the student to find a checkbox labelled
"Show practice hints". The actual checkbox says **"Show practice hints during
lessons"**.

This one matters more in your language than in English. The student is
listening, not looking: they hear the label read out and have to match it to
what the lesson just told them to find. If the lesson's wording and the
checkbox's wording differ in your translation, they will think they are in
the wrong place.

The other two checkboxes in that window are "Enable screen reader tips" and
"Open Coach window automatically on startup". Please check that all three
match between your lesson text and your `.po`.

**Files:** `getting_started.json` and your `nvda.po`

---

## 8. The Menu key is on the right, not the left

`keyboard_reference.json` said:

> The Windows key and the Menu key (if present) are usually only on the left
> side or only on one side of the keyboard.

The Menu key, also called the Applications key, is on the **right** of the
bottom row, next to the right Control key. NVDA's own guide puts it "next to
the right control key on most keyboards". The sentence also contradicted
itself.

**File:** `keyboard_reference.json`

---

## 9. NVDA has three modifier key choices, not two

`keyboard_reference.json` said the NVDA key "is one of two options: Insert or
Caps Lock". NVDA's Keyboard settings offers **three** checkboxes - Caps Lock,
the Insert key in the cluster above the arrows, and the Insert on the numeric
keypad - and any combination can be switched on at once.

The English now mentions all three. If your language's lesson simplifies this
for beginners, that is a reasonable choice; just do not say "two".

**File:** `keyboard_reference.json`

---

## 10. A cross-reference to a lesson that does not exist

`nvda_settings.json` referred twice to "the Moving Between Controls lesson in
the Getting Started chapter". No such lesson exists. The real title is
**"Move Between Controls with Tab"**.

Worth a general check in your language: when a lesson names another lesson or
another chapter, does that name match what the lesson picker actually shows?
We found one of these in Brazilian Portuguese too, where two chapters
disagreed about what the reading chapter is called.

---

## 11. Simplified and Traditional Chinese: four lessons missing from the readme

This one is only for the two Chinese translators.

Chapters 1, 3 and 6 each gained a lesson in 1.5.4 (chapter 6 gained two), and
no documentation page was updated to match. Your `doc/<lang>/readme.html`
still advertises 13, 7 and 2 lessons for those chapters, while your lesson
files correctly ship 14, 8 and 4.

The four lessons missing from your page are:

| Chapter | Lesson |
|---|---|
| Getting Started | Check Your Battery Status - `NVDA+Shift+B` |
| Reading and Moving Through Text | Check Font and Formatting - `NVDA+F` |
| Customizing NVDA | Change the Audio Output Device - `NVDA+Ctrl+U` |
| Customizing NVDA | Control Audio Ducking - `NVDA+Shift+D` |

All four are already translated in your lesson files, so the titles exist in
Chinese - it is only the readme's list and the "thirteen / seven / two"
counts in the chapter blurbs that need updating. We did not edit your page,
because the one-line description beside each lesson is prose.

Spanish, Polish, Russian and Turkish pages are NOT affected: those languages
genuinely ship 41 lessons and their pages are accurate.

---

## What we ask

Corrections 2, 3, 4 and 5 are fixed in English only. We deliberately did not
rewrite them inside your files. Rewriting several sentences of somebody's
translation, in a language we cannot read, to fix a fact — and then shipping
it under their name — is not a thing we are willing to do without asking.

So: when you next work on your language, please bring these four into line
with the English above. If you would rather we drafted them for you to check,
say so and we will.

If you find anything else NVDA Coach teaches that NVDA does not actually do,
tell us. You are the people most likely to notice, because you read every
sentence closely enough to translate it.

— Tony Gebhard, <info@tonygebhard.me>

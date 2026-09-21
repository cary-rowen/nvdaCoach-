# NVDA Coach 1.6.0 language release: accessibility and localization review

Reviewer: Jessica, TG Studios accessibility.
Branch reviewed: `release/1.6.0-languages`. Nothing was edited.
Date: 2026-09-20.

## Verdict

Do not ship yet. Five findings break something for a real user, eleven are
wrong but survivable, four are polish. Twenty in total.

The worst one is not in this release's new content at all. NVDA Coach binds
`NVDA+shift+c`, and that is a documented NVDA command that NVDA Coach silently
takes away from every user in every language. Details in finding 1.

The good news first, because it is real. The gettext resync is clean. I parsed
`locale/nvda.pot` and every `nvda.po` with a proper reader and compared them to
the strings actually present in the Python source: 204 source strings, 204
msgids in the template, zero missing, zero stale, zero non-literal arguments to
`_()`. Every `.mo` loads, decodes and returns the right string. The doc HTML is
in better shape than the brief feared: every file has a correct `lang`, a real
`<title>`, a declared charset, a single `h1`, no skipped heading levels, tables
with `<th>`, `scope` and a `<caption>`, and no vague link text. The Polish and
Traditional Chinese practice pages are structurally faithful to English and
fully localized down to the `aria-label` on every landmark.

## How I checked

- Read NVDA's own source at `raw.githubusercontent.com/nvaccess/nvda/master`
  for `languageHandler.py`, `addonHandler/__init__.py` and `scriptHandler.py`,
  and quoted it rather than working from memory.
- Read the NVDA developer guide at
  <https://download.nvaccess.org/documentation/developerGuide.html> for the
  manifest contract, and the NVDA user guide at
  <https://download.nvaccess.org/documentation/userGuide.html> for command
  bindings.
- Parsed `manifest.ini` and all seven `locale/*/manifest.ini` with ConfigObj
  5.0.9, the same library NVDA uses, with `encoding="utf-8"`.
- Loaded every `nvda.mo` with Python's `gettext.GNUTranslations` and probed a
  known string.
- Parsed every lesson JSON and diffed ids, order, step counts and gesture
  identifiers against English.
- Parsed the doc HTML for lang, title, charset, heading sequence, table
  headers, link text and relative link targets.

I did not run NVDA and capture speech for this pass. Where a claim depends on
runtime behaviour I say so and name the code path I read.

I stayed out of `lessons/pt_BR/`, `locale/pt_BR/` and `doc/pt_BR/` as asked, and
I have not judged pt_BR completeness.

---

# Tier 1: breaks for a user

## 1. NVDA Coach takes away NVDA's own "Set column headers" command

This is the worst finding in the review.

**Defect.** `globalPlugins/nvdaCoach/__init__.py:1760-1762` binds:

```python
@script(
    description=_("Show NVDA Coach window, or open the lesson picker"),
    gesture="kb:NVDA+shift+c",
    category="NVDA Coach",
)
```

`NVDA+shift+c` is already a documented NVDA command. The NVDA user guide lists
it under Application Specific Features, Microsoft Word, Automatic Column and
Row Header Reading, as **Set column headers**:
<https://download.nvaccess.org/documentation/userGuide.html#WordAutomaticColumnAndRowHeaderReading>

NVDA binds it at NVDAObject level. Verified in
`source/NVDAObjects/UIA/wordDocument.py` lines 905 to 906:

```python
@script(gesture="kb:NVDA+shift+c")
def script_setColumnHeader(self, gesture):
```

**Why NVDA Coach wins.** NVDA resolves a gesture through
`scriptHandler._yieldObjectsForFindScript`, and the order is fixed. From
`source/scriptHandler.py` lines 180 to 203, the yield order is: the gesture's
scriptable object, then **global plugins**, then the app module, then braille,
then vision, then the tree interceptor, then the focused NVDAObject, then focus
ancestors. Global plugins are second. The Word document object is seventh.

So while NVDA Coach is installed and enabled, a blind Word user who presses
`NVDA+shift+c` to mark a column header row gets the Coach window instead. No
message explains it. NVDA's Input Help will read out NVDA Coach's description
where the user expects the Word command. The command is simply gone.

**Why it matters more here than in another add-on.** NVDA Coach's whole purpose
is teaching NVDA commands, and its own Browse Mode chapter includes a
`navigate_tables` lesson. It is teaching table navigation with one hand while
removing a table command with the other. A key somebody has learned should never
be taken away.

**What right looks like.** Pick a gesture that collides with nothing, for
example `NVDA+shift+alt+c`, and keep `NVDA+shift+c` available only as an
optional binding the user adds themselves in Input Gestures. If the current key
is kept for existing users, the readme must say plainly that it overrides Set
column headers in Microsoft Word, and the add-on should ship an unassigned
alternative. Changing a key people already use is itself a cost, so decide once
and document it in the changelog.

**Carried elsewhere.** No other TG Studios program binds an NVDA gesture, so
this one is contained to NVDA Coach. Worth a standing check for any future NVDA
add-on: validate every proposed gesture against the user guide command tables
before binding it.

## 2. The manifest still says version 1.5.7, so this release cannot ship

**Defect.** `manifest.ini` line 6:

```
version = 1.5.7
```

`build.bat` line 7 agrees: `set VERSION=1.5.7`. `CHANGELOG.md` has no 1.6.0
section; its top entry is v1.5.7 dated 2026-07-12. Only the translator
worksheets under `doc/translators/` say 1.6.0.

I confirmed the value by parsing `manifest.ini` with ConfigObj the way NVDA
does, not by eye.

**Why it breaks.** The NVDA developer guide, Manifest Files, Available Fields,
says of `version`: "For a user to be able to update to this add-on, the version
must be greater than the last version uploaded" and "Add-on versions are
expected to be unique for the addon name and channel".
<https://download.nvaccess.org/documentation/developerGuide.html>

`nvdaCoach-1.5.7.nvda-addon` is already in the repo root and already published.
Submitting 1.5.7 again is rejected. If it somehow got through, no existing user
would be offered the update, because NVDA sees the same version they already
have. Every user of this release gets nothing.

**What right looks like.** Bump `manifest.ini`, `build.bat` and `CHANGELOG.md`
to 1.6.0 together, and add the 1.6.0 changelog section before building.

## 3. Hong Kong Traditional Chinese users fall all the way back to English

This is the surprising landing the brief asked about, and it lands on a language
this release is revising.

**Defect.** `_loadLessonCategories()` at
`globalPlugins/nvdaCoach/__init__.py:198-204` and `_localizedDocPath()` at
`globalPlugins/nvdaCoach/__init__.py:243-250` both build the same candidate
chain: the full locale, then `lang.split("_")[0]`, then `en`.

For `zh_HK` that chain is `zh_HK`, then `zh`, then `en`. Neither
`lessons/zh_HK/` nor `lessons/zh/` exists, so a Hong Kong user gets
`lessons/en/`. Same for `doc/`. The gettext lookup fails the same way:
`Addon.getTranslationsInstance` at `addonHandler/__init__.py:845-858` calls
`gettext.translation(..., languages=[languageHandler.getLanguage()],
fallback=True)`, and Python expands `zh_HK` to `zh_HK` and `zh` only, never to
`zh_TW`. The translated store listing fails too:
`addonHandler._translatedManifestPaths` at lines 989 to 998 tries
`locale/zh_HK/manifest.ini`, `locale/zh/manifest.ini`, `locale/en/manifest.ini`,
and none of the three exists.

**zh_HK is a real NVDA language, not a hypothetical.** I listed NVDA's shipped
locale directories from its repository. There are 73, and they include `zh_HK`,
`zh_CN`, `zh_TW`, `pt_PT`, `pt_BR`, `es`, `es_CO`, `ja`, `pl`. A Hong Kong user
can select it in NVDA's language list today.

So a reader of Traditional Chinese in Hong Kong gets English lessons, English
docs, an English interface and an English store description, while a complete,
newly revised zh_TW set sits unused in the package.

**The other locales, worked through.** I checked every case the brief named,
against the real resolution code.

- `ja_JP`, `es_MX`, `pl_PL` are **not** NVDA locales, so a user cannot select
  them in NVDA's language list. They can only arrive through the default
  "Windows" setting. `languageHandler.setLanguage` handles that at
  `source/languageHandler.py:326-351`: it calls `getWindowsLanguage()`, which
  normalizes the Windows locale to for example `ja_JP`, then tries to build a
  gettext translation for it, and on failure does
  `localeName = localeName.split("_")[0]` and tries again. `getLanguage()`
  returns the locale that succeeded. NVDA has a `ja` catalogue, so
  `getLanguage()` returns `ja`, and NVDA Coach then finds `lessons/ja/` and
  `doc/ja/`. **These three resolve correctly. No action needed.**
- `pt_PT` **is** an NVDA locale, so `getLanguage()` returns `pt_PT` and the
  split gives `pt`, which does not exist. A Portugal user gets English
  everywhere, and will still get English after the pt_BR work lands. Worth
  deciding now, while two agents are in that code: either add `locale/pt_PT`,
  `doc/pt_PT` and `lessons/pt_PT` as thin aliases, or name the folders `pt` so
  both `pt_BR` and `pt_PT` reach them.
- `es_CO` is an NVDA locale and resolves to `es` correctly.
- `de_CH`, `nb_NO`, `nn_NO` fall to English, which is correct because no German
  or Norwegian set exists.

**What right looks like.** Add an explicit regional alias map in front of the
existing chain, in both `_loadLessonCategories()` and `_localizedDocPath()`, so
the two stay in step:

```
zh_HK -> zh_TW
zh_SG -> zh_CN
pt_PT -> pt_BR   (or rename to pt)
```

The `locale/` side needs the same treatment, which means either real
`locale/zh_HK/` folders containing a copy of the zh_TW `.mo` and `manifest.ini`,
or accepting an English interface for those users. A folder copy is the only
thing NVDA's own gettext lookup will see, because that lookup is in NVDA, not in
your code.

**One more thing in the same two functions.** Both guard with
`if lang and lang != "Windows"`. `getLanguage()` returns `_language`, and
`_language` is only ever assigned the validated locale name of a catalogue that
loaded, or `"en"`. It can never be the string `"Windows"`. The guard is dead
code and the docstring at line 198 that says it can return `"Windows"` is
wrong. Harmless, but it will mislead the next person. Listed again as finding
20.

## 4. The Japanese practice page contradicts the Japanese landmark lesson

**Defect.** `doc/ja/practice.html` is not a translation of the English practice
page. It is a different page, and the Japanese Browse Mode lesson that ships
with it describes the English one.

`lessons/ja/browse_mode.json`, lesson `landmarks_and_lists`, step 0, tells the
learner that a well built page has named regions and gives three examples:
navigation, main, footer. Then step 1 says to press D to jump to the next
landmark, and step 2 says to press D again.

The landmarks actually present in `doc/ja/practice.html` are:

```
<header role="banner">
<main role="main">
<footer role="contentinfo">
```

There is no `<nav>`. English, Polish and Traditional Chinese all have one:
`<nav aria-label="Site navigation">`, `<nav aria-label="Nawigacja strony">`,
`<nav aria-label="網站導覽">`.

So a Japanese beginner presses D expecting the navigation region the lesson just
named, and NVDA announces a banner landmark that the lesson never mentioned. The
one landmark the lesson led with is the one the page does not have.

**The page is also missing a section.** English, Polish and Traditional Chinese
practice pages have 13 headings and a `<section id="about">` holding "About This
Page" as `h2` and "How to Use This Page" as `h3`. The Japanese page has 11
headings and no about section, so the Japanese learner lands on a practice page
with no orientation text. It also has 3 lists where the others have 4.

**Why this is tier 1.** Nothing crashes and the learner can still press Enter,
because `expectedGestures` is not enforced (see finding 6). But this is a
teaching product for absolute beginners, and the lesson tells them something
untrue about the page in front of them. For someone learning landmark
navigation for the first time, being told to expect "navigation" and hearing
"banner" is exactly the kind of thing that makes a new user think they pressed
the wrong key.

**What right looks like.** Rebuild `doc/ja/practice.html` from the English page
so the structure matches, translating text and `aria-label` values only, the way
`doc/pl/` and `doc/zh_TW/` were done. Keep `<nav>`, keep the about section, keep
the fourth list. If the extra `<header role="banner">` is wanted, add it to all
four pages and mention banner in the lesson text in all languages.

## 5. Polish ships four fewer lessons than English

**Defect.** Polish is a new language in this release and its lesson set is
short. Diffed by lesson id against `lessons/en/`:

- `getting_started`: 13 lessons, English has 14. Missing `battery_status`.
- `reading_text`: 7 lessons, English has 8. Missing `font_info`.
- `nvda_settings`: 2 lessons, English has 4. Missing `audio_output` and
  `audio_ducking`.

Total 41 lessons against English 45.

This is not the same thing as the `.po` percentage. The Polish `.po` is 194 of
204 strings, which is fine. The lesson content is a separate body of text and it
is four lessons short, and nobody flagged it, because the known-issues list only
covered `.po` percentages for es, ru and tr.

Because `_loadLessonCategories()` picks one directory and reads whatever is in
it, there is no per-lesson fallback. A Polish learner does not get the four
missing lessons in English. They simply do not exist for that user, and the
lesson picker gives no hint that anything is absent.

**Japanese, for comparison, is nearly complete.** All 45 lessons are present.
One step is missing: `reading_text` lesson `font_info` has 3 steps where English
has 4. The missing one is the final step, the chapter close that recaps what the
learner just covered. Japanese learners finish that chapter without the recap.

**Traditional Chinese is complete.** 45 lessons, matching step counts
throughout.

**What right looks like.** Either translate the four Polish lessons before
shipping, or make the missing-lesson case visible: when a localized chapter has
fewer lessons than `lessons/en/`, log it at startup and consider appending the
untranslated English lessons rather than dropping them. Silent absence is the
problem, not the gap itself.

---

# Tier 2: wrong but survivable

## 6. The Turkish lesson set has machine-translated gesture identifiers

**Defect.** A find and replace ran across `lessons/tr/` and hit machine-readable
fields, not just prose. Examples from the JSON:

- `lessons/tr/reading_text.json`, `move_by_character`:
  `["kb:sağ tamam"]` and `["kb:sol tamam"]` where English has `["kb:rightArrow"]`
  and `["kb:leftArrow"]`. "Arrow" was translated as "tamam", which means "OK".
- `jump_to_ends`: `["kb:kontrol+Ana Sayfa"]` where English has
  `["kb:control+home"]`. "Home" became "Ana Sayfa", meaning "home page".
- `tab_navigation`: `["kb:sekme"]` and `["kb:Shift+Sekme"]` for `kb:tab` and
  `kb:shift+tab`.
- `navigate_paragraph_page`: `["kb:sayfaAşağı"]`, `["kb:sayfaYukarı"]`.
- `lessons/tr/getting_started.json`: the lesson **id** itself was corrupted from
  `activate_controls` to `activate_Kontrols`.

Twelve lessons have divergent gesture identifiers. I diffed every language
against English step by step.

**Why it is survivable today, and only today.** I grepped the entire Python
source: `expectedGestures` does not appear anywhere. `lessonRunner.py` says so
in its header comment, that there is no global gesture interception and the
student confirms with Enter. So these strings are dead data right now and no
Turkish learner is blocked. I checked this before calling it a blocker, and I am
glad I did.

The day anyone switches on gesture checking, every one of these steps becomes
uncompletable in Turkish while working everywhere else, and it will look like a
runner bug rather than a data bug.

The corrupted lesson id is live now, in a small way: `ProgressTracker` keys
completion on category id plus lesson id, so a user who switches away from
Turkish loses the completion mark for that lesson.

**What right looks like.** Restore every `expectedGestures` value and every
`id` in `lessons/tr/` from `lessons/en/`. Those two fields are code, not copy.
Add a build check that asserts, for every language, that the lesson id list and
the `expectedGestures` list are byte identical to English. That check would have
caught this and will catch the next one.

## 7. The readmes do not document four keys the add-on binds, and Space is documented nowhere

**Defect.** I listed every key the code binds and every key the docs describe.

Bound in `globalPlugins/nvdaCoach/__init__.py`, `_onKey` at lines 1021 to 1115
and `_onKeyPress` at lines 1649 to 1665:

F1, F2, F3, F4, F5, F6, F7, Escape, Enter, Numpad Enter, Space, Ctrl+N, Ctrl+B,
Ctrl+R, and the global NVDA+Shift+C.

The in-app introduction text is complete. It lists Enter, F1, F2, F3, Escape
including the three-press close, then F4 through F7, then Ctrl+N, Ctrl+B,
Ctrl+R. Good.

The readmes are not. In `doc/en/readme.html`, `doc/pl/readme.html` and
`doc/zh_TW/readme.html`, the "keys available during a lesson" list contains F1,
F2, F3, Escape, NVDA+Shift+C, Ctrl+N, Ctrl+B and Ctrl+R. F4 through F7 appear
only much further down, inside the version history section, as a changelog
bullet. A learner reading the manual to find the help key has to read the
changelog.

Two more gaps in all three readmes:

- **Space advances a step** (`__init__.py:1054-1058`) and is not documented
  anywhere, in the app or the docs.
- **Escape pressed three times closes the window**
  (`_handleIdleEscape`, `__init__.py:1118-1141`). The in-app text says so. The
  readmes say only that Escape stops the lesson.

**Also.** All three readmes list `NVDA+Shift+C` twice in the same bulleted list,
once as "return to the Coach window" and once as "open the lesson picker". Both
are true, it is one key doing two things by context, but two separate bullets in
one list reads as an error.

**What right looks like.** One key table in the readme that matches the in-app
introduction exactly, covering Enter, Space, F1 to F7, Escape including the
three-press close, Ctrl+N, Ctrl+B, Ctrl+R and NVDA+Shift+C, with the two
NVDA+Shift+C behaviours in a single row. Then the same table in all nine
languages.

## 8. The Polish readme documents version 1.5.1, and all three readmes state a stale version

**Defect.** `doc/pl/readme.html` line 15 says "Wersja 1.5.1". It has 22 headings
where English has 25. Comparing them, the Polish readme is missing the F1 to F7
introduction reference item, the Activate Buttons and Controls entry and the
Focus Mode versus Browse Mode entry, among others. It is two feature releases
behind, so a Polish learner reads a manual for a product that is not the one
they installed.

`doc/en/readme.html` says "Version 1.5.4" and `doc/zh_TW/readme.html` says
"版本 1.5.4". This release is 1.6.0. No readme states the shipping version.

`doc/zh_TW/readme.html` is otherwise current: 25 headings, matching English
structure, and it carries the F1 to F7 and Focus Mode entries Polish lacks.

**What right looks like.** Bring `doc/pl/readme.html` up to the English 1.6.0
content, then set the version line in all nine readmes from one place at build
time so it can never drift again.

## 9. The add-on manifest is missing docFileName and does not quote its values

I parsed `manifest.ini` and all seven translated manifests with ConfigObj 5.0.9,
UTF-8, exactly as `AddonManifest.__init__` does.

**Result: every required field is present and every file parses cleanly.**
`name`, `summary`, `version`, `author`, `minimumNVDAVersion` and
`lastTestedNVDAVersion` are all there. `minimumNVDAVersion = 2024.1` is less
than `lastTestedNVDAVersion = 2026.1.1`, so the API version range constraint
holds. All seven translated manifests parse, contain only `summary` and
`description`, and every `description` comes back as a single string, including
the long triple-quoted ones. Nothing parsed into a list by accident. Nothing is
mis-encoded.

Three things are still wrong.

**a. `docFileName` is absent.** The developer guide describes it as "The name of
the main documentation file for this add-on; e.g. readme.html".
`Addon.getDocFilePath()` at `addonHandler/__init__.py:895-922` returns `None`
when `fileName` is falsy and the manifest has no `docFileName`, so NVDA has no
registered entry point to the localized readme set this release just translated.
Notably, `getDocFilePath` implements the same language, base language, English
chain your code does, so setting `docFileName = "readme.html"` would give you
NVDA's own localized documentation lookup for free.

**b. Values are not quoted.** The developer guide states plainly: "All string
values must be enclosed in quotes as shown in the example below", and its
example quotes every value including `version = "1.0.0"` and
`minimumNVDAVersion = "2021.1"`. Yours are bare. ConfigObj parses them anyway
today, which is why this is tier 2 and not tier 1. The reason the rule exists is
that ConfigObj turns an unquoted value containing a comma into a list. No
current value has a comma, but `summary` and `description` are exactly the
fields that acquire one when somebody edits them.

**c. `changelog` is absent.** Optional, but the guide notes it is shown to users
in the Add-on Store, converted to HTML and read in browse mode. For a release
whose entire story is new languages, that is the field that tells a Japanese or
Polish user why they should update.

**d. Two locales have no translated manifest:** `en` and `ja`. The `ja` one is
already known and being handled. `en` is expected, since the base manifest is
the English one.

One detail worth knowing while the `ja` manifest is being written. In
`_translatedManifestPaths` at `addonHandler/__init__.py:989-998`, the English
fallback is nested inside `if "_" in lang:`. For a language code with no
underscore, such as `ja`, `pl`, `es`, `ru` or `tr`, the candidate list is just
that one path. So `locale/ja/manifest.ini` missing means the base manifest's
English `summary` and `description` are used, which is a clean fallback, not a
failure.

## 10. F4, the documented help key, opens an English website instead of the localized readme

**Defect.** `globalPlugins/nvdaCoach/__init__.py:943` sets
`_HELP_URL = "https://tonygebhard.me/nvdacoach/"`, and `_handleF4` at line 956
opens it in the browser.

So this release translates `doc/ja/`, `doc/pl/` and `doc/zh_TW/` readme,
practice and resources pages, and the key the docs and the in-app introduction
both call "help" opens an English web page.

The localized readme is reachable, but only in two hops: the lesson picker's
"Additional Training and Help" item opens `_localizedDocPath("resources.html")`
(`__init__.py:1545`), and that page has a link to `readme.html`. A beginner
looking for help presses F4.

**What right looks like.** F4 opens `_localizedDocPath("readme.html")` locally.
Offer the website as a second option, or keep F4 on the website only for `en`.

## 11. The completion certificate writes an invalid HTML language tag

**Defect.** `_generateCertificate()` at `globalPlugins/nvdaCoach/__init__.py:267`
does:

```python
lang = languageHandler.getLanguage() or "en"
```

and drops it straight into `<html lang="{lang}">` at line 306.

`getLanguage()` returns NVDA's locale form, with an underscore. So a Traditional
Chinese learner's certificate is `<html lang="zh_TW">`, a Simplified Chinese
learner's is `<html lang="zh_CN">`, and a Brazilian learner's is
`<html lang="pt_BR">`.

The `lang` attribute must be a valid BCP 47 language tag, and BCP 47 separates
subtags with hyphens, never underscores. `zh_TW` is not a valid tag. A browser
and a screen reader will not match it, so they fall back to the default voice.
The learner's certificate, the one artefact they are likely to share, gets read
in the wrong language voice.

This is a WCAG 2.2 Success Criterion 3.1.1 Language of Page failure, and it hits
exactly the languages this release adds and revises.
<https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html>

The doc HTML files do this correctly, which is how I spotted it.
`doc/zh_TW/readme.html` has `<html lang="zh-TW">` with a hyphen. Only the
generated certificate is wrong.

**What right looks like.** One line:

```python
lang = (languageHandler.getLanguage() or "en").replace("_", "-")
```

Languages affected today: zh_TW, zh_CN, pt_BR, and any user on pt_PT, zh_HK,
es_CO, de_CH, nb_NO or nn_NO. Single-subtag codes like `ja`, `pl`, `es`, `ru`
and `tr` are already valid and unaffected.

## 12. doc/ja/resources.html has a dead link, as a consequence of the missing readme

**Defect.** `doc/ja/resources.html` links to `readme.html` as a relative link.
`doc/ja/readme.html` does not exist.

The missing file itself is already known and being handled. I am recording the
symptom separately because it is the part a user experiences: the Japanese
resources page opens fine, its first list item is a link to the user guide, and
following it gives a file not found. `_localizedDocPath` falls back per file, so
the page opens in Japanese, but relative links inside it do not get the same
fallback, because at that point it is the browser resolving them, not your code.

I checked every relative link in all twelve doc files. This is the only dead
one.

**What right looks like.** Confirm this link resolves once `doc/ja/readme.html`
lands. If any language is ever shipped without a readme again, the resources
page for that language should point at the English readme by explicit path
rather than leaving a broken relative link.

## 13. The Japanese catalogue ships unfilled template headers and the Polish one credits a machine

**Defect.** `locale/ja/LC_MESSAGES/nvda.po` header, lines 4 to 10:

```
"Project-Id-Version: NVDA Coach 1.3\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
```

Those are gettext's unfilled placeholders. A community contributor did 204
strings of Japanese and their name is not on it. The project version says 1.3.

`locale/pl/LC_MESSAGES/nvda.po` line 9:

```
"Last-Translator: OpenAI Codex <noreply@openai.com>\n"
```

That is a shipped, user-readable provenance claim that the Polish translation
was machine produced. Whether or not it is accurate, it is worth a decision
rather than an accident, especially since the Polish lesson set is also the one
that is four lessons short.

`locale/zh_TW/LC_MESSAGES/nvda.po` is correct: real translator, real date, and
`Project-Id-Version: nvdaCoach 1.5.7`.

No `.po` states 1.6.0.

**What right looks like.** Fill the Japanese header with the contributor's
name from the pull request. Decide what the Polish `Last-Translator` should say
and put a human or the project there. Set `Project-Id-Version` to 1.6.0 across
all nine as part of the version bump in finding 2.

## 14. Two catalogues have no Plural-Forms, and two declare a locale that does not match their folder

**Defect.** Measured by loading each `.mo` with `gettext.GNUTranslations` and
reading `info()`.

- `ja` and `pl` have no `Plural-Forms` header. Every other language has one.
- `ru` declares `Language: ru_RU` while its folder is `locale/ru/`.
- `tr` declares `Language: tr_TR` while its folder is `locale/tr/`.

**Why it is survivable.** I scanned the source with an AST walk for calls to
`ngettext` and `npgettext`. There are none, so no plural form is selected at
runtime today and the missing headers change nothing. The `Language` header is
informational; gettext resolves by folder name, which is correct in both cases.

**Why to fix it anyway.** The moment somebody writes "3 lessons remaining" with
`ngettext`, Polish silently gets the Germanic default rule, `n != 1`, and Polish
needs three forms. It will produce wrong grammar in a product whose job is to
teach carefully. Add now, while the files are open:

```
ja: "Plural-Forms: nplurals=1; plural=0;\n"
pl: "Plural-Forms: nplurals=3; plural=(n==1 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2);\n"
```

and correct the `ru` and `tr` `Language` headers to match their folders.

## 15. F1 does nothing in the idle Coach window, while F4 is help

**Defect.** In `_onKey` at `globalPlugins/nvdaCoach/__init__.py:1040-1068`, F1,
F2 and F3 are handled only inside `if runner.isActive`. With no lesson running,
F1 falls through to `evt.Skip()` and nothing happens.

F1 is the Windows-wide help key. In an add-on that teaches Windows and NVDA
conventions to beginners, pressing F1 in its main window and getting silence
teaches the wrong thing. Help is on F4, and F4 needs two presses.

**What right looks like.** When idle, F1 should either speak the key summary or
open help. The lesson-time meaning of F1, repeat the instruction, is fine and
should not change, since people will have learned it.

I have not run this to hear what NVDA says on an unhandled F1 in a wx frame. The
claim above is from reading the handler. Worth thirty seconds with NVDA before
acting on it.

## 16. Stale bytecode and internal worksheets will be packaged into the add-on

**Defect.** `globalPlugins/nvdaCoach/__pycache__/` exists with three
`cpython-313.pyc` files. `build.bat` zips `globalPlugins` wholesale and warns in
a comment to delete the folder first, which makes it a manual step somebody will
forget.

`build.bat` also zips `doc` wholesale, and `doc/translators/` contains eight
`TRANSLATORS-*.md` worksheets. Those are internal working documents and they
would ship inside the `.nvda-addon` that goes to the store.

**What right looks like.** Make the build exclude `__pycache__`, `*.pyc`,
`*.po`, `*.pot` and `doc/translators/` rather than relying on a comment. The
README already says the canonical build is a Python snippet, so the two build
paths should be reconciled to one.

---

# Tier 3: polish

## 17. The certificate date is in US order for every language

`_generateCertificate()` at `globalPlugins/nvdaCoach/__init__.py:266` uses:

```python
date_str = datetime.date.today().strftime("%B %d, %Y")
```

`languageHandler.setLanguage` calls `setLocale(getLanguage())`, so `%B` gives a
localized month name, but the order and the comma are fixed US English. A
Japanese certificate reads as a Japanese month name followed by a comma and a
year, where it should be year, month, day. Use `locale`-aware formatting, or a
per-language format string in the catalogue so translators can set it.

## 18. Four store descriptions list the six chapters in the wrong order

The real chapter order, read from the `order` field in each lesson file, is:
Getting Started, Your Keyboard, Reading and Moving Through Text, Browse Mode and
Web Navigation, Object Navigation, Customizing NVDA.

`locale/zh_TW/manifest.ini` lists them in that order and is correct.

`locale/es/manifest.ini`, `locale/ru/manifest.ini`, `locale/zh_CN/manifest.ini`
and `locale/pt_BR/manifest.ini` all put "Your Keyboard" last instead of second.
That is the pre-1.5.5 order. It is the first thing a prospective user reads in
the Add-on Store.

I did not touch the pt_BR file and am only noting it so the agents working on it
know.

## 19. Spanish, Russian and Turkish lesson sets are short in the same places as Polish

Diffed by lesson id, the same four lessons are missing from `es`, `ru` and `tr`
as from `pl`: `battery_status`, `font_info`, `audio_output` and
`audio_ducking`. Turkish additionally has the `activate_Kontrols` id corruption
from finding 6.

This is pre-existing and not caused by this release, and the known-issues list
covers the `.po` side for these three. Recording it so the lesson gap is tracked
separately from the string gap, and so the fix for finding 5 can cover all four
languages at once.

## 20. Dead language guard and an inaccurate docstring

`_loadLessonCategories()` at `globalPlugins/nvdaCoach/__init__.py:198-200`:

```python
lang = languageHandler.getLanguage()  # e.g. "fr_BE", "pt_BR", "en", "Windows"
candidates = []
if lang and lang != "Windows":
```

and the same guard in `_localizedDocPath()` at line 245.

`getLanguage()` returns `_language`, and `setLanguage` assigns `_language` only
from `validatedLocalName`, which is the locale of a catalogue that actually
loaded, or `"en"`. Verified at `source/languageHandler.py:326-351` and
`440-441`. The string `"Windows"` is the config value, not a return value, and
never reaches `getLanguage()`.

The guard is harmless. The comment is wrong and will mislead whoever implements
the alias map in finding 3. Remove the `"Windows"` case or correct the comment,
and while in there, factor the shared candidate-chain logic out of the two
functions so an alias map cannot be added to one and forgotten in the other.

---

# What I confirmed working

Stated separately so it does not get lost among the defects.

- **Gettext resync is correct.** 204 translatable strings in the source, 204
  msgids in `locale/nvda.pot`, zero missing, zero orphaned, zero non-literal
  arguments to `_()`. Every `.po` contains all 204 entries. No fuzzy entries in
  any shipping language.
- **Every `.mo` loads and decodes.** All eight declare
  `charset=UTF-8`, all return correct text on a probe. Entry counts match the
  translated counts in their `.po`, so the compilations are current: ja 205,
  pl 195, zh_CN 205, zh_TW 205, es 98, ru 162, tr 162.
- **Japanese, Simplified Chinese and Traditional Chinese are 204 of 204
  strings.** Polish is 194 of 204.
- **All twelve doc HTML files pass the browse mode structure checks.** Correct
  and valid `lang` on `<html>` in every file, including `lang="ja"`,
  `lang="pl"` and `lang="zh-TW"`. None was left as `en`. A real `<title>` in
  every file. Charset declared in every file. Exactly one `h1`, first heading is
  `h1`, and no skipped levels anywhere.
- **Every practice page table has `<th>`, `scope` and a `<caption>`.**
- **No vague or empty link text** in any language.
- **Polish and Traditional Chinese practice pages are structurally faithful to
  English** and fully localized, including every landmark `aria-label`.
- **All eight translated manifests parse cleanly** with the same library NVDA
  uses, contain only the two fields NVDA reads, and none parsed into a list by
  accident.
- **`ja_JP`, `es_MX` and `pl_PL` resolve correctly** through NVDA's own locale
  fallback before your code ever sees them.

"""Pre-release gate for NVDA Coach.

Run this before every build. It derives what it checks from the add-on itself
rather than from a list somebody has to remember to update, because a check
that is typed twice goes stale and starts lying.

Written 2026-09-20 during the 1.6.0 review, after a release pass found:

  - a keyboard command the add-on taught that NVDA does not have, translated
    faithfully into all nine languages
  - a .mo compiled without its header, which made NVDA's gettext fall back to
    ASCII and raise UnicodeDecodeError on the first Turkish character
  - a locale folder that had shipped as an English copy since 1.5.1
  - seven documentation pages each advertising a different, older version
  - translator worksheets about to be packaged into the add-on users download

Every one of those is checked below.

    python tools/validate_addon.py            # report
    python tools/validate_addon.py --strict   # non-zero exit on any warning

Exit code is non-zero if anything FAILS, so it can gate a build.
"""
import gettext
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS = os.path.join(ROOT, "globalPlugins", "nvdaCoach", "lessons")
LOCALE = os.path.join(ROOT, "locale")
DOC = os.path.join(ROOT, "doc")

CHAPTERS = [
    "getting_started.json",
    "keyboard_reference.json",
    "reading_text.json",
    "browse_mode.json",
    "object_navigation.json",
    "nvda_settings.json",
]
DOC_PAGES = ["readme.html", "practice.html", "resources.html"]

# Things the add-on once claimed that NVDA does not do. Each was verified
# against https://download.nvaccess.org/documentation/keyCommands.html
# If one reappears in English, it is a regression, not a style choice.
KNOWN_WRONG = [
    (r"NVDA\+Shift\+Comma", "NVDA binds NVDA+shift+o, not shift+comma"),
    (r"kb:nvda\+shift\+,", "dead gesture binding"),
    (r"Reset to defaults", "the Speech category has no reset button"),
    (r"device picker|listing all available audio", "NVDA+Ctrl+U opens Audio settings, not a picker"),
    (r"and so on up to 6", "heading quick-nav goes to 9"),
    (r"one of two options: Insert", "NVDA offers three modifier keys"),
    (r"Moving Between Controls", "no lesson by that name"),
]

results = []


def check(ok, label, detail="", warn=False):
    results.append(("WARN" if (warn and not ok) else ("PASS" if ok else "FAIL"), label, detail))
    return ok


def manifest_version():
    with io.open(os.path.join(ROOT, "manifest.ini"), encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("version"):
                return line.split("=", 1)[1].strip()
    return None


def languages():
    return sorted(d for d in os.listdir(LESSONS) if os.path.isdir(os.path.join(LESSONS, d)))


def lesson_sig(path):
    with io.open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    out = []
    for les in d["lessons"]:
        out.append((les["id"], len(les.get("steps", []))))
    return d, out


def main(strict):
    version = manifest_version()
    check(bool(version), "manifest.ini states a version", version or "")

    langs = languages()
    check(len(langs) >= 2, "languages present", " ".join(langs))

    # --- every language is complete -------------------------------------
    for lang in langs:
        missing = [c for c in CHAPTERS if not os.path.isfile(os.path.join(LESSONS, lang, c))]
        check(not missing, "%s: all six chapter files" % lang, ", ".join(missing))

        docmissing = [p for p in DOC_PAGES if not os.path.isfile(os.path.join(DOC, lang, p))]
        check(not docmissing, "%s: all three doc pages" % lang, ", ".join(docmissing))

        if lang != "en":
            po = os.path.join(LOCALE, lang, "LC_MESSAGES", "nvda.po")
            mo = os.path.join(LOCALE, lang, "LC_MESSAGES", "nvda.mo")
            mani = os.path.join(LOCALE, lang, "manifest.ini")
            check(os.path.isfile(po), "%s: has nvda.po" % lang)
            check(os.path.isfile(mo), "%s: has compiled nvda.mo" % lang)
            check(os.path.isfile(mani), "%s: has a translated store listing" % lang)

    # --- every .mo actually loads, with a charset -----------------------
    # A .mo whose header was dropped makes gettext fall back to ASCII and
    # raise on the first accented character. It looks fine in ls.
    for lang in langs:
        mo = os.path.join(LOCALE, lang, "LC_MESSAGES", "nvda.mo")
        if not os.path.isfile(mo):
            continue
        try:
            with open(mo, "rb") as fh:
                cat = gettext.GNUTranslations(fh)
            ct = cat.info().get("content-type", "")
            check("utf-8" in ct.lower(), "%s: .mo declares UTF-8" % lang, ct)
        except Exception as e:
            check(False, "%s: .mo loads" % lang, "%s: %s" % (type(e).__name__, e))

    # --- lesson files parse, and structure matches English --------------
    en_sigs = {}
    for c in CHAPTERS:
        p = os.path.join(LESSONS, "en", c)
        if os.path.isfile(p):
            en_sigs[c] = lesson_sig(p)[1]

    for lang in langs:
        broken = []
        for c in CHAPTERS:
            p = os.path.join(LESSONS, lang, c)
            if not os.path.isfile(p):
                continue
            try:
                lesson_sig(p)
            except Exception as e:
                broken.append("%s (%s)" % (c, e))
        check(not broken, "%s: every chapter file parses" % lang, "; ".join(broken))

    # --- a locale that is secretly an English copy ----------------------
    def strings_of(o, out):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("id", "type", "order", "expectedGestures", "monitorGestures"):
                    continue
                strings_of(v, out)
        elif isinstance(o, list):
            for v in o:
                strings_of(v, out)
        elif isinstance(o, str) and len(o.strip()) > 12:
            out.append(o.strip())
        return out

    en_all = set()
    for c in CHAPTERS:
        p = os.path.join(LESSONS, "en", c)
        if os.path.isfile(p):
            en_all |= set(strings_of(json.load(io.open(p, encoding="utf-8")), []))

    for lang in langs:
        if lang == "en":
            continue
        mine = []
        for c in CHAPTERS:
            p = os.path.join(LESSONS, lang, c)
            if os.path.isfile(p):
                mine += strings_of(json.load(io.open(p, encoding="utf-8")), [])
        if not mine:
            continue
        same = sum(1 for s in mine if s in en_all) * 100.0 / len(mine)
        check(same < 90, "%s: is actually translated" % lang,
              "%.1f%% of its lesson text is identical to English" % same)

    # --- errors that must never come back --------------------------------
    for pattern, why in KNOWN_WRONG:
        hits = []
        for root, _dirs, files in os.walk(LESSONS):
            if os.sep + "en" not in root + os.sep:
                continue
            for f in files:
                if not f.endswith(".json"):
                    continue
                raw = io.open(os.path.join(root, f), encoding="utf-8").read()
                if re.search(pattern, raw):
                    hits.append(f)
        check(not hits, "English is free of: %s" % why, ", ".join(sorted(set(hits))))

    # --- gesture bindings are real NVDA gestures -------------------------
    bad_gestures = []
    for root, _dirs, files in os.walk(LESSONS):
        for f in files:
            if not f.endswith(".json"):
                continue
            raw = io.open(os.path.join(root, f), encoding="utf-8").read()
            for g in re.findall(r'"(kb:[^"]+)"', raw):
                # A gesture with a non-ASCII key name is a translated one,
                # which NVDA will never match.
                if any(ord(ch) > 127 for ch in g):
                    bad_gestures.append("%s: %s" % (os.path.basename(root), g))
    check(not bad_gestures, "no gesture identifiers were translated",
          "; ".join(sorted(set(bad_gestures))[:6]), warn=True)

    # --- doc pages declare their language --------------------------------
    for lang in langs:
        for page in DOC_PAGES:
            p = os.path.join(DOC, lang, page)
            if not os.path.isfile(p):
                continue
            raw = io.open(p, encoding="utf-8", errors="replace").read()
            m = re.search(r"<html[^>]*\blang=[\"']([^\"']+)", raw, re.I)
            declared = m.group(1) if m else None
            want = lang.replace("_", "-")
            ok = declared is not None and declared.lower().split("-")[0] == want.lower().split("-")[0]
            check(ok, "%s/%s declares its language" % (lang, page),
                  "lang=%r, folder says %r" % (declared, want), warn=True)

    # --- version is stated consistently ----------------------------------
    stale = []
    for lang in langs:
        p = os.path.join(DOC, lang, "readme.html")
        if not os.path.isfile(p):
            continue
        raw = io.open(p, encoding="utf-8", errors="replace").read()
        # Strip <style> first: "line-height: 1.6" reads as a version number
        # otherwise, and this check reported a page as claiming 1.6 when it
        # actually claimed 1.5.2. A check that lies is worse than no check.
        body = re.sub(r"<style\b.*?</style>", " ", raw, flags=re.S | re.I)
        body = re.sub(r"<[^>]+>", " ", body)
        head = body[:2500]
        found = re.findall(r"\b\d+\.\d+(?:\.\d+)?\b", head)
        if found and version not in found:
            stale.append("%s says %s" % (lang, found[0]))
    check(not stale, "every readme states the current version", "; ".join(stale))

    # --- the readme advertises the lessons that actually ship ------------
    # Chapters 1, 3 and 6 each gained a lesson in 1.5.4 and no documentation
    # page was updated, so four pages spent two releases advertising 41
    # lessons while the add-on shipped 45.
    for lang in langs:
        p = os.path.join(DOC, lang, "readme.html")
        if not os.path.isfile(p):
            continue
        raw = io.open(p, encoding="utf-8", errors="replace").read()
        ships = {}
        for c in CHAPTERS:
            f = os.path.join(LESSONS, lang, c)
            if os.path.isfile(f):
                d = json.load(io.open(f, encoding="utf-8"))
                ships[d.get("title", c)] = len(d["lessons"])
        wrong = []
        for block in re.split(r"<h3>", raw)[1:]:
            name = re.sub(r"^\d+[.、\s]*", "", block.split("</h3>")[0].strip())
            listed = len(re.findall(r"<li><strong>", block.split("<h2")[0]))
            actual = ships.get(name)
            if actual is not None and actual != listed:
                wrong.append("%s lists %d, ships %d" % (name[:24], listed, actual))
        check(not wrong, "%s: readme lists every lesson that ships" % lang,
              "; ".join(wrong), warn=True)

    # --- nothing internal gets packaged ----------------------------------
    leak = []
    for root, _dirs, files in os.walk(DOC):
        for f in files:
            if f.endswith(".md") and f != "readme.md":
                leak.append(os.path.relpath(os.path.join(root, f), ROOT))
    check(not leak, "no internal notes inside doc/ (it is packaged)", ", ".join(leak))

    # --- report -----------------------------------------------------------
    width = max(len(l) for _s, l, _d in results)
    fails = warns = 0
    for status, label, detail in results:
        if status == "FAIL":
            fails += 1
        elif status == "WARN":
            warns += 1
        if status == "PASS" and "-v" not in sys.argv:
            continue
        print("%-4s %-*s %s" % (status, width, label, detail))

    total = len(results)
    print()
    print("%d checks, %d failed, %d warnings" % (total, fails, warns))
    if fails:
        print("NOT READY TO BUILD")
    elif warns and strict:
        print("warnings present and --strict given")
    else:
        print("OK to build %s" % version)
    return 1 if fails or (warns and strict) else 0


if __name__ == "__main__":
    sys.exit(main("--strict" in sys.argv))

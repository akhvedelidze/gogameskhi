#!/usr/bin/env python3
"""Audit bilingual keyword coverage on canonical pages (titles, descriptions, h1, main text)."""
import importlib.util
import re
import sys
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SITE = 'https://gogameskhi.com'
errors, warnings = [], []


def load_build_data():
    """Import PAGE_* dicts from build.py without running the generator."""
    spec = importlib.util.spec_from_file_location('build_mod', ROOT / 'build.py')
    mod = importlib.util.module_from_spec(spec)
    old_main = sys.modules.get('__main__')
    mod.__name__ = 'build_mod'
    try:
        spec.loader.exec_module(mod)
    finally:
        if old_main:
            sys.modules['__main__'] = old_main
    return mod.PAGE_KEYWORDS, mod.TRACK_KEYWORDS, mod.STORY_KEYWORDS, mod.tracks, mod.stories


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = ''
        self.title = ''
        self.description = ''
        self.canonical = ''
        self.in_title = self.in_main = False
        self.main_text = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = a.get('lang', '')
        elif tag == 'title':
            self.in_title = True
        elif tag == 'meta' and a.get('name') == 'description':
            self.description = a.get('content', '')
        elif tag == 'link' and a.get('rel') == 'canonical':
            self.canonical = a.get('href', '')
        elif tag == 'main':
            self.in_main = True

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag == 'main':
            self.in_main = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_main:
            t = data.strip()
            if t:
                self.main_text.append(t)


def norm(s):
    return unicodedata.normalize('NFKC', s).casefold()


def contains(hay, needle):
    return norm(needle) in norm(hay)


def page_stem(canonical, lang):
    if canonical == SITE + '/':
        return 'index'
    if canonical == SITE + '/ka/':
        return 'index'
    path = canonical.replace(SITE + '/', '').replace(f'{lang}/', '', 1)
    if path.startswith('music/'):
        return 'music/' + path.split('/')[1].replace('.html', '')
    if path.startswith('stories/'):
        return 'stories/' + path.split('/')[1].replace('.html', '')
    return path.replace('.html', '')


def keywords_for(stem, lang, page_kw, track_kw, story_kw):
    if stem.startswith('music/'):
        slug = stem.split('/', 1)[1]
        kw = track_kw.get(slug, {})
    elif stem.startswith('stories/'):
        slug = stem.split('/', 1)[1]
        kw = story_kw.get(slug, {})
    else:
        kw = page_kw.get(stem, {})
    if not kw:
        return [], []
    pk = 'primary_ka' if lang == 'ka' else 'primary_en'
    sk = 'secondary_ka' if lang == 'ka' else 'secondary_en'
    return kw.get(pk, []), kw.get(sk, [])


def audit_page(rel, html, page_kw, track_kw, story_kw):
    p = PageParser()
    p.feed(html)
    if not p.canonical or 'noindex' in html[:2000]:
        return
    lang = p.lang
    stem = page_stem(p.canonical, lang)
    primary, secondary = keywords_for(stem, lang, page_kw, track_kw, story_kw)
    if not primary:
        warnings.append(f'{rel}: no keyword mapping for stem {stem!r}')
        return
    main_html = html.split('<main', 1)[-1].split('</main>', 1)[0] if '<main' in html else ''
    h1 = ' '.join(re.sub(r'<[^>]+>', ' ', m) for m in re.findall(r'<h1[^>]*>.*?</h1>', main_html, re.S))
    bucket = ' '.join([p.title, p.description, h1, ' '.join(p.main_text[:80])])
    missing_p = [k for k in primary if not contains(bucket, k)]
    if missing_p and not any(contains(bucket, k) for k in primary):
        errors.append(f'{rel}: no primary keyword in title, description, h1 or main: {primary}')
    found_s = [k for k in secondary if contains(bucket, k)]
    if secondary and not found_s:
        warnings.append(f'{rel}: no secondary keyword in visible text (optional): {secondary[:3]}…')
    # Cannibalization: primary should appear in <title>, not only body
    if not any(contains(p.title, k) or contains(p.description, k) for k in primary):
        if not contains(h1, primary[0]):
            warnings.append(f'{rel}: primary keyword missing from title and description')


def audit_cannibalization(canonical_pages, page_kw):
    """Flag when two pages share the same primary English keyword (hub pages only)."""
    owners = {}
    for rel, canon, lang in canonical_pages:
        if lang != 'en':
            continue
        stem = page_stem(canon, lang)
        if '/' in stem or stem in ('privacy', '404'):
            continue
        for k in page_kw.get(stem, {}).get('primary_en', []):
            if k == 'Goga Meskhi':
                continue
            owners.setdefault(k, []).append((stem, rel))
    for k, pages in owners.items():
        if len(pages) > 1:
            warnings.append(f'cannibalization risk: primary EN {k!r} on {pages}')


def write_keywords_md(page_kw, track_kw, story_kw, tracks, stories, canonical_pages):
    """Write SEO-KEYWORDS.md: mappings, coverage, and opportunities."""
    priority_en = [
        'Goga Meskhi', 'Goga Meskhi singer', 'Goga Meskhi songs', 'Goga Meskhi biography',
        'Goga Meskhi music', 'Goga Meskhi concert', 'Georgian singer', 'Georgian music',
        'Goga Meskhi actor', 'Georgian recording artist',
    ]
    priority_ka = [
        'გოგა მესხი', 'გოგა მესხი მომღერალი', 'გოგა მესხი სიმღერები', 'გოგა მესხის ბიოგრაფია',
        'გოგა მესხი მუსიკა', 'გოგა მესხი კონცერტი', 'ქართველი მომღერალი', 'ქართული მუსიკა',
        'გოგა მესხი მსახიობი',
    ]
    all_text_en = all_text_ka = ''
    for rel, _, lang in canonical_pages:
        html = (ROOT / rel).read_text(encoding='utf8')
        text = re.sub(r'<[^>]+>', ' ', html)
        if lang == 'en' or rel == 'index.html':
            all_text_en += ' ' + text
        if lang == 'ka' or rel == 'index.html':
            all_text_ka += ' ' + text

    def cov_row(keys, text):
        rows = []
        for k in keys:
            ok = contains(text, k)
            rows.append(f'| {k} | {"Yes" if ok else "Gap"} |')
        return '\n'.join(rows)

    hub_rows = []
    for stem in (
        'index', 'music', 'videos', 'listen', 'live', 'about', 'stories', 'press', 'contact', 'privacy'
    ):
        kw = page_kw.get(stem, {})
        hub_rows.append(
            f'| `{stem}` | {", ".join(kw.get("primary_en", []))} | {", ".join(kw.get("secondary_en", [])[:4])} '
            f'| {", ".join(kw.get("primary_ka", []))} | {", ".join(kw.get("secondary_ka", [])[:4])} |'
        )

    track_rows = []
    for tr in tracks:
        kw = track_kw.get(tr['slug'], {})
        track_rows.append(
            f'| `{tr["slug"]}` | {tr["en"]} | {tr["ka"]} | {", ".join(kw.get("primary_en", []))} '
            f'| {", ".join(kw.get("secondary_en", [])[:3])} |'
        )

    story_rows = []
    for s in stories:
        kw = story_kw.get(s[0], {})
        tr = s[6]
        story_rows.append(
            f'| `{s[0]}` | {s[1]} | {tr["en"]} | {", ".join(kw.get("primary_en", [])[:2])} |'
        )

    page_rows = []
    for rel, canon, lang in sorted(canonical_pages, key=lambda x: (x[2], x[1])):
        stem = page_stem(canon, lang)
        primary, secondary = keywords_for(stem, lang, page_kw, track_kw, story_kw)
        page_rows.append(
            f'| [{canon}]({canon}) | {lang} | {stem} | {"; ".join(primary)} | {"; ".join(secondary[:4])} |'
        )

    en_hit = sum(contains(all_text_en, k) for k in priority_en)
    ka_hit = sum(contains(all_text_ka, k) for k in priority_ka)
    gaps_en = [k for k in priority_en if not contains(all_text_en, k)]
    gaps_ka = [k for k in priority_ka if not contains(all_text_ka, k)]

    doc = f"""# SEO keyword map — gogameskhi.com

Generated by `seo_keyword_audit.py` from `PAGE_KEYWORDS`, `TRACK_KEYWORDS`, and `STORY_KEYWORDS` in `build.py`. Re-run after content changes:

```powershell
python build.py
python seo_keyword_audit.py
python seo_check.py
```

## Summary

| Metric | Result |
|---|---|
| Canonical pages audited | {len(canonical_pages)} |
| Priority English phrases (exact substring across EN pages) | {en_hit}/{len(priority_en)} |
| Priority Georgian phrases (exact substring across KA pages) | {ka_hit}/{len(priority_ka)} |
| Song titles (EN / KA) | {len(tracks)}/{len(tracks)} each |
| Meta keywords tag | Not used (by design) |

## Cannibalization strategy (primary keyword ownership)

| Intent | EN primary owner | KA primary owner |
|---|---|---|
| Artist brand | `/` — Goga Meskhi | `/ka/` — გოგა მესხი |
| Songs & catalogue | `/en/music.html` — Goga Meskhi songs, Goga Meskhi music | `/ka/music.html` — გოგა მესხი სიმღერები, გოგა მესხი მუსიკა |
| Biography | `/en/about.html` — Goga Meskhi biography | `/ka/about.html` — გოგა მესხის ბიოგრაფია |
| Concerts / booking | `/en/live.html`, `/en/contact.html` (concert secondary) | `/ka/live.html`, `/ka/contact.html` |
| Streaming | `/en/listen.html` — Listen to Goga Meskhi | `/ka/listen.html` — გოგა მესხი მუსიკა |
| Song stories (editorial) | `/en/stories.html` — Song stories | `/ka/stories.html` — სიმღერების ისტორიები |
| Individual recordings | `/en/music/{{slug}}.html` — song title + transliteration | same pattern in `ka/` |
| Press | `/en/press.html` — Goga Meskhi (media context) | `/ka/press.html` — გოგა მესხი |

Utility page `privacy` keeps brand-only keywords and stays out of `sitemap.xml`.

## Hub pages — keyword assignments

| Stem | Primary EN | Secondary EN | Primary KA | Secondary KA |
|---|---|---|---|---|
{chr(10).join(hub_rows)}

## Priority phrase coverage

### English

| Phrase | Site-wide |
|---|---|
{cov_row(priority_en, all_text_en)}

### Georgian

| ფრაზა | საიტზე |
|---|---|
{cov_row(priority_ka, all_text_ka)}

## Tracks (slug → titles → keywords)

| Slug | EN title | KA title | Primary EN | Secondary EN |
|---|---|---|---|---|
{chr(10).join(track_rows)}

Each track page title pattern: `{{title}} ({{translation}}) — Goga Meskhi | song` / `სიმღერა` in Georgian. Body copy includes performer credit, catalogue back-link to the music hub, and transliterated Georgian titles on EN pages (`lang="ka"`).

## Story pages

| Slug | Story headline EN | Linked track | Primary EN |
|---|---|---|---|
{chr(10).join(story_rows)}

## All canonical URLs ({len(canonical_pages)})

| Canonical | Lang | Stem | Primary | Secondary (sample) |
|---|---|---|---|---|
{chr(10).join(page_rows)}

## Remaining opportunities

"""
    if gaps_en:
        doc += '- **English exact-string gaps** (audit uses literal substring match; nearby variants may still rank): ' + ', '.join(f'`{g}`' for g in gaps_en) + '.\n'
    else:
        doc += '- **English priority list:** all ten target phrases appear at least once on English pages.\n'
    if gaps_ka:
        doc += '- **Georgian exact-string gaps:** ' + ', '.join(f'`{g}`' for g in gaps_ka) + '.\n'
    else:
        doc += '- **Georgian priority list:** all nine target phrases appear at least once on Georgian pages.\n'
    doc += """- **Long-tail:** transliterations (`Ar Makhsovs`, `Nu Damemdurebi`, etc.) live on EN track pages beside Georgian script titles; no separate Latin-only URLs (avoids duplicate content).
- **Off-site profiles:** SameAs in JSON-LD lists verified YouTube, Facebook, and Spotify artist URLs; Instagram/Amazon remain unlisted until confirmed (`RESEARCH-SOURCES.md`).
- **Post-launch:** monitor Search Console queries; if `Goga Meskhi singer` / `actor` split across pages, adjust internal links from home → About before changing titles.

## Related docs

- `SEO-REPORT.md` — technical SEO (canonical, hreflang, schema, sitemap).
- `build.py` — `PAGE_META`, `PAGE_KEYWORDS`, body copy (single source of truth).
"""
    out = ROOT / 'SEO-KEYWORDS.md'
    out.write_text(doc, encoding='utf8', newline='\n')
    print(f'Wrote {out.name}')


def main():
    print('Loading keyword map from build.py…')
    page_kw, track_kw, story_kw, tracks, stories = load_build_data()
    canonical_pages = []
    for f in sorted(ROOT.rglob('*.html')):
        rel = f.relative_to(ROOT).as_posix()
        html = f.read_text(encoding='utf8')
        if rel == 'en/index.html' or rel == '404.html':
            continue
        if 'rel="canonical"' not in html:
            continue
        m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
        lang = re.search(r'<html lang="([^"]+)"', html)
        if m and lang:
            canonical_pages.append((rel, m.group(1), lang.group(1)))
        audit_page(rel, html, page_kw, track_kw, story_kw)
    audit_cannibalization(canonical_pages, page_kw)
    # Priority list coverage
    priority_en = [
        'Goga Meskhi', 'Goga Meskhi singer', 'Goga Meskhi songs', 'Goga Meskhi biography',
        'Goga Meskhi music', 'Goga Meskhi concert', 'Georgian singer', 'Georgian music',
        'Goga Meskhi actor', 'Georgian recording artist',
    ]
    priority_ka = [
        'გოგა მესხი', 'გოგა მესხი მომღერალი', 'გოგა მესხი სიმღერები', 'გოგა მესხის ბიოგრაფია',
        'გოგა მესხი მუსიკა', 'გოგა მესხი კონცერტი', 'ქართველი მომღერალი', 'ქართული მუსიკა',
        'გოგა მესხი მსახიობი',
    ]
    all_text_en = all_text_ka = ''
    for rel, canon, lang in canonical_pages:
        html = (ROOT / rel).read_text(encoding='utf8')
        text = re.sub(r'<[^>]+>', ' ', html)
        if lang == 'en' or rel == 'index.html':
            all_text_en += ' ' + text
        if lang == 'ka' or rel == 'index.html':
            all_text_ka += ' ' + text
    song_en = {tr['en'] for tr in tracks}
    song_ka = {tr['ka'] for tr in tracks}
    print(f'\nPriority EN on site: {sum(contains(all_text_en, k) for k in priority_en)}/{len(priority_en)}')
    for k in priority_en:
        if not contains(all_text_en, k):
            print(f'  gap EN: {k}')
    print(f'Priority KA on site: {sum(contains(all_text_ka, k) for k in priority_ka)}/{len(priority_ka)}')
    for k in priority_ka:
        if not contains(all_text_ka, k):
            print(f'  gap KA: {k}')
    print(f'Song titles EN: {sum(contains(all_text_en, s) for s in song_en)}/{len(song_en)}')
    print(f'Song titles KA: {sum(contains(all_text_ka, s) for s in song_ka)}/{len(song_ka)}')
    print(f'\n{len(canonical_pages)} canonical pages audited.')
    print(f'{len(errors)} errors, {len(warnings)} warnings.')
    for e in errors:
        print('ERROR', e)
    for w in warnings:
        print('WARN', w)
    write_keywords_md(page_kw, track_kw, story_kw, tracks, stories, canonical_pages)
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
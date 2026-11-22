"""Technical SEO audit of the generated site. Standard library only.

    python seo_check.py              check every page, robots.txt, sitemap.xml and CNAME
    python seo_check.py --external   also request every external link and image

Exits with status 1 if any check fails. Run it after `python build.py`.
"""
import json
import posixpath
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent
SITE = 'https://gogameskhi.com'
PERSON_ID = SITE + '/#person'
WEBSITE_ID = SITE + '/#website'
DUPLICATES = {'en/index.html'}      # same content as the root homepage; canonical points at the root
NOINDEX = {'404.html'}              # utility pages that must stay out of the index
UTILITY = {'en/privacy.html', 'ka/privacy.html'}   # indexable, but not listed in the sitemap
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}

errors, warnings = [], []


def error(page, message):
    errors.append(f'{page}: {message}')


def warn(page, message):
    warnings.append(f'{page}: {message}')


class Page(HTMLParser):
    """Collects the parts of one HTML file that the checks need."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lang = None
        self.title = ''
        self.meta = {}            # name or property -> content
        self.canonical = []
        self.hreflang = {}
        self.jsonld = []
        self.headings = []        # (level, text)
        self.images = []          # attribute dicts
        self.links = []           # (href, text, aria-label)
        self.resources = []       # local CSS, JS and icon paths
        self.ids = set()
        self._capture = None      # element whose text is being collected
        self._text = []
        self._link = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'html':
            self.lang = a.get('lang')
        elif tag == 'meta':
            key = a.get('name') or a.get('property')
            if key:
                if key in self.meta:
                    self.meta.setdefault('__repeated__', []).append(key)
                self.meta[key] = a.get('content', '')
        elif tag == 'link':
            rel = a.get('rel', '')
            if rel == 'canonical':
                self.canonical.append(a.get('href', ''))
            elif rel == 'alternate' and a.get('hreflang'):
                if a['hreflang'] in self.hreflang:
                    self.meta.setdefault('__repeated__', []).append('hreflang ' + a['hreflang'])
                self.hreflang[a['hreflang']] = a.get('href', '')
            elif rel in ('stylesheet', 'icon', 'apple-touch-icon') and not a.get('href', '').startswith('http'):
                self.resources.append(a.get('href', ''))
        elif tag == 'script':
            if a.get('type') == 'application/ld+json':
                self._capture, self._text = 'jsonld', []
            elif a.get('src') and not a['src'].startswith('http'):
                self.resources.append(a['src'])
        elif tag == 'title':
            self._capture, self._text = 'title', []
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            self._capture, self._text = tag, []
        elif tag == 'img':
            self.images.append(a)
            if self._link is not None:
                self._link[1].append(a.get('alt', ''))
        elif tag == 'a' and 'href' in a:
            self._link = [a['href'], [], a.get('aria-label', '')]
        elif tag == 'br' and self._capture:
            self._text.append(' ')

    def handle_endtag(self, tag):
        if tag == 'a' and self._link is not None:
            self.links.append((self._link[0], ' '.join(''.join(self._link[1]).split()), self._link[2]))
            self._link = None
        if self._capture == 'jsonld' and tag == 'script':
            self.jsonld.append(''.join(self._text))
            self._capture = None
        elif self._capture == 'title' and tag == 'title':
            self.title = ''.join(self._text).strip()
            self._capture = None
        elif self._capture == tag and tag.startswith('h'):
            self.headings.append((int(tag[1]), ' '.join(''.join(self._text).split())))
            self._capture = None

    def handle_data(self, data):
        if self._capture:
            self._text.append(data)
        if self._link is not None:
            self._link[1].append(data)


def expected_canonical(rel):
    if rel in ('index.html', 'en/index.html'):
        return SITE + '/'
    if rel.endswith('/index.html'):
        return f'{SITE}/{rel[:-len("index.html")]}'
    return f'{SITE}/{rel}'


def url_to_file(url):
    """Local file that an absolute site URL is served from, or None for other hosts."""
    if not url.startswith(SITE + '/'):
        return None
    path = url[len(SITE) + 1:].split('#')[0]
    return path + 'index.html' if path == '' or path.endswith('/') else path


def resolve(rel, href):
    """Local file an internal href points at, relative to the page that contains it."""
    path = href.split('#')[0].split('?')[0]
    if path.startswith('/'):
        target = posixpath.normpath(path.lstrip('/')) if path != '/' else '.'
    else:
        target = posixpath.normpath(posixpath.join(posixpath.dirname(rel), path))
    if path.endswith('/') or target == '.':
        target = 'index.html' if target == '.' else target + '/index.html'
    return target


def walk(node):
    """Every dict nested inside a JSON-LD structure."""
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from walk(item)


def check_jsonld(rel, page, canonical):
    """Returns the Person node so its consistency can be compared across pages."""
    if not page.jsonld:
        error(rel, 'no JSON-LD structured data')
        return None
    nodes = []
    for raw in page.jsonld:
        try:
            data = json.loads(raw)
        except ValueError as exc:
            error(rel, f'JSON-LD does not parse: {exc}')
            return None
        if data.get('@context') != 'https://schema.org':
            error(rel, 'JSON-LD @context is not https://schema.org')
        nodes += data.get('@graph', [data])
    by_id = {n['@id']: n for n in nodes if '@id' in n}
    types = [n.get('@type') for n in nodes]

    person = by_id.get(PERSON_ID)
    if not person or person.get('@type') != 'Person':
        error(rel, f'no Person node with @id {PERSON_ID}')
    else:
        for key in ('name', 'alternateName', 'sameAs', 'url'):
            if not person.get(key):
                error(rel, f'Person is missing {key}')
        if {person.get('name'), person.get('alternateName')} != {'Goga Meskhi', 'გოგა მესხი'}:
            error(rel, 'Person must carry both the English and the Georgian name')
    if WEBSITE_ID not in by_id:
        error(rel, 'no WebSite node')

    pages = [n for n in nodes if n.get('@id') == canonical + '#webpage']
    if len(pages) != 1:
        error(rel, 'expected exactly one WebPage node for this URL')
    else:
        wp = pages[0]
        if wp.get('url') != canonical:
            error(rel, 'WebPage url differs from the canonical URL')
        if wp.get('inLanguage') != page.lang:
            error(rel, 'WebPage inLanguage differs from <html lang>')
        if wp.get('name') != page.title:
            error(rel, 'WebPage name differs from <title>')
        if rel.endswith('/about.html') and (wp.get('@type') != 'ProfilePage' or wp.get('mainEntity') != {'@id': PERSON_ID}):
            error(rel, 'the About page must be a ProfilePage whose mainEntity is the Person')

    crumbs = [n for n in nodes if n.get('@type') == 'BreadcrumbList']
    is_home = canonical in (SITE + '/', SITE + '/ka/')
    if is_home and crumbs:
        error(rel, 'homepage should not have a breadcrumb')
    if not is_home:
        if len(crumbs) != 1:
            error(rel, 'expected one BreadcrumbList')
        else:
            items = crumbs[0].get('itemListElement', [])
            if [i.get('position') for i in items] != list(range(1, len(items) + 1)):
                error(rel, 'breadcrumb positions are not 1..n')
            if not items or items[-1].get('item') != canonical:
                error(rel, 'last breadcrumb is not this page')
            for item in items:
                target = url_to_file(item.get('item', ''))
                if not item.get('name') or target is None or not (ROOT / target).is_file():
                    error(rel, f'breadcrumb item is not a page of this site: {item.get("item")}')

    # Every {"@id": ...} reference must point at a node defined on the same page.
    for node in walk(nodes):
        if set(node) == {'@id'} and node['@id'] not in by_id:
            error(rel, f'JSON-LD reference to undefined node {node["@id"]}')

    for video in (n for n in nodes if n.get('@type') == 'VideoObject'):
        for key in ('name', 'description', 'thumbnailUrl', 'uploadDate', 'embedUrl'):
            if not video.get(key):
                error(rel, f'VideoObject is missing {key}')
        if not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d[+-]\d\d:\d\d', video.get('uploadDate', '')):
            error(rel, 'VideoObject uploadDate must be ISO 8601 with a timezone')
        if not re.fullmatch(r'PT(\d+H)?(\d+M)?(\d+S)?', video.get('duration', 'PT0S')):
            error(rel, 'VideoObject duration is not ISO 8601')
    for rec in (n for n in nodes if n.get('@type') == 'MusicRecording'):
        artists = rec.get('byArtist')
        artists = artists if isinstance(artists, list) else [artists]
        if {'@id': PERSON_ID} not in artists:
            error(rel, 'MusicRecording byArtist does not reference the Person')
    if '/music/' in rel and 'MusicRecording' not in types:
        error(rel, 'track page has no MusicRecording')
    for listing in (n for n in nodes if n.get('@type') == 'ItemList'):
        for item in listing.get('itemListElement', []):
            target = url_to_file(item.get('url', ''))
            if target is None or not (ROOT / target).is_file():
                error(rel, f'ItemList entry is not a page of this site: {item.get("url")}')
    return person


def check_page(rel, page, external):
    in_ka = rel.startswith('ka/')
    if page.lang != ('ka' if in_ka else 'en'):
        error(rel, f'<html lang="{page.lang}"> does not match the page language')
    if not page.title:
        error(rel, 'missing <title>')
    elif not 10 <= len(page.title) <= 70:
        warn(rel, f'title is {len(page.title)} characters')
    desc = page.meta.get('description', '')
    if not desc:
        error(rel, 'missing meta description')
    elif not 50 <= len(desc) <= 300:
        warn(rel, f'meta description is {len(desc)} characters')
    for key in page.meta.get('__repeated__', []):
        error(rel, f'{key} appears more than once')
    if 'viewport' not in page.meta:
        error(rel, 'missing viewport meta')

    robots = page.meta.get('robots', '')
    if rel in NOINDEX:
        if 'noindex' not in robots:
            error(rel, 'utility page must be noindex')
        if page.canonical or page.hreflang:
            error(rel, 'noindex page must not declare canonical or hreflang')
    else:
        if 'noindex' in robots or 'nofollow' in robots:
            error(rel, f'page is blocked from indexing: robots="{robots}"')
        canonical = expected_canonical(rel)
        if page.canonical != [canonical]:
            error(rel, f'canonical is {page.canonical}, expected {canonical}')
        if rel in DUPLICATES:
            if page.hreflang:
                error(rel, 'duplicate page must not carry hreflang')
        else:
            if set(page.hreflang) != {'ka', 'en', 'x-default'}:
                error(rel, f'hreflang set is {sorted(page.hreflang)}')
            elif page.hreflang['ka' if in_ka else 'en'] != canonical:
                error(rel, 'hreflang for this language is not self-referencing')
            elif page.hreflang['x-default'] != page.hreflang['en']:
                error(rel, 'x-default does not point at the English page')
            if in_ka and not page.hreflang.get('ka', '').startswith(SITE + '/ka/'):
                error(rel, 'Georgian page is not under /ka/')

        # Open Graph and X/Twitter cards
        for key in ('og:site_name', 'og:type', 'og:title', 'og:description', 'og:url', 'og:locale', 'og:image',
                    'og:image:width', 'og:image:height', 'og:image:alt', 'twitter:card', 'twitter:title',
                    'twitter:description', 'twitter:image', 'twitter:image:alt'):
            if not page.meta.get(key):
                error(rel, f'missing {key}')
        if page.meta.get('og:url') != canonical:
            error(rel, 'og:url differs from the canonical URL')
        if page.meta.get('og:title') != page.title or page.meta.get('twitter:title') != page.title:
            error(rel, 'social title differs from <title>')
        if page.meta.get('og:locale') != ('ka_GE' if in_ka else 'en_US'):
            error(rel, 'og:locale does not match the page language')
        for key in ('og:image', 'twitter:image'):
            image = page.meta.get(key, '')
            if not image.startswith('https://'):
                error(rel, f'{key} is not an absolute https URL')
            local = url_to_file(image)
            if local and not (ROOT / local).is_file():
                error(rel, f'{key} file does not exist: {local}')
            elif not local:
                external.setdefault(image, rel)
        person = check_jsonld(rel, page, canonical)
        page.person = person

    # Headings
    levels = [level for level, _ in page.headings]
    if levels.count(1) != 1:
        error(rel, f'{levels.count(1)} <h1> elements (expected 1)')
    elif levels[0] != 1:
        error(rel, 'the first heading is not the <h1>')
    for (prev, _), (level, text) in zip(page.headings, page.headings[1:]):
        if level > prev + 1:
            error(rel, f'heading level jumps from h{prev} to h{level} at "{text}"')
    for level, text in page.headings:
        if not text:
            error(rel, f'empty <h{level}>')

    # Images
    for image in page.images:
        src = image.get('src', '')
        if not image.get('alt', '').strip():
            error(rel, f'image without alt text: {src}')
        if src.startswith('http://'):
            error(rel, f'image is not served over https: {src}')
        if src.endswith('/hqdefault.jpg') and (image.get('width'), image.get('height')) != ('480', '360'):
            error(rel, f'thumbnail without width/height: {src}')
        if image.get('loading') not in ('lazy', 'eager'):
            error(rel, f'image without a loading attribute: {src}')
        if src.startswith('http'):
            external.setdefault(src, rel)
    if sum(1 for i in page.images if i.get('fetchpriority') == 'high') > 1:
        error(rel, 'more than one image is marked fetchpriority="high"')

    # Links
    for href, text, label in page.links:
        if not (text or label):
            error(rel, f'link without text: {href}')
        if href.startswith(('http://', 'https://')):
            if href.startswith('http://'):
                error(rel, f'external link is not https: {href}')
            if href.startswith(SITE):
                error(rel, f'internal link written as an absolute URL: {href}')
            external.setdefault(href.split('#')[0], rel)
        elif href.startswith('#'):
            if href[1:] not in page.ids:
                error(rel, f'fragment link without a target: {href}')
        elif href.startswith(('mailto:', 'tel:')):
            pass
        else:
            target = resolve(rel, href)
            if not (ROOT / target).is_file():
                error(rel, f'broken internal link: {href}')
            elif target in DUPLICATES or href.split('#')[0].endswith('index.html'):
                error(rel, f'internal link points at a non-canonical URL: {href}')
    for res in page.resources:
        if not (ROOT / resolve(rel, res)).is_file():
            error(rel, f'missing file: {res}')


def check_site(pages):
    indexable = {rel: p for rel, p in pages.items() if rel not in NOINDEX and rel not in DUPLICATES}

    # Titles and descriptions must be unique across canonical pages.
    for label, getter in (('title', lambda p: p.title), ('meta description', lambda p: p.meta.get('description', ''))):
        seen = {}
        for rel, page in indexable.items():
            seen.setdefault(getter(page), []).append(rel)
        for value, rels in seen.items():
            if len(rels) > 1:
                error(', '.join(rels), f'duplicate {label}: "{value[:70]}"')

    # hreflang must be reciprocal: every alternate lists the same set of URLs.
    for rel, page in indexable.items():
        for lang, url in page.hreflang.items():
            target = url_to_file(url)
            if target is None or target not in indexable:
                error(rel, f'hreflang {lang} points at a URL that is not an indexable page: {url}')
            elif indexable[target].hreflang != page.hreflang:
                error(rel, f'hreflang is not reciprocal with {target}')
            elif indexable[target].canonical != [url]:
                error(rel, f'hreflang {lang} points at a non-canonical URL: {url}')

    # The Person entity must be identical on every page of the same language.
    for lang in ('en', 'ka'):
        people = {json.dumps(p.person, sort_keys=True, ensure_ascii=False)
                  for rel, p in indexable.items() if rel.startswith('ka/') == (lang == 'ka') and getattr(p, 'person', None)}
        if len(people) != 1:
            error(f'{lang} pages', f'Person node differs between pages ({len(people)} variants)')
    same_as = {json.dumps(p.person.get('sameAs')) for p in indexable.values() if getattr(p, 'person', None)}
    if len(same_as) != 1:
        error('site', 'Person sameAs differs between pages')

    # sitemap.xml
    path = ROOT / 'sitemap.xml'
    if not path.is_file():
        error('sitemap.xml', 'file is missing')
    else:
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9', 'x': 'http://www.w3.org/1999/xhtml'}
        entries = {}
        for url in ET.parse(path).getroot().findall('s:url', ns):
            loc = url.find('s:loc', ns).text
            if loc in entries:
                error('sitemap.xml', f'duplicate entry {loc}')
            entries[loc] = {link.get('hreflang'): link.get('href') for link in url.findall('x:link', ns)}
        expected = {p.canonical[0]: p.hreflang for rel, p in indexable.items() if rel not in UTILITY and p.canonical}
        for loc in sorted(set(expected) - set(entries)):
            error('sitemap.xml', f'canonical page is missing: {loc}')
        for loc in sorted(set(entries) - set(expected)):
            error('sitemap.xml', f'lists a URL that is not a canonical public page: {loc}')
        for loc in set(entries) & set(expected):
            if entries[loc] != expected[loc]:
                error('sitemap.xml', f'language alternates differ from the page for {loc}')

    # robots.txt
    path = ROOT / 'robots.txt'
    if not path.is_file():
        error('robots.txt', 'file is missing')
    else:
        lines = [line.strip() for line in path.read_text(encoding='utf8').splitlines()]
        if f'Sitemap: {SITE}/sitemap.xml' not in lines:
            error('robots.txt', 'does not reference the sitemap')
        if 'Disallow: /' in lines:
            error('robots.txt', 'blocks the whole site')
        blocked = [line.split(':', 1)[1].strip() for line in lines if line.startswith('Disallow:')]
        for rel in indexable:
            if any(rule and ('/' + rel).startswith(rule.rstrip('$*')) and '*' not in rule for rule in blocked):
                error('robots.txt', f'blocks the page /{rel}')

    # GitHub Pages and custom domain
    cname = ROOT / 'CNAME'
    if not cname.is_file() or cname.read_text(encoding='utf8').strip() != SITE.split('//')[1]:
        error('CNAME', f'must contain {SITE.split("//")[1]}')
    if not (ROOT / '.nojekyll').is_file():
        error('.nojekyll', 'file is missing')
    if not (ROOT / '404.html').is_file():
        error('404.html', 'file is missing')


def check_external(urls):
    """Request every external URL. Some publishers refuse scripted requests; those are reported separately."""
    agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'
    print(f'\nRequesting {len(urls)} external URLs...')
    for url, rel in sorted(urls.items()):
        status = 0
        try:
            request = urllib.request.Request(url, headers={'User-Agent': agent, 'Accept-Language': 'en-US,en;q=0.9'})
            with urllib.request.urlopen(request, timeout=25) as response:
                status = response.status
        except urllib.error.HTTPError as exc:
            status = exc.code
        except Exception as exc:  # DNS failure, timeout, TLS error
            status = type(exc).__name__
        if status == 200:
            continue
        # Facebook answers 400 to anything that is not a real browser.
        refused = status in (401, 403, 429, 999) or (status == 400 and urlsplit(url).netloc.endswith('facebook.com'))
        if refused:
            warn(rel, f'{status} to a scripted request (check in a browser): {url}')
        else:
            error(rel, f'external URL returned {status}: {url}')


def main():
    pages, external = {}, {}
    for path in sorted(ROOT.rglob('*.html')):
        rel = path.relative_to(ROOT).as_posix()
        page = Page()
        page.feed(path.read_text(encoding='utf8'))
        pages[rel] = page
    for rel, page in pages.items():
        check_page(rel, page, external)
    check_site(pages)
    if '--external' in sys.argv:
        check_external(external)

    for line in warnings:
        print('WARN ', line)
    for line in errors:
        print('ERROR', line)
    indexable = len(pages) - len(NOINDEX) - len(DUPLICATES)
    print(f'\n{len(pages)} HTML files, {indexable} canonical pages, {len(external)} external URLs referenced.')
    print(f'{len(errors)} errors, {len(warnings)} warnings.')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())

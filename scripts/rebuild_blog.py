#!/usr/bin/env python3
"""Rebuild blog/index.html and the blog entries in sitemap.xml from whatever
post folders currently exist under blog/. Run after publishing a batch."""
import io, os, re, json, html, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_RULES = [
 (r'drain|clog|jet|snak|disposal', ['plumber-snaking-kitchen-drain.png',
   'plumber-clearing-drain-line.png', 'plumber-inspecting-sink-trap.png',
   'plumber-replacing-sink-p-trap.png', 'crawl-space-drain-line-repair.png']),
 (r'sewer|lateral|root|camera', ['sewer-line-excavation-yard.jpg',
   'new-sewer-pipe-installation-trench.jpg', 'sewer-cleanout-risers-installed.png',
   'trenchless-sewer-yard-restoration.png', 'underslab-sewer-rough-in-stakes.jpg']),
 (r'repipe|pex|cpvc|copper|galvanized|polybutylene|pinhole|pipe-burst|burst|cast-iron',
  ['repiped-copper-water-lines.jpg', 'copper-manifold-brazing-repipe.jpg',
   'copper-repipe-manifold-wall.png', 'plumber-cutting-pex-pipe.png',
   'plumber-repairing-leaking-pipe.png', 'large-diameter-pipe-fabrication-shop.jpg']),
 (r'water-heater|tankless|anode|descal|gas-line', ['plumber-servicing-water-heater.png',
   'water-heater-recirculation-piping.png', 'gas-line-welding-water-heater-install.jpg']),
 (r'slab|leak|meter|water-bill|irrigation', ['plumber-checking-shower-valve.png',
   'plumber-repairing-under-sink-plumbing.jpg', 'plumber-tightening-sink-drain-pipe.jpg',
   'underslab-sewer-rough-in-stakes.jpg']),
 (r'toilet|flange', ['plumber-sealing-toilet-base.jpg', 'plumber-working-under-bathroom-sink.png']),
 (r'faucet|fixture|shower-valve|angle-stop', ['smiling-plumber-installing-faucet.jpg',
   'plumber-wrench-on-shower-fitting.png', 'plumber-tightening-pipe-fitting.png']),
 (r'bathroom|remodel|kitchen', ['plumber-working-under-bathroom-sink.png',
   'plumber-under-kitchen-sink.png', 'plumber-repairing-under-sink-plumbing.jpg']),
 (r'softener|filtration|osmosis|well-water|hard-water|backflow',
  ['water-heater-recirculation-piping.png', 'plumber-welding-pipe-spool-fabrication.jpg',
   'large-diameter-pipe-fabrication-shop.jpg']),
 (r'pressure|regulator', ['plumber-tightening-pipe-fitting.png',
   'plumber-wrench-on-shower-fitting.png']),
]
FALLBACK = ['plumber-fixing-pipes-boynton-beach.png', 'plumber-under-kitchen-sink.png',
            'plumber-inspecting-sink-trap.png', 'plumber-tightening-pipe-fitting.png']
def pick_image(slug):
    h = sum(ord(c) for c in slug)
    for pat, imgs in IMG_RULES:
        if re.search(pat, slug): return imgs[h % len(imgs)]
    return FALLBACK[h % len(FALLBACK)]

def read_post(d):
    f = os.path.join(d, 'index.html')
    s = io.open(f, encoding='utf-8').read()
    slug = os.path.basename(d)
    h1 = html.unescape(re.sub(r'<[^>]+>', '', re.search(r'<h1>(.*?)</h1>', s, re.S).group(1))).strip()
    desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
    date = None
    for m in re.finditer(r'(?s)<script type="application/ld\+json">(.*?)</script>', s):
        try: j = json.loads(m.group(1))
        except Exception: continue
        if j.get('@type') == 'BlogPosting': date = j.get('datePublished')
    if not date:
        m = re.search(r'<p class="eyebrow"[^>]*>([A-Z][a-z]+ \d{1,2}, \d{4})</p>', s)
        date = datetime.datetime.strptime(m.group(1), '%B %d, %Y').strftime('%Y-%m-%d') if m else '2026-01-01'
    # summary: first sentence or two of the lede paragraph in the pagehead
    lede = re.search(r'<h1>.*?</h1><p>(.*?)</p>', s, re.S)
    summary = html.unescape(re.sub(r'<[^>]+>', '', lede.group(1))).strip() if lede else desc
    return dict(slug=slug, h1=h1, desc=desc, date=date, summary=summary)

def main():
    posts = [read_post(d) for d in sorted(glob.glob(os.path.join(ROOT, 'blog', '*')))
             if os.path.isdir(d) and os.path.exists(os.path.join(d, 'index.html'))]
    posts.sort(key=lambda p: (p['date'], p['slug']), reverse=True)

    cards = ''
    for p in posts:
        pretty = datetime.datetime.strptime(p['date'], '%Y-%m-%d').strftime('%B %-d, %Y')
        cards += (f'<a class="card rv" href="{p["slug"]}/" style="text-decoration:none">'
                  f'<div class="card-img"><img src="../assets/img/{pick_image(p["slug"])}" '
                  f'alt="{html.escape(p["h1"], quote=True)}" loading="lazy" width="800" height="500" /></div>'
                  f'<p class="eyebrow" style="margin-bottom:.5em">{pretty}</p>'
                  f'<h3>{html.escape(p["h1"])}</h3><p>{html.escape(p["summary"])}</p>'
                  f'<span class="more">Read the article &rarr;</span></a>')

    idx = os.path.join(ROOT, 'blog', 'index.html')
    s = io.open(idx, encoding='utf-8').read()
    start = s.index('<div class="grid g3">')
    depth = 0
    for m in re.finditer(r'<div\b[^>]*>|</div>', s[start:]):
        depth += -1 if m.group(0).startswith('</') else 1
        if depth == 0:
            end = start + m.end(); break
    s = s[:start] + '<div class="grid g3">' + cards + '</div>' + s[end:]
    s = re.sub(r'(<h2>Plumbing Guides for Boynton Beach and Palm Beach County</h2>)',
               r'\1', s)
    io.open(idx, 'w', encoding='utf-8').write(s)

    sm = os.path.join(ROOT, 'sitemap.xml')
    x = io.open(sm, encoding='utf-8').read()
    x = re.sub(r'\n?\s*<url><loc>https://plumbersboyntonbeach\.com/blog/[^<]+/</loc>.*?</url>', '', x)
    entries = ''.join(
        f'\n  <url><loc>https://plumbersboyntonbeach.com/blog/{p["slug"]}/</loc>'
        f'<lastmod>{p["date"]}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>'
        for p in posts)
    x = x.replace('</urlset>', entries + '\n</urlset>')
    io.open(sm, 'w', encoding='utf-8').write(x)
    print(f'blog index and sitemap rebuilt for {len(posts)} posts')
    return posts

if __name__ == '__main__':
    main()

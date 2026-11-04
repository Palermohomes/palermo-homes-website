import os, re
os.chdir(os.path.join(os.path.dirname(__file__), '..', 'site'))
candidates = []
for root, _, files in os.walk('wp-content/uploads'):
    for f in files:
        low = f.lower()
        if not (low.endswith('.jpg') or low.endswith('.jpeg')):
            continue
        if re.search(r'-\d+x\d+\.', f):
            continue
        if any(x in low for x in ('logo', 'artboard', 'icon', 'cropped-')):
            continue
        full = os.path.join(root, f).replace(os.sep, '/')
        size = os.path.getsize(full)
        if size < 150_000:
            continue
        candidates.append((size, '/' + full))

candidates.sort(reverse=True)
cards = []
for _, path in candidates[:40]:
    cards.append(f'<div class="card"><img src="{path}" loading="lazy"><div class="name">{path}</div></div>')

html = open('pick-hero.html', encoding='utf-8').read()
html = html.replace('<div class="grid">\n', '<div class="grid">\n' + '\n'.join(cards) + '\n')
html += '</div></body></html>'
open('pick-hero.html', 'w', encoding='utf-8').write(html)
print(f'added {len(cards)} candidates')

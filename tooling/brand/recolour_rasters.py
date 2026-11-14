"""Recolour the raster brand files (PNG, GIF) from one purple to another, keeping sizes, alpha, frames and timing.

usage: python3 tooling/brand/recolour_rasters.py [--from 35307E] [--to 39235F] FILE...

Each pixel (PNG) or colour-table entry (GIF, rewritten in place, frames and timing untouched) that is the old
purple, or an anti-aliased blend of the old purple with another colour of the image, becomes the same blend with the
new purple.
"""
import sys, argparse
from PIL import Image, ImageSequence


def hexrgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def make_mapper(old, new, partners):
    def dist(a, b): return sum((x - y) ** 2 for x, y in zip(a, b)) ** .5
    partners = [q for q in partners if dist(q, old) > 40]

    def f(c):
        if dist(c, old) < 4:
            return new
        best = None
        for q in partners:
            v = [p - x for p, x in zip(old, q)]
            vv = sum(x * x for x in v)
            t = sum((ci - qi) * vi for ci, qi, vi in zip(c, q, v)) / vv
            if not 0.03 < t < 1.03:
                continue
            r = dist(c, [qi + t * vi for qi, vi in zip(q, v)])
            if r < 6 and (best is None or r < best[0]):
                best = (r, q, min(t, 1.0))
        if best is None:
            return c
        _, q, t = best
        return tuple(max(0, min(255, round(qi + t * (ni - qi)))) for qi, ni in zip(q, new))
    return f


def dominant(counts, total, share=0.004):
    return [c for c, n in counts.items() if n >= total * share]


def recolour_png(path, old, new):
    im = Image.open(path).convert('RGBA')
    px = im.load(); w, h = im.size
    counts = {}
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a > 200: counts[(r, g, b)] = counts.get((r, g, b), 0) + 1
    f = make_mapper(old, new, dominant(counts, sum(counts.values())) + [(255, 255, 255)])
    cache, changed = {}, 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0: continue
            c = (r, g, b)
            if a < 64 and sum((x - y) ** 2 for x, y in zip(c, old)) < 900:
                px[x, y] = new + (a,); changed += 1; continue   # faint edge pixels: RGB is quantised noise
            if c not in cache: cache[c] = f(c)
            if cache[c] != c:
                px[x, y] = cache[c] + (a,); changed += 1
    if changed: im.save(path, optimize=True)
    return changed


def recolour_gif(path, old, new):
    data = bytearray(open(path, 'rb').read())
    counts = {}
    for fr in ImageSequence.Iterator(Image.open(path)):
        for n, c in fr.convert('RGB').getcolors(1 << 24) or []:
            counts[c] = counts.get(c, 0) + n
    f = make_mapper(old, new, dominant(counts, sum(counts.values())) + [(255, 255, 255)])
    changed = 0

    def table(pos, size):
        nonlocal changed
        for i in range(size):
            o = pos + 3 * i; c = tuple(data[o:o + 3]); m = f(c)
            if m != c: data[o:o + 3] = bytes(m); changed += 1
        return pos + 3 * size

    p = 13; flags = data[10]
    if flags & 0x80: p = table(p, 2 ** ((flags & 7) + 1))
    while p < len(data):
        b = data[p]
        if b == 0x3B: break
        if b == 0x21:                      # extension: label, then sub-blocks
            p += 2
            while data[p]: p += data[p] + 1
            p += 1
        elif b == 0x2C:                    # image descriptor, optional local table, LZW data
            lf = data[p + 9]; p += 10
            if lf & 0x80: p = table(p, 2 ** ((lf & 7) + 1))
            p += 1
            while data[p]: p += data[p] + 1
            p += 1
        else:
            raise ValueError(f'{path}: unexpected block 0x{b:02x} at {p}')
    if changed: open(path, 'wb').write(data)
    return changed


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--from', dest='old', default='35307E'); ap.add_argument('--to', dest='new', default='39235F')
    ap.add_argument('files', nargs='+')
    a = ap.parse_args(); old, new = hexrgb(a.old), hexrgb(a.new)
    for p in a.files:
        n = recolour_gif(p, old, new) if p.lower().endswith('.gif') else recolour_png(p, old, new)
        print(f'{n:7d}  {p}')

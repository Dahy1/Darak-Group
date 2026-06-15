# Build a halftone (dotted) gray Europe map clipped to the landmass, on transparent bg.
# Style matches tresmarescapital.com: faint gray dots forming Europe, red office pins.
import json, math

d = json.load(open('europe.geojson', 'r', encoding='utf-8'))

def merc(lon, lat):
    lat = max(min(lat, 83), -83)
    return math.radians(lon), math.log(math.tan(math.pi/4 + math.radians(lat)/2))

# landscape framing (a touch of eastern Europe for width, full Iberia + Nordics)
LON0, LON1 = -12.0, 43.0
LAT0, LAT1 = 34.0, 71.0
W = 1320.0
x0, y0 = merc(LON0, LAT1)
x1, y1 = merc(LON1, LAT0)
sx = W / (x1 - x0)
H = (y0 - y1) * sx
sy = H / (y0 - y1)

def project(lon, lat):
    x, y = merc(lon, lat)
    return (x - x0) * sx, (y0 - y) * sy

def ring_path(coords):
    THRESH = 2.6
    pts, last = [], None
    for lon, lat in coords:
        px, py = project(lon, lat)
        if last is None or (abs(px-last[0]) + abs(py-last[1])) > THRESH:
            pts.append((round(px), round(py))); last = (px, py)
    if len(pts) < 3:
        return ''
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    if (max(xs)-min(xs)) < 7 and (max(ys)-min(ys)) < 7:
        return ''
    s = 'M' + f'{pts[0][0]} {pts[0][1]}'
    for px, py in pts[1:]:
        s += f'L{px} {py}'
    return s + 'Z'

paths = []
for f in d['features']:
    geom = f['geometry']
    polys = [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']
    for poly in polys:
        for ring in poly:
            xs = [c[0] for c in ring]; ys = [c[1] for c in ring]
            if max(xs) < LON0-3 or min(xs) > LON1+3 or max(ys) < LAT0-3 or min(ys) > LAT1+3:
                continue
            p = ring_path(ring)
            if p:
                paths.append(p)

clip = ''.join(f'<path d="{p}"/>' for p in paths)
svg = (
 f'<svg viewBox="0 0 {W:.0f} {H:.0f}" class="exp-map-svg" xmlns="http://www.w3.org/2000/svg" '
 f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">'
 f'<defs>'
 f'<pattern id="ohzDots" width="10" height="10" patternUnits="userSpaceOnUse">'
 f'<circle cx="2.6" cy="2.6" r="1.7" fill="#cdc9c2"/></pattern>'
 f'<clipPath id="ohzEuClip">{clip}</clipPath>'
 f'</defs>'
 f'<rect width="{W:.0f}" height="{H:.0f}" fill="url(#ohzDots)" clip-path="url(#ohzEuClip)"/>'
 f'</svg>'
)
open('europe_dots.svg', 'w', encoding='utf-8').write(svg)
print('viewBox 0 0 %.0f %.0f  ratio %.3f' % (W, H, W/H))
print('rings:', len(paths), 'bytes:', len(svg))

# office pin percentages within the viewBox
for name, lon, lat in [('Madrid',-3.703,40.417),('London',-0.127,51.507),('Frankfurt',8.682,50.110)]:
    px, py = project(lon, lat)
    print(f'{name:10s} left={px/W*100:5.2f}%  top={py/H*100:5.2f}%')

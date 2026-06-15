# Build a halftone (dotted) gray Egypt map clipped to the landmass, matching the
# previous Europe map's style. Outline is a simplified Egypt border (factual geo data).
import math

# Egypt border, clockwise (lon, lat): Med coast W->E (with Nile delta), Sinai (Aqaba
# down, Suez up), mainland Red Sea coast down, 22N south border W, ~25E west border N.
RING = [
    (25.0, 31.60), (27.0, 31.40), (28.5, 30.95), (29.9, 31.20), (30.4, 31.46),
    (31.0, 31.60), (31.6, 31.50), (32.3, 31.25), (33.5, 31.10), (34.25, 31.21),
    (34.90, 29.40), (34.50, 28.30), (34.25, 27.75),                      # Sinai E (Aqaba) -> Sharm
    (33.40, 28.60), (32.90, 29.50), (32.55, 29.97),                      # Sinai W (Suez) -> Suez
    (32.35, 29.40), (32.70, 28.50), (33.60, 27.25), (34.40, 26.00),      # mainland Red Sea coast
    (34.90, 25.00), (35.60, 24.00), (36.30, 23.10), (36.90, 22.00),      # -> SE corner
    (34.0, 22.0), (31.0, 22.0), (28.0, 22.0), (25.0, 22.0),              # south border 22N
    (25.0, 25.0), (25.0, 28.0), (25.0, 30.5),                            # west border ~25E
]

LON0, LON1 = 24.3, 37.6
LAT0, LAT1 = 21.2, 32.1
W = 1320.0

def merc(lon, lat):
    lat = max(min(lat, 83), -83)
    return math.radians(lon), math.log(math.tan(math.pi/4 + math.radians(lat)/2))

x0, y0 = merc(LON0, LAT1)
x1, y1 = merc(LON1, LAT0)
sx = W / (x1 - x0)
H = (y0 - y1) * sx

def project(lon, lat):
    x, y = merc(lon, lat)
    return (x - x0) * sx, (y0 - y) * sx

pts = [project(lon, lat) for lon, lat in RING]
path = 'M' + f'{pts[0][0]:.0f} {pts[0][1]:.0f}' + ''.join(f'L{px:.0f} {py:.0f}' for px, py in pts[1:]) + 'Z'

DOT = '#808080'   # mid-gray, clearer contrast on white
svg = (
 f'<svg viewBox="0 0 {W:.0f} {H:.0f}" class="exp-map-svg" xmlns="http://www.w3.org/2000/svg" '
 f'preserveAspectRatio="xMidYMid meet" aria-hidden="true">'
 f'<defs>'
 f'<pattern id="ohzDots" width="10" height="10" patternUnits="userSpaceOnUse">'
 f'<circle cx="2.6" cy="2.6" r="1.85" fill="{DOT}"/></pattern>'
 f'<clipPath id="ohzEuClip"><path d="{path}"/></clipPath>'
 f'</defs>'
 f'<rect width="{W:.0f}" height="{H:.0f}" fill="url(#ohzDots)" clip-path="url(#ohzEuClip)"/>'
 f'</svg>'
)

open('egypt_dots.svg', 'w', encoding='utf-8').write(svg)

# pin positions (left%, top%) for Egyptian cities
CITIES = {'Cairo': (31.24, 30.05), 'Alexandria': (29.92, 31.20), 'Aswan': (32.90, 24.09)}
print('viewBox', f'0 0 {W:.0f} {H:.0f}', '| H=', round(H))
for name, (lon, lat) in CITIES.items():
    px, py = project(lon, lat)
    print(f'{name}: left {px/W*100:.2f}% top {py/H*100:.2f}%')

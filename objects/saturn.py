import math

name = 'Saturn'

# ── Planet body ───────────────────────────────────────────────────────────────
# Oblate spheroid: 6 meridians × 5 latitude bands + north/south poles
# Vertex layout: index = i_lat * 6 + i_lon  (i_lat 0-4, i_lon 0-5)
#   S-pole: 30  N-pole: 31
_R,  _Ry = 1.0, 0.88                                   # equatorial / polar r
_lons    = [k * math.pi / 3 for k in range(6)]         # 0° 60° … 300°
_lats    = [math.radians(d) for d in (-60, -30, 0, 30, 60)]

_body = [
    (_R  * math.cos(phi) * math.cos(th),
     _Ry * math.sin(phi),
     _R  * math.cos(phi) * math.sin(th))
    for phi in _lats for th in _lons
]

_S_POLE = (0.0, -_Ry, 0.0)   # index 30
_N_POLE = (0.0,  _Ry, 0.0)   # index 31

# ── Ring system ───────────────────────────────────────────────────────────────
# Three rings in the equatorial plane, tilted 27° around the x-axis:
#   Ring C (inner crepe ring)  r=1.30  12 pts  indices 32-43
#   Ring B (bright main ring)  r=1.62  16 pts  indices 44-59
#   Ring A (outer ring)        r=2.00  16 pts  indices 60-75
# The gap between B and A (r=1.62→2.00) represents the Cassini Division.
_TILT = math.radians(27)

def _ring(r, n):
    pts = []
    for k in range(n):
        th = 2 * math.pi * k / n
        x  = r * math.cos(th)
        z0 = r * math.sin(th)
        pts.append((x, -z0 * math.sin(_TILT), z0 * math.cos(_TILT)))
    return pts

_ring_c = _ring(1.30, 12)
_ring_b = _ring(1.62, 16)
_ring_a = _ring(2.00, 16)

verts = _body + [_S_POLE, _N_POLE] + _ring_c + _ring_b + _ring_a

# ── Edges ─────────────────────────────────────────────────────────────────────
edges = []

# Latitude parallels (5 horizontal circles)
for i_lat in range(5):
    base = i_lat * 6
    for i_lon in range(6):
        edges.append((base + i_lon, base + (i_lon + 1) % 6))

# Meridians: S-pole → lat-0 → lat-1 → … → lat-4 → N-pole
for i_lon in range(6):
    edges.append((30, i_lon))
    for i_lat in range(4):
        edges.append((i_lat * 6 + i_lon, (i_lat + 1) * 6 + i_lon))
    edges.append((24 + i_lon, 31))

# Ring C (12 segments)
for k in range(12):
    edges.append((32 + k, 32 + (k + 1) % 12))

# Ring B (16 segments)
for k in range(16):
    edges.append((44 + k, 44 + (k + 1) % 16))

# Ring A (16 segments)
for k in range(16):
    edges.append((60 + k, 60 + (k + 1) % 16))

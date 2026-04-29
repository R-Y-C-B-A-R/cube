#!/usr/bin/env python3
# Real-time 3D wireframe renderer for the terminal.
# Usage: python3 cube.py [name|file]   (default: wuerfel)
# Built-in objects: objects/wuerfel.py  objects/pyramide.py  objects/katze.py
import math, time, sys, os
from objects import load

def rotate(pts, ax, ay, az):
    out = []
    for x, y, z in pts:
        y, z = y*math.cos(ax) - z*math.sin(ax), y*math.sin(ax) + z*math.cos(ax)
        x, z = x*math.cos(ay) + z*math.sin(ay), -x*math.sin(ay) + z*math.cos(ay)
        x, y = x*math.cos(az) - y*math.sin(az), x*math.sin(az) + y*math.cos(az)
        out.append((x, y, z))
    return out

def project(pts, W, H, fov, dist=4.5):
    return [
        (int(x * fov / (z + dist) + W / 2),
         int(y * fov / (z + dist) * 0.5 + H / 2))
        for x, y, z in pts
    ]

def draw_line(buf, W, H, x0, y0, x1, y1):
    dx, dy = abs(x1-x0), abs(y1-y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    e = dx - dy
    while True:
        if 0 <= x0 < W and 0 <= y0 < H:
            buf[y0 * W + x0] = '·'
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * e
        if e2 > -dy: e -= dy; x0 += sx
        if e2 <  dx: e += dx; y0 += sy

def main():
    obj = load(sys.argv[1] if len(sys.argv) > 1 else 'wuerfel')
    verts = obj['verts']
    edges = obj['edges']
    label = obj['name']

    try:
        cols, rows = os.get_terminal_size()
    except OSError:
        cols, rows = 80, 24
    W, H = min(cols, 120), min(rows - 1, 40)

    ax = ay = az = 0.0
    fov = int(H * 3.2)
    sys.stdout.write('\033[?25l\033[2J')

    try:
        while True:
            buf = [' '] * (W * H)
            pts = project(rotate(verts, ax, ay, az), W, H, fov)

            for i, j in edges:
                draw_line(buf, W, H, *pts[i], *pts[j])

            for px, py in pts:
                if 0 <= px < W and 0 <= py < H:
                    buf[py * W + px] = '+'

            # Label bottom-left
            for ci, ch in enumerate(label):
                if ci < W:
                    buf[(H - 1) * W + ci] = ch

            sys.stdout.write('\033[H' + '\n'.join(
                ''.join(buf[r * W:(r + 1) * W]) for r in range(H)
            ))
            sys.stdout.flush()

            ax += 0.020
            ay += 0.033
            az += 0.011
            time.sleep(0.033)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write('\033[?25h\033[H\033[2J')

if __name__ == '__main__':
    main()

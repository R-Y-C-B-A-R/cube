# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running

```bash
python3 cube.py              # default: wuerfel
python3 cube.py pyramide     # built-in by name
python3 cube.py myobj.py     # any .py file with name/verts/edges
```

Press `Ctrl+C` to exit. No dependencies beyond the Python standard library (`math`, `time`, `sys`, `os`, `importlib`, `pathlib`).

## Architecture

The project has two parts: `cube.py` (renderer) and the `objects/` package (geometry definitions).

### Object files (`objects/`)

Each object is a standalone Python file with three module-level variables:

```python
name  = 'Würfel'          # display label
verts = [(x,y,z), ...]    # 3-D corner coordinates
edges = [(i,j), ...]      # index pairs into verts
```

Built-ins: `wuerfel.py`, `pyramide.py`, `katze.py`, `saturn.py`. Add any new `.py` file with the same structure and pass its name or path to `cube.py`.

`objects/__init__.py` exposes `load(name)` which resolves the argument as a direct file path first, then as `objects/<name>.py`, and raises `SystemExit` with the available list if neither exists.

### Rendering pipeline (`cube.py`)

The rendering pipeline runs top-to-bottom each frame:

1. **Geometry** — `VERTS` (8 corner coordinates) and `EDGES` (12 index pairs) define a static cube.
2. **`rotate(pts, ax, ay, az)`** — applies three successive rotation matrices (X → Y → Z) to all vertices each frame. The angles accumulate at different rates (`ax += 0.020`, `ay += 0.033`, `az += 0.011`) so the rotation never visibly repeats.
3. **`project(pts, W, H, fov, dist)`** — perspective projection: divides by `z + dist` and scales Y by 0.5 to correct for terminal character aspect ratio.
4. **`draw_line(buf, ...)`** — Bresenham's line algorithm writes `·` characters into a flat `W*H` character buffer.
5. **`main()`** — the animation loop: clears to a blank buffer, rotates + projects vertices, draws edges, overdraw vertices with `+`, then writes the whole buffer to stdout via a single ANSI escape sequence (`\033[H` to home the cursor). Target is ~30 FPS (`time.sleep(0.033)`).

Terminal size is read from `os.get_terminal_size()` and clamped to 120×40; FOV is derived from terminal height (`H * 3.2`). Cursor hiding/restoring uses ANSI escape codes (`\033[?25l` / `\033[?25h`).

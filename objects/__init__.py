import importlib.util
import pathlib

_HERE = pathlib.Path(__file__).parent


def load(name):
    p = pathlib.Path(name)
    if not p.exists():
        p = _HERE / (name + '.py')
    if not p.exists():
        available = sorted(f.stem for f in _HERE.glob('*.py') if f.name != '__init__.py')
        raise SystemExit(f"Unbekanntes Objekt '{name}'. Verfügbar: {', '.join(available)}")
    spec = importlib.util.spec_from_file_location('_obj', p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {'name': mod.name, 'verts': mod.verts, 'edges': mod.edges}

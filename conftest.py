import pathlib
import sys
import types

PROJECT_DIR = pathlib.Path(__file__).resolve().parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

if 'line_profiler' not in sys.modules:
    line_profiler = types.ModuleType('line_profiler')
    line_profiler.profile = lambda func: func
    sys.modules['line_profiler'] = line_profiler

cache_dir = PROJECT_DIR / '__pycache__'
if cache_dir.exists():
    for path in cache_dir.glob('*.nb[ci]'):
        try:
            path.unlink()
        except OSError:
            pass

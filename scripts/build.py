"""Regenerate every animated SVG in ./assets:  python3 scripts/build.py"""
import importlib
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))

for mod, fn in (("hero", "hero"), ("cards", "cards"), ("sections", "sections")):
    getattr(importlib.import_module(mod), fn)()

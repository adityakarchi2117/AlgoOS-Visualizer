# File: frontend/pages/__init__.py
"""
Page modules for AlgoOS Visualizer.
DSA pages only - OS pages are handled directly in app.py
"""

from . import dsa_stack
from . import dsa_linkedlist
from . import dsa_tree

__all__ = [
    'dsa_stack',
    'dsa_linkedlist', 
    'dsa_tree'
]

"""Addons activator for Anki v2.1."""

import os
import sys

_HERE = os.path.dirname(__file__)

sys.path.append(os.path.abspath(os.path.join(_HERE, '..')))

import activate_addons

activate_addons.activate_default_addons()

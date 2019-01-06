"""Activate selected addons."""

import os
import sys

from anki import version as anki_version
anki_version = tuple([int(_) for _ in anki_version.split('.')])


def activate_addon_py2(folder_name, module_name):
    sys.path.append(os.path.join(os.path.dirname(__file__), folder_name))
    __import__(module_name)


def activate_addon(folder_name, module_name):
    sys.path.append(pathlib.Path(__file__).parent.joinpath(folder_name))
    __import__(module_name)


if sys.version_info[:2] > (3, 5):
    import pathlib
else:
    import os

    activate_addon = activate_addon_py2

# Button Colours (Good, Again)
sys.path.append(os.path.join(os.path.dirname(__file__), 'button_colours'))
import button_colours

# Night Mode
if anki_version[:2] >= (2, 1):
    sys.path.append(os.path.join(os.path.dirname(__file__), 'night_mode'))
    import night_mode
else:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'night_mode_legacy'))
    import Night_Mode

# True Retention by Card Maturity
sys.path.append(os.path.join(
    os.path.dirname(__file__), 'addons_by_glutanimate', 'src', 'stats_true_retention_extended'))
import stats_true_retention_extended

# True Retention graph
sys.path.append(os.path.join(os.path.dirname(__file__), 'addons_by_sebastiengllmt', 'src'))
import true_retention_graph

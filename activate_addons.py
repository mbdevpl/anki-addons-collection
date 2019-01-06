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

# Deck name in title
sys.path.append(os.path.join(os.path.dirname(__file__), 'addons_by_ospalh'))
import deck_name_in_title

# Deck Stats
sys.path.append(os.path.join(os.path.dirname(__file__), 'deck_stats'))
import deck_stats

# Night Mode
if anki_version[:2] >= (2, 1):
    sys.path.append(os.path.join(os.path.dirname(__file__), 'night_mode'))
    import night_mode
else:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'night_mode_legacy'))
    import Night_Mode

# Progress Graphs and Stats for Learned and Matured Cards
sys.path.append(os.path.join(os.path.dirname(__file__), 'progress_for_learned_and_matured_cards'))
import chart_progress

# Review Heatmap
if anki_version[:2] >= (2, 1):
    sys.path.append(os.path.join(os.path.dirname(__file__), 'review_heatmap', 'src'))
else:
    sys.path.append(os.path.join(os.path.dirname(__file__), 'review_heatmap_legacy'))
import review_heatmap

# Speed Focus Mode (auto-alert, auto-reveal, auto-fail)
sys.path.append(os.path.join(
    os.path.dirname(__file__), 'addons_by_glutanimate', 'src', 'reviewer_speed_mode'))
import speed_focus_mode

# True Retention by Card Maturity
sys.path.append(os.path.join(
    os.path.dirname(__file__), 'addons_by_glutanimate', 'src', 'stats_true_retention_extended'))
import stats_true_retention_extended

# True Retention graph
sys.path.append(os.path.join(os.path.dirname(__file__), 'addons_by_sebastiengllmt', 'src'))
import true_retention_graph

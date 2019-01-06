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

# Export Browser's card list contents to CSV file Enhanced
sys.path.append(os.path.join(os.path.dirname(__file__), 'export_cards_to_csv_legacy'))
import Export_Browsers_card_list_contents_to_CSV_file_Enhanced

# Export Notes in CSV format
sys.path.append(os.path.join(os.path.dirname(__file__), 'export_decks_to_csv'))
import export_csv

# More Overview Stats 2
sys.path.append(os.path.join(os.path.dirname(__file__), 'more_overveiw_stats_legacy'))
import More_Overview_Stats_2

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

# Stats: Expected number of cards
sys.path.append(os.path.join(os.path.dirname(__file__), 'expectd_cards_legacy'))
import Stats_Expected_number_of_cards

# True Retention by Card Maturity
sys.path.append(os.path.join(
    os.path.dirname(__file__), 'addons_by_glutanimate', 'src', 'stats_true_retention_extended'))
import stats_true_retention_extended

# True Retention graph
sys.path.append(os.path.join(os.path.dirname(__file__), 'addons_by_sebastiengllmt', 'src'))
import true_retention_graph

#!/usr/bin/env python

"""Activate selected addons."""

import json
import logging
import os
import sys

_LOG = logging.getLogger(__name__)
_HERE = os.path.dirname(__file__)

# if sys.version_info[:2] > (3, 5):
#     import pathlib
#     _HERE = pathlib.Path(__file__).parent

if not _LOG.handlers:
    logging.basicConfig()
    # _LOG.addHandler(logging.StreamHandler(stream=sys.stdout))


def activate_addon(folder_name, module_name=None):
    # if sys.version_info[:2] > (3, 5):
    #     path = _HERE.joinpath(folder_name)
    # else:
    path = os.path.join(_HERE, folder_name)
    if module_name is None:
        module_name = os.path.basename(path)
    sys.path.append(path)
    __import__(module_name)


def activate_addons(addons, active_addons):
    # type: (dict, list) -> None
    """Activate addons according to provided configuration."""
    activated = 0
    for addon_name in active_addons:
        addon_data = addons[addon_name]
        if 'path' not in addon_data:
            addon_data = addon_data.get(ANKI_VERSION_TAG, addon_data.get('', None))
            if addon_data is None:
                _LOG.info('skipping addon "%s" - it is incompatible with Anki %s',
                          addon_name, ANKI_VERSION_TAG)
                continue
        activate_addon(addon_data['path'], addon_data.get('module', None))
        activated += 1
    _LOG.info('Addons summary: %i configured, %i activated, %i incompatible',
              len(addons), activated, len(active_addons) - activated)


def addons_config():
    # type () -> dict
    addons_json_path = 'addons.json'
    addons_json_path = os.path.join(_HERE, addons_json_path)
    with open(addons_json_path) as addons_json:
        return json.load(addons_json)


def activate_default_addons():
    """Activate default addons according to configuration files."""
    _LOG.info('Activating default addons in Anki %s', ANKI_VERSION_TAG)
    addons = addons_config()
    active_addons_json_path = 'active_addons.json'
    active_addons_json_path = os.path.join(_HERE, active_addons_json_path)
    with open(active_addons_json_path) as active_addons_json:
        active_addons = json.load(active_addons_json)
    activate_addons(addons, active_addons)


def main():
    addons = addons_config()
    print('available addons:')
    for addon_name in addons:
        print('"{}"'.format(addon_name))


if __name__ == '__main__':
    main()
else:
    try:
        from anki import version as anki_version
        ANKI_VERSION = tuple([int(_) for _ in anki_version.replace('beta', '.').split('.')])
        ANKI_VERSION_TAG = 'v{}'.format('.'.join([str(_) for _ in ANKI_VERSION[:2]]))
        if ANKI_VERSION[:2] <= (2, 0):
            activate_default_addons()
    except ImportError:
        _LOG.exception('attempted to activate addons but failed')


def _activate_default_addons():
    # Button Colours (Good, Again)
    sys.path.append(os.path.join(os.path.dirname(__file__), 'button_colours'))
    import button_colours

    # Deck name in title
    if anki_version[:2] <= (2, 0):
        sys.path.append(os.path.join(os.path.dirname(__file__), 'addons_by_ospalh'))
        import deck_name_in_title

    # Deck Stats
    sys.path.append(os.path.join(os.path.dirname(__file__), 'deck_stats'))
    import deck_stats

    # Export Browser's card list contents to CSV file Enhanced
    if anki_version[:2] <= (2, 0):
        sys.path.append(os.path.join(os.path.dirname(__file__), 'export_cards_to_csv_legacy'))
        import Export_Browsers_card_list_contents_to_CSV_file_Enhanced

    # Export Notes in CSV format
    if anki_version[:2] <= (2, 0):
        sys.path.append(os.path.join(os.path.dirname(__file__), 'export_decks_to_csv'))
        import export_csv

    # More Overview Stats 2
    sys.path.append(os.path.join(os.path.dirname(__file__), 'more_overview_stats_legacy'))
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
        # sys.path.append(os.path.join(os.path.dirname(__file__), 'review_heatmap', 'src'))
        pass
    else:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'review_heatmap_legacy'))
        import review_heatmap

    # Speed Focus Mode (auto-alert, auto-reveal, auto-fail)
    sys.path.append(os.path.join(
        os.path.dirname(__file__), 'addons_by_glutanimate', 'src', 'reviewer_speed_mode'))
    import speed_focus_mode

    # Stats: Expected number of cards
    sys.path.append(os.path.join(os.path.dirname(__file__), 'expected_cards_legacy'))
    import Stats_Expected_number_of_cards

    # True Retention by Card Maturity
    sys.path.append(os.path.join(
        os.path.dirname(__file__), 'addons_by_glutanimate', 'src', 'stats_true_retention_extended'))
    import stats_true_retention_extended

    # True Retention graph
    sys.path.append(os.path.join(os.path.dirname(__file__), 'addons_by_sebastiengllmt', 'src'))
    import true_retention_graph

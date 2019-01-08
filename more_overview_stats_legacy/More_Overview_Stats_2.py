# -*- coding: utf-8 -*-

"""
More Overview Stats 2
=====================
Statistics add-on for Anki -- based on "More Overview Stats" by
Calumks <calumks@gmail.com>

Copyright (c) 2014 Martin Zuther (http://www.mzuther.de/)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Thank you for using free software!


USAGE
=====
This statistics add-on for Anki is based on the nice "More Overview
Stats" add-on by Calumks but shows more (and different) values.

To change the behaviour of this add-on, create a JSON file called
'More_Overview_Stats_2.json' in your profile folder.  When you edit
this file, please make sure you save the JSON file using a compatible
encoding such as UTF-8.

In case you don't like to see the stats on finished decks, copy the
following lines to your JSON file:

   {
      "options": {
         "show_table_for_finished_decks": false
      }
   }

There is another (advanced) option: I use Anki to learn vocabulary,
and some of my decks have one card per note, while others have two
cards per note.  To watch my progress, I want to know the (somewhat
virtual) number of *notes* instead of the cards.

To achieve this, edit the JSON file along these lines:

   {
      "options": {
         "show_table_for_finished_decks": true
      },
      "note_correction_factors": {
         "Spanisch": 2,
         "Türkisch": 2,
         "Türkisch::Word Pool": 1
      }
   }

If everything works fine, this add-on will compare the current deck
name with the entries and use the factor given for the longest match.

For the example above, all Spanish and Turkish decks will divide the
card numbers by 2, while the subdeck "Türkisch::Word Pool" will show
the original card numbers.  Please note that the card numbers for new,
learning and review will NOT be modified so that you can still monitor
your learning progress.

Enjoy!


HISTORY
=======
version 1.9:

* now works correctly with empty decks (thanks to Jonte!)

version 1.8:

* changed displayed values (unseen / suspended)
* format display using CSS

version 1.7:

* move hidden variable from source code to JSON file

version 1.6:

* correct note numbers by deck-specific factors

version 1.5:

* hide new/learning/review block when deck is finished

version 1.4:

* changed displayed values (learned / unlearned)

version 1.3:

* support Unicode in localisations

version 1.2:

* align table regardless of font

version 1.1:

* show table even if deck is finished

version 1.0:

* initial commit

"""

import json
import os
import time
from aqt.overview import Overview


def overview_table(self):
    json_file = os.path.join(self.mw.pm.profileFolder(),
                             'More_Overview_Stats_2.json')

    if os.path.isfile(json_file):
        with open(json_file, mode='r') as f:
            settings = json.load(f)
    else:
        settings = {}

    current_deck_name = self.mw.col.decks.current()['name']

    correction_for_notes = 1
    last_match_length = 0

    if 'note_correction_factors' in settings:
        for fragment, factor in settings['note_correction_factors'].items():
            if current_deck_name.startswith(fragment):
                if len(fragment) > last_match_length:
                    correction_for_notes = int(factor)
                    last_match_length = len(fragment)

        # prevent division by zero and negative results
        if correction_for_notes <= 0:
            correction_for_notes = 1

    total, mature, young, unseen, suspended, due = self.mw.col.db.first(
        u'''
          select
          -- total
          count(id),
          -- mature
          sum(case when queue = 2 and ivl >= 21
                   then 1 else 0 end),
          -- young / learning
          sum(case when queue in (1, 3) or (queue = 2 and ivl < 21)
                   then 1 else 0 end),
          -- unseen
          sum(case when queue = 0
                   then 1 else 0 end),
          -- suspended
          sum(case when queue < 0
                   then 1 else 0 end),
          -- due
          sum(case when queue = 1 and due <= ?
                   then 1 else 0 end)
          from cards where did in {:s}
        '''.format(self.mw.col.sched._deckLimit()),
        round(time.time()))

    if not total:
        return u'<p>No cards found.</p>'

    scheduled_counts = list(self.mw.col.sched.counts())
    deck_is_finished = not sum(scheduled_counts)

    cards = {}

    cards['mature'] = round(mature / int(correction_for_notes))
    cards['young'] = round(young / int(correction_for_notes))
    cards['unseen'] = round(unseen / int(correction_for_notes))
    cards['suspended'] = round(suspended / int(correction_for_notes))

    cards['total'] = round(total / int(correction_for_notes))
    cards['learned'] = cards['mature'] + cards['young']
    cards['unlearned'] = cards['total'] - cards['learned']

    cards['new'] = scheduled_counts[0]
    cards['learning'] = scheduled_counts[1]
    cards['review'] = scheduled_counts[2]
    # cards['due'] = due + cards['review']

    cards_percent = {}

    cards_percent['mature'] = cards['mature'] * 1.0 / cards['total']
    cards_percent['young'] = cards['young'] * 1.0 / cards['total']
    cards_percent['unseen'] = cards['unseen'] * 1.0 / cards['total']
    cards_percent['suspended'] = cards['suspended'] * 1.0 / cards['total']

    cards_percent['total'] = 1.0
    cards_percent['learned'] = cards['learned'] * 1.0 / cards['total']
    cards_percent['unlearned'] = cards['unlearned'] * 1.0 / cards['total']

    cards_percent['new'] = cards['new'] * 1.0 / cards['total']
    cards_percent['learning'] = cards['learning'] * 1.0 / cards['total']
    cards_percent['review'] = cards['review'] * 1.0 / cards['total']
    # cards_percent['due'] = cards['due'] * 1.0 / cards['total']

    labels = {}

    labels['mature'] = _('Mature')
    labels['young'] = _('Young')
    labels['unseen'] = _('Unseen')
    labels['suspended'] = _('Suspended')

    labels['total'] = _('Total')
    labels['learned'] = _('Learned')
    labels['unlearned'] = _('Unlearned')

    labels['new'] = _('New')
    labels['learning'] = _('Learning')
    labels['review'] = _('Review')
    # labels['due'] = _('Due')

    for key in labels:
        labels[key] = u'{:s}:'.format(labels[key])

    button = self.mw.button

    output_table = u'''
      <style type="text/css">
      <!--
        hr {
            height: 1px;
            border: none;
            border-top: 1px solid #aaa;
        }

        td {
            vertical-align: top;
        }

        td.row1 {
            text-align: left;
        }

        td.row2 {
            text-align: right;
            padding-left: 1.2em;
            padding-right: 1.2em;
        }

        td.row3 {
            text-align: right;
        }

        td.new {
            font-weight: bold;
            color: #00a;
        }

        td.learning {
            font-weight: bold;
            color: #a00;
        }

        td.review {
            font-weight: bold;
            color: #080;
        }

        td.percent {
            font-weight: normal;
            color: #888;
        }

        td.mature {
            font-weight: normal;
            color: #008;
        }

        td.young {
            font-weight: normal;
            color: #008;
        }

        td.learned {
            font-weight: normal;
            color: #080;
        }

        td.unseen {
            font-weight: normal;
            color: #a00;
        }

        td.suspended {
            font-weight: normal;
            color: #a70;
        }

        td.total {
            font-weight: bold;
            color: #000;
        }
      -->
      </style>

      <table cellspacing="2">
    '''

    if not deck_is_finished:
        output_table += u'''
            <tr>
              <td class="row1">{label[new]:s}</td>
              <td class="row2 new">{cards[new]:d}</td>
              <td class="row3 percent">{percent[new]:.0%}</td>
            </tr>
            <tr>
              <td class="row1">{label[learning]:s}</td>
              <td class="row2 learning">{cards[learning]:d}</td>
              <td class="row3 percent">{percent[learning]:.0%}</td>
            </tr>
            <tr>
              <td class="row1">{label[review]:s}</td>
              <td class="row2 review">{cards[review]:d}</td>
              <td class="row3 percent">{percent[review]:.0%}</td>
            </tr>
            <tr>
              <td colspan="3"><hr /></td>
            </tr>
        '''.format(label=labels,
                   cards=cards,
                   percent=cards_percent)

    output_table += u'''
        <tr>
          <td class="row1">{label[mature]:s}</td>
          <td class="row2 mature">{cards[mature]:d}</td>
          <td class="row3 percent">{percent[mature]:.0%}</td>
        </tr>
        <tr>
          <td class="row1">{label[young]:s}</td>
          <td class="row2 young">{cards[young]:d}</td>
          <td class="row3 percent">{percent[young]:.0%}</td>
        </tr>
        <tr>
          <td colspan="3"><hr /></td>
        </tr>
        <tr>
          <td class="row1">{label[learned]:s}</td>
          <td class="row2 learned">{cards[learned]:d}</td>
          <td class="row3 percent">{percent[learned]:.0%}</td>
        </tr>
        <tr>
          <td class="row1">{label[unseen]:s}</td>
          <td class="row2 unseen">{cards[unseen]:d}</td>
          <td class="row3 percent">{percent[unseen]:.0%}</td>
        </tr>
        <tr>
          <td class="row1">{label[suspended]:s}</td>
          <td class="row2 suspended">{cards[suspended]:d}</td>
          <td class="row3 percent">{percent[suspended]:.0%}</td>
        </tr>
        <tr>
          <td colspan="3"><hr /></td>
        </tr>
        <tr>
          <td class="row1">{label[total]:s}</td>
          <td class="row2 total">{cards[total]:d}</td>
          <td class="row3 percent">{percent[total]:.0%}</td>
        </tr>
    '''.format(label=labels,
               cards=cards,
               percent=cards_percent)

    output = ''

    if deck_is_finished:
        if (not 'options' in settings) or (settings['options'].get(
                'show_table_for_finished_decks', True)):
            output += output_table
            output += u'''
              </table>
              <hr style="margin: 1.5em 0; border-top: 1px dotted #888;" />
            '''

        output += u'''
          <div style="white-space: pre-wrap;">{:s}</div>
        '''.format(self.mw.col.sched.finishedMsg())
    else:
        output += output_table
        output += u'''
            <tr>
              <td colspan="3" style="text-align: center; padding-top: 0.6em;">{button:s}</td>
            </tr>
          </table>
        '''.format(button=button('study', _('Study Now'), id='study'))

    return output


# replace _table method
Overview._table = overview_table

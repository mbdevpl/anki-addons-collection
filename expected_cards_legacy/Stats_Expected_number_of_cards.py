# -*- coding: utf-8 -*-
# Copyright: Fabien  S H U M - K I N G
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# Displays in the stats for each deck (or the current one) the number
# of expected cards per day, according to their frequency.
# For example, a card with a frequency of 3 days count as 1/3 card per day

# version: 0.2

import anki
import anki.stats
import aqt
import math
import time
import datetime

# save previous graph func
fsk_old_cardGraph = anki.stats.CollectionStats.todayStats

def fskNewGraph(self):
	out = self._title("Average expected cards","")
	deck_stats = []
	# for each of the decks or the current deck (according to stats option)
	for deck in self.col.decks.all() if self.wholeCollection else (self.col.decks.current(),):
		# get sum 
		res = self.col.db.scalar(
		"select round(sum(1./ivl),2) from cards where did=? and ivl>0 and queue!=-1",
		deck['id'])
		if res>0:
			deck_stats.append((deck["name"], res))
	# decreasing count sort
	deck_stats.sort(lambda x, y: -cmp(x[1], y[1]))
	
	# add sum if many decks stats
	if len(deck_stats)>1:
		deck_stats.append(("Total", sum(map(lambda x: x[1], deck_stats))))

	# create lines
	lines = []
	for st in deck_stats:
		self._line(lines, st[0], "{0} cards per day".format(st[1]))
		
	out += self._lineTbl(lines)
	return fsk_old_cardGraph(self) + out

# replace graph func
anki.stats.CollectionStats.todayStats = fskNewGraph


# -*- coding: utf-8 -*-
# Export the Browser's selected rows to a csv data file
# I dont take credit for this because I'm not the original author
# Now if i'm breaking the License: GNU GPL, version 3 , then i'm sorry because my English is my second language and 
# I Can tell you the terms used in that license description is ESL-unfriendly. So yes, i'm sorry for being irresponsible but no way 
# am I going to spend my whole week with my dictionary and decrypts the terms and agreement for the license. My Goal is to learn to read japanese, not formal English vocabs.
# However, If you email me in Easy English that I should remove this add-on because it's against the rule, then i'll gladly remove this add-on. 
# Copyright (Original Author): Steve AW <steveawa@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# 
# Support: None. Use at your own risk. If you do find a problem please email me # steveawa@gmail.com but no promises.
# This addon exports the contents of the Browser's selected rows to a csv
# 	file that is escaped/quoted etc to be compatible with MS Excel.
# You can control which columns are exported by adding/removing
# 	columns from the Browser's list.
# To use: 
# 	1. Open the Browse window.
# 	2. Select the rows you want to export. (If you want all rows, 
#		click on the "Edit" menu, then click on "Select All".
#	3. Click on the "Edit" menu, then click on "Export Selected to CSV".
#	4. Select the file name/location where you want the file saved.
#
# Note: I wrote this because I wanted access to the Due dates and intervals
# 	to analyze in another program. As far as I can see it exports the other types
# 	of fields, including the text fields, without any problems. But I have not
# 	looked closetly at anything except for the date fields. 
#
# Warning: buyer beware ... The author is not a python, nor a qt programmer
#
# Support: None. Use at your own risk. If you do find a problem please email me
# 	fickle_123@hotmail.com but no promises.
# Rev Log (Original Author):
# 1. 25-Jun-2013 Fix bug introduced in Anki2.09 due to change in getSaveFile()

# Rev Log (What I modified):
# 1. 06-12-2014 Fix Null object error which occurred when the field is blank
# 2. 06-12-2014 changed default delimiter to tab  (original delimiter was ,) so I can view it on excel
#
# Outstanding To-do:
# 1. figure out how to export column in the order seen by the browser 

import sys, csv, os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt.utils import getSaveFile, showWarning
from aqt import mw



#I am not sure if I needed to do this, but I just wanted an object that could stand
#	in for the Index objects that browser.py DataModel>>columnData	was expecting
class RowAndColumn(object):
	def __init__(self, r, c):
		self.irow = r
		self.icolumn = c
	def row(self):
		return self.irow
	def column(self):
		return self.icolumn

#copied from Exporter class
#Possibly not necessary as the csv writer object is set to the excel dialect?
def escapeText(text):
	"Escape newlines and tabs, and strip Anki HTML."
	"Only do this if the text(aka field) is not null"
	if not text is None:
		text = text.replace("\n", "<br>")
		text = text.replace("\t", " " * 8)
	return text

def onExportList(browser):
	if not browser.form.tableView.selectionModel().hasSelection():
		showWarning("Please select 1 or more rows", browser, help="")
		return
	path = getSaveFile( browser, _("Export Browser List"), "exportcsv", _("Cards as CSV"), '.csv' , 'exportcsv.csv')
	if not path: 
		return
	file = open(path, "wb")
	writer = csv.writer(file, dialect='excel',delimiter ='	')

	for rowIndex in browser.form.tableView.selectionModel().selectedRows():
		#wasn't sure if I could modify the "Index" objects we get back from
		#  the selection model. Since the columnData function only accesses
		#  the row() and column() functions, seemed safer to create new
		#  instances.
		row = rowIndex.row()
		rowdata = []
		for column in range(browser.model.columnCount(0)):
			index = RowAndColumn(row, column)
			#let the browser model's columnData function do all the hard work
			answer = escapeText(browser.model.columnData(index))
			"Only do this if the text(aka field) is not null"
			if not answer is None:
				rowdata.append(answer.encode('utf8'))
			if answer is None:
				rowdata.append(answer)
		writer.writerow(rowdata)
	file.close()

def setupMenu(browser):
	a = QAction("Export Selected To CSV", browser)
	browser.connect(a, SIGNAL("triggered()"), lambda b=browser: onExportList(b))
	browser.form.menuEdit.addSeparator()
	browser.form.menuEdit.addAction(a)
addHook("browser.setupMenus", setupMenu)
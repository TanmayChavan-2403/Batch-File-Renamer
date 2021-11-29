from functools import partial
from configparser import ConfigParser
from tkinter import *
from tkinter import messagebox
from tkinter import Listbox
from tkinter import ttk
from datetime import date
from datetime import datetime
import os


class ConsoleStatusFrame():


	def __init__(self, win):
		win.update_idletasks()

		width = (win.winfo_width() // 2)
		height = win.winfo_height()

		self.CS_Frame = Frame(win, height=height-50, width=width, bg='#222222')
		self.CS_Frame.grid(row = 1, column = 1, sticky='E')
		self.CS_Frame.grid_propagate(0)

		Grid.columnconfigure(self.CS_Frame, 0, weight = 1)
		Grid.rowconfigure(self.CS_Frame, 0, weight = 1)

		win.update_idletasks() 


		# This will be base Frame in which all the status will be displayed
		self.consoleFrame = LabelFrame(self.CS_Frame,text='Status Console', width=width, height = height-70, bg='#222222', fg='white',
			font=('Flux Regular', 20, 'bold'))
		self.consoleFrame.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))
		self.consoleFrame.grid_propagate(0)
		Grid.rowconfigure(self.consoleFrame, 0, weight=1)
		Grid.columnconfigure(self.consoleFrame, 0, weight=1)

		self.statusList = Listbox(self.consoleFrame, bg='#222222', fg='white', font=('Flux Regular', 10, 'bold'), 
			bd = 0, highlightbackground='#222222', relief='solid')
		self.statusList.grid(row=0, column = 0, padx=(10, 10), pady=(10, 10), sticky='nsew')

		self.scrollBar = Scrollbar(self.consoleFrame, orient="horizontal", bg='grey', activerelief='solid',
			bd=0, cursor='hand2', troughcolor='#222222', relief='solid')
		self.scrollBar.grid(row=1, column=0, sticky='ew')

		# Configuring scrollbar for statusList
		self.statusList.configure(xscrollcommand = self.scrollBar.set)
		self.scrollBar.configure(command=self.statusList.xview)

		self.clearConsoleButton = Button(self.consoleFrame, text='Clear Console', activebackground='tomato', activeforeground='white', bd=0, 
			relief='solid', bg='#0892d0',highlightthickness = 0, fg='white', font=('Flux Regular', 10, 'bold'),
			cursor='hand2', command= self.clearConsole)
		self.clearConsoleButton.grid(row=1, column=0, sticky='ew')

		self.deleteHistoryButton = Button(self.consoleFrame, text='Delete Entire History', activebackground='tomato', activeforeground='white', bd=0, 
			relief='solid', bg='#0892d0',highlightthickness = 0, fg='white', font=('Flux Regular', 10, 'bold'), cursor='hand2',
			command=self.deleteHistory)



	def saveLogsToHistory(self):
		entries = self.statusList.get(0, END)
		with open('./packages/history.txt', 'at') as file:
			file.write('DAY: ' + date.today().strftime("%B %d, %Y") + ' ' + 'TIME: ' + datetime.now().strftime("%H:%M:%S") + '\n')
			for entry in range(len(entries) - 1):
				file.write(entries[entry] + '\n')


	def logToConsole(self, value, action=None):
		if action == 'delete':
			self.statusList.delete(0, END)
		else:
			self.statusList.insert(END, value)


	def clearConsole(self):
		# Clearing the entire listbox
		self.statusList.delete(0, END)

		# If remove history button was grided to screen then we will remove it too
		self.deleteHistoryButton.grid_forget()

		# Reconfiguring the column of consoleFrame
		Grid.columnconfigure(self.consoleFrame, 1, weight=0)

		# Re-gridding the listbox to change the remove the columnspan value
		self.statusList.grid(row=0, column = 0, padx=(10, 10), pady=(10, 10), sticky='nsew')


	def deleteHistory(self):
		if messagebox.askyesno('Confirmation Window', 'This action will delete all the history recorded so far, do you still want to proceed futher ?'):
			with open('./packages/history.txt', 'r+') as file:
				file.truncate(0)

			# Running this function again so that it resets all the widgets and clears console
			self.clearConsole()
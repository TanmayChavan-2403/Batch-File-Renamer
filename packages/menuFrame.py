from functools import partial
import configparser
from tkinter import *
from tkinter import messagebox
from tkinter import Listbox
from tkinter import ttk
import os


class MenuFrame():
	def __init__(self, win):
		if sys.platform == 'win32':
			bgColor = '#0892d0'
		else:
			bgColor = '#222222'

		self.action = 'Default'

		width = win.winfo_screenwidth() - 60
		height = win.winfo_screenheight()
		win.configure(bg='#0f0f0f')

		self.M_Frame = Frame(win, height='40', width=width, bg='#0f0f0f')
		self.M_Frame.grid(row = 0, column = 0, columnspan = 2, pady=8, sticky='W', padx=5)


		self.historyButton = Button(self.M_Frame, text = 'History Logs', activebackground='#0892d0', activeforeground='white',
		 	bd=0, relief='solid', bg='#0892d0',fg='white', highlightbackground ='#0892d0', font=('Flux Regular', 10, 'bold'),
		 	cursor='hand2', command = self.logHistoryToConsole)
		self.historyButton.grid(row=0, column = 0, padx=10, pady=5, ipadx=15)

		self.action = StringVar()
		self.action.set("Renamer")
		self.actionSelection = OptionMenu(self.M_Frame, self.action, "Rename", "Zipper")
		self.actionSelection.configure(activebackground='#0892d0', activeforeground='white', bd=0, relief='solid',cursor='hand2',
			bg='#0892d0',fg='white', highlightbackground='#0892d0', font=('Flux Regular', 10, 'bold'))
		self.actionSelection['menu'].configure(activebackground='#0892d0', activeforeground='white', bd=0, relief='solid',
			bg='#222222',fg='white', font=('Flux Regular', 10, 'bold'))
		self.actionSelection.grid(row=0, column=2, padx=10, ipadx=15)


		self.helpButton = Button(self.M_Frame, text = 'Help \u24D8', activebackground='#0892d0', activeforeground='white', bd=0, relief='solid',
			bg='#0892d0',fg='white', highlightbackground='#0892d0', font=('Flux Regular', 10, 'bold'), cursor='hand2',
			command= self.showHelp)
		self.helpButton.grid(row = 0, column=3, padx=10, ipadx=15)

	def validatePath(self):
		aliasName = self.diskAliasVar.get()
		path = self.diskPathVar.get()
		if aliasName == '' and path == '' :
			messagebox.showwarning('Warning!', "Please don't leave fields empty")
		else:
			try:
				os.listdir(path)
				config = configparser.ConfigParser()
				config.read('./packages/config.ini')
				if 'LINUX_LOCAL_DISKS' in config:
					config['LINUX_LOCAL_DISKS'][aliasName] = path
					with open('./packages/config.ini', 'w') as configFile:
						config.write(configFile)

				else:
					print('ELSE')
					config['LINUX_LOCAL_DISKS'] = { aliasName: path }
					with open('./packages/config.ini', 'w') as configFile:
						config.write(configFile)
				messagebox.showinfo('Success', f'Disk {aliasName} added successfully!')
			except FileNotFoundError:
				messagebox.showerror('No such directory!', 'Please provide valid directory path, this path is not valid')
				self.diskAlias.delete(0, END)
				self.diskPath.delete(0, END)
			
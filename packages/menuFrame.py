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
		 	bd=0, relief='solid', bg='#222222',fg='white', highlightbackground ='#0892d0', font=('Flux Regular', 10, 'bold'),
		 	cursor='hand2', command = self.logHistoryToConsole)
		self.historyButton.grid(row=0, column = 0, padx=10, pady=5, ipadx=15)

		self.localDiskSelection = Button(self.M_Frame, text = 'Save Local Disks', activebackground='#0892d0', bd=0, relief='solid',
			activeforeground='white', bg='#222222',fg='white', highlightbackground='#0892d0', cursor='hand2', 
			 font=('Flux Regular', 10, 'bold'), command = self.saveLocalDisks)
		self.localDiskSelection.grid(row = 0, column=1, padx=10, pady=2, ipadx=15)


		self.action = StringVar()
		self.action.set("Renamer")
		self.actionSelection = OptionMenu(self.M_Frame, self.action, "Rename", "Zipper")
		self.actionSelection.configure(activebackground='#0892d0', activeforeground='white', bd=0, relief='solid',cursor='hand2',
			bg='#222222',fg='white', highlightbackground='#0892d0', font=('Flux Regular', 10, 'bold'))
		self.actionSelection['menu'].configure(activebackground='#0892d0', activeforeground='white', bd=0, relief='solid',
			bg='#222222',fg='white', font=('Flux Regular', 10, 'bold'))
		self.actionSelection.grid(row=0, column=2, padx=10, ipadx=15)


		self.helpButton = Button(self.M_Frame, text = 'Help \u24D8', activebackground='#0892d0', activeforeground='white', bd=0, relief='solid',
			bg='#222222',fg='white', highlightbackground='#0892d0', font=('Flux Regular', 10, 'bold'), cursor='hand2',
			command= self.showHelp)
		self.helpButton.grid(row = 0, column=3, padx=10, ipadx=15)

	def saveLocalDisks(self):

		if sys.platform == 'win32':
			messagebox.showinfo('Access Deinied!', 'This option is only available for linux users, for windows all directories are automatically calculated')
			return
		
		root = Toplevel()
		root.title('Settings')
		root.geometry('500x300')
		root.configure(bg='#222222')
		root.update_idletasks()
		root.attributes('-topmost', 0)
		root.minsize(500, 300)
		root.maxsize(500, 300)
		# Gets the requested values of the height and widht.
		windowWidth = 500
		windowHeight = 300


		# Gets both half the screen width/height and window width/height
		positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)

		# Positions the window in the center of the page.
		root.geometry("+{}+{}".format(positionRight, positionDown))

		Grid.columnconfigure(root, 0, weight=1)

		displayFrame = Frame(root, bg='#222222')
		displayFrame.grid(row=0, column=0, sticky='ew')
		Grid.columnconfigure(displayFrame, 0, weight=1)
		Grid.columnconfigure(displayFrame, 1, weight=1)

		self.diskAliasVar = StringVar()
		self.diskAlias = Entry(displayFrame, textvariable=self.diskAliasVar)
		self.diskAlias.grid(row=0, column=0, sticky='ew', padx=(5, 5), pady=(5, 0))


		self.diskPathVar = StringVar()
		self.diskPath = Entry(displayFrame, textvariable=self.diskPathVar)
		self.diskPath.grid(row=0, column=1, sticky='ew', padx=(5, 5), pady=(5, 0))


		saveButton = Button(displayFrame, text='Save', justify='center', bg='#32cd32', fg='black', cursor='hand2',
			font=('Flux Regular', 10, 'bold'), highlightthickness='0', bd=0, relief='solid', activebackground='#32cd32',
			command = self.validatePath)
		saveButton.grid(row=1, column=0, columnspan=2, sticky='ew', padx=(25, 25), pady=(5, 5))

		smallTip = Label(displayFrame, text='Click on Save Button every time you fill both the fields', justify='left',
			fg='#FFE338', bg='#222222')
		smallTip.grid(row=2, column=0, columnspan=2, sticky='ew', ipadx=10, pady=(10, 10))

		instructionFrame = LabelFrame(displayFrame, text='Instructions', height=50, labelanchor='n', bg='#222222',
		 fg='#ff0000', font=('Flux Regular', 15, 'bold'))
		instructionFrame.grid(row=3, column=0, columnspan=2, sticky='ew')
		Grid.columnconfigure(instructionFrame, 0, weight=1)
		root.update_idletasks() # To update all the idle tasks

		instructionText = 'Above you must be seeing two entry box out of which, left side is used to mention alias name for that respective path and right side is used to mention path to that directory. Now you must be wondering what exactly is alias name ? so here is your answer to this question. Alias name is nothing but the name which you will be reading when you will start browsing. Like for e.g Local Disk1, Local Disk2, Local Disk3 etc. which are the main directories from which you will be choosing folders to rename'
		instructionLabel = Label(instructionFrame, text=instructionText, wraplength=instructionFrame.winfo_width()-30,
			fg='white', font=('Flux Regular', 10, 'bold'), bg='#222222')
		instructionLabel.grid(row=0, column=0)

		root.mainloop()	

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
			
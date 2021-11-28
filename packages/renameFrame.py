from functools import partial
from configparser import ConfigParser
from tkinter import *
from tkinter import messagebox
from tkinter import Listbox
from tkinter import ttk
# from ttkthemes import ThemedTk
import os

from .navigator import Navigator
from .consoleStatusFrame import ConsoleStatusFrame
from .menuFrame import MenuFrame
from .helpFrame import HelpFrame

class RenameFrame(Navigator, ConsoleStatusFrame, MenuFrame, HelpFrame):

	browsed_path = ''

	def __init__(self, win):

		# This line is use to invoke the init method of ConsoleStatusFrame
		ConsoleStatusFrame.__init__(self, win)
		MenuFrame.__init__(self, win)

		self.win = win
		win.update_idletasks() 

		width = (win.winfo_width() // 2)
		height = win.winfo_height()


		# Instance variable declarations
		# self.browsed_path = ''
		self.customNameList = {}
		self.renameAction = 'Default'

		# Setting variable of Radio buttons present in 4th row because it won't work as it will disappear at the
		#  end of the function leaving the RadionButton with no place to store its state
		self.radioButtonStatus = IntVar() 
		self.ignoreFileWhileRenaming = []

		

		# This is main frame inside which we will be defining all frames, widgets and we will be returning this Frame
		self.R_Frame = Frame(win, width=width, height=height-50, bg='#222222', highlightcolor='white',relief='solid')
		self.R_Frame.grid(row = 1, column = 0)
		self.R_Frame.grid_propagate(0)
		Grid.columnconfigure(self.R_Frame, 0, weight = 1)
		Grid.rowconfigure(self.R_Frame, 0, weight = 1)


		# The update() and update_idletask() methods are useful for processing any pending or idle tasks
		win.update_idletasks() 




		# This Is LabelFrame which is used to display all the features 
		self.R_FrameContent = LabelFrame(self.R_Frame, text='Bunch Renamer', width=width, height = height, bg='#222222',
		 fg='white', font=('Flux Regular', 20, 'bold'))
		self.R_FrameContent.grid(padx=10, pady=10, ipady=20, ipadx=20)
		self.R_FrameContent.grid_propagate(0)

		# self.R_FrameContet configurations
		Grid.columnconfigure(self.R_FrameContent, 1, weight = 2)



		# This Frame is used to display files which are selected to rename
		self.selectedFilesFrame = LabelFrame(self.R_FrameContent, text = 'Selected Files', labelanchor = 'n', bg='#222222', fg='white',
			font=('Flux Regular', 10, 'bold'))
		self.selectedFilesFrame.grid(row = 4, column = 0, columnspan = 3, padx=15, pady= (10, 10), sticky='ew')
		Grid.columnconfigure(self.selectedFilesFrame, 1, weight=1)




		global pathVal

		# First Row start

		lb = Label(self.R_FrameContent, text='Selected Folder: ',bg='#222222', fg='white', font=('Flux Regular', 10, 'bold'),
			width='15')
		lb.grid(row=0, column=0, pady=5, padx=2)


		pathVal = StringVar()
		pathVal.set("No Folder Selected")
		entry = Entry(self.R_FrameContent, textvariable=pathVal, bd=0, relief = 'solid')
		entry.grid(row=0, column=1, padx=2, ipadx=5, ipady=2 , sticky="ew")
		entry.bind("<Button-1>", lambda e: "break") #Adding mouse left button binding to prevent user from changing field value
		# entry.grid_propagate(0)

		browseButton = Button(self.R_FrameContent, text = 'Browse', activebackground='tomato', activeforeground='white', bd=0, relief='solid',
			bg='tomato',fg='white', highlightbackground='tomato', font=('Flux Regular', 10, 'bold'), width=10,
			cursor='hand2',	command= self.startBrowsing)
		browseButton.grid(row=0, column=2, pady=5, padx=2)

		# First Row end		




		# Second and ThirdRow start
		global statusValue
		global filesValue

		# total number of files/ Status/ Encountered extensions/ 
		currStatus = Label(self.R_FrameContent, text='Current Status: ', bg='#222222', fg='white', font=('Flux Regular', 10, 'bold'))
		currStatus.grid(row=1, column=0, padx=10, pady=(10, 5))

		statusValue = Label(self.R_FrameContent, text='Not Started', bg='#222222', fg='grey', font=('Flux Regular', 10, 'bold'))
		statusValue.grid(row=1, column=1, padx=5, pady=(10, 5), sticky='w')

		files = Label(self.R_FrameContent, text='Number of Files \nencountered: ', bg='#222222', fg='white', font=('Flux Regular', 10, 'bold'))
		files.grid(row=2, column=0, padx=10, pady=(5, 10))

		filesValue = Label(self.R_FrameContent, text='0 files found', bg='#222222', fg='grey', font=('Flux Regular', 10, 'bold'))
		filesValue.grid(row=2, column=1, padx=5, pady=(5, 10), sticky='w')

		# Second and Third Row end










		# Fourth Row start

		# This frame is used for selecting actions which are default, custom prefix and custom name
		self.actionSelectionFrame = LabelFrame(self.R_FrameContent, text = 'Select Action', labelanchor = 'n', bg='#222222', fg='white',
			font=('Flux Regular', 10, 'bold'))
		self.actionSelectionFrame.grid(row = 3, column = 0, columnspan = 3, padx=15, pady= (10, 10), sticky='ew')


		# self.actionSelectionFrame configurations
		Grid.columnconfigure(self.actionSelectionFrame, 0, weight = 2)
		Grid.columnconfigure(self.actionSelectionFrame, 1, weight = 2)
		Grid.columnconfigure(self.actionSelectionFrame, 2, weight = 2)

		self.radioButtonStatus.set(1)
		rb1 = Radiobutton(self.actionSelectionFrame, text='Default Prefix', variable=self.radioButtonStatus, font=('Flux Regular', 10, 'bold'),
		 value= 1, cursor='hand2', command=partial(self.changeRenameAction, 'Default'))
		rb1.grid(row=0, column=0, ipady=5, ipadx=5, padx=5, pady=(10, 10) , sticky="ew")

		rb2 = Radiobutton(self.actionSelectionFrame, text='Custom Prefix', variable=self.radioButtonStatus, font=('Flux Regular', 10, 'bold'), 
			value= 2, cursor='hand2', command=partial(self.changeRenameAction, 'CustomPrefix'))
		rb2.grid(row=0, column=1, ipady=5, ipadx=5, padx=5, pady=(10, 10) , sticky="ew")

		rb3 = Radiobutton(self.actionSelectionFrame, text='Custom File Name ', variable=self.radioButtonStatus, font=('Flux Regular', 10, 'bold'),
		 	value= 3, cursor='hand2', command=partial(self.changeRenameAction, 'CustomName'))
		rb3.grid(row=0, column=2, ipady=5, ipadx=5, padx=5, pady=(10, 10) , sticky="nsew")

		# Fourth Row end







		# Fifth Row start
		global fileList

		self.fileList = Listbox(self.selectedFilesFrame, bg='#222222', fg='white', font=('Flux Regular', 10, 'bold'), 
			bd = 0, highlightbackground='#222222', relief='solid', height=6, justify='center')
		self.fileList.grid(row= 0, column= 1, sticky='ew', pady=(10, 10), padx=(5, 5))
		self.fileList.insert(END, 'No files to display')

		self.fileList.bind('<Button-3>', self.rightClickMenu)
		# Fifth Row end




		# Sixth Row start

		# This Frame is used to handle custom name feature 
		self.customNameFrame = LabelFrame(self.R_FrameContent, text = 'Custom Name', labelanchor = 'n', bg='#222222', fg='white',
			height=150, font=('Flux Regular', 10, 'bold'))
		# self.customNameFrame.grid(row = 5, column = 0, columnspan = 3, padx=10, sticky='ew')
		Grid.columnconfigure(self.customNameFrame, 0, weight=1)
		Grid.columnconfigure(self.customNameFrame, 1, weight=1)

		self.Replacing = Entry(self.customNameFrame)
		self.Replacing.grid(row=0, column=0, padx=5, sticky='ew' )
		self.Replacing.insert(0, 'Check help to see how to use Custom Name feature ')

		self.Replacor = Entry(self.customNameFrame)
		self.Replacor.grid(row=0, column=1, padx=5, sticky='ew' )
		self.Replacor.insert(0, 'Check help to see how to use Custom Name feature ')

		self.addedNamesField = Text(self.customNameFrame, height=5)
		self.addedNamesField.insert(END, 'Added custom names will be displayed here\n')
		self.addedNamesField.bind("<Button-1>", lambda e: "break")
		self.addedNamesField.bind("<Key>", lambda e: "break")
		self.addedNamesField.grid(row=1, column=0, columnspan=4, pady=(10, 10),padx=(10, 10), ipady=5, ipadx=5, sticky='ew' )
		
		self.valueAdder = Button(self.customNameFrame, text='Add Field', bd = 0, relief='solid',
			cursor='hand2',bg='#0892d0', fg='white', highlightthickness=1, highlightbackground='#0892d0',
			activebackground='#0892d0', activeforeground='white', command=partial(self.handleCustomName, 'add'))
		self.valueAdder.grid(row=0, column=2, pady=(5, 10), padx=10, ipadx=10, ipady=2)

		self.valueRemover = Button(self.customNameFrame, text='Remove Field', bd = 0, relief='solid',
			cursor='hand2',bg='#0892d0', fg='white', highlightthickness=1, highlightbackground='#0892d0',
			activebackground='#0892d0', activeforeground='white', command=partial(self.handleCustomName, 'remove'))
		self.valueRemover.grid(row=0, column=3, pady=(5, 10), padx=5, ipadx=10, ipady=2)

		# Sixth Row end


		# Sixth Row Start
		
		# This Frame is used to handle Custom Prefix feature
		self.customPrefixFrame = LabelFrame(self.R_FrameContent, text = 'Custom Prefix', labelanchor = 'n', bg='#222222', fg='white',
			height=150, font=('Flux Regular', 10, 'bold'))
		# self.customPrefixFrame.grid(row = 5, column = 0, columnspan = 3, padx=10, sticky='ew')
		Grid.columnconfigure(self.customPrefixFrame, 0, weight=1)


		self.customPrefixInput = Entry(self.customPrefixFrame)
		self.customPrefixInput.grid(row = 0, column=0, sticky='ew', padx=(5, 5), pady=(5, 5))

		self.customPrefixSaveButton = Button(self.customPrefixFrame, text='Add Prefix', bd = 0, relief='solid',
			cursor='hand2',bg='#0892d0', fg='white', highlightthickness=1, highlightbackground='#0892d0',
			activebackground='#0892d0', activeforeground='white')
		self.customPrefixSaveButton.grid(row = 0, column=1, padx=(5, 5), pady=(5, 5))
		
		# Sixth Row end



		# Seventh Row start

		rename = Button(self.R_FrameContent, text='Start Renaming', activebackground='tomato', activeforeground='white', bd=0, 
			relief='solid', bg='#0892d0',highlightthickness = 0, fg='white', font=('Flux Regular', 10, 'bold'),
			cursor='hand2', command=self.startRenaming)
		rename.grid(row = 6, columnspan=3, sticky='ew', padx=15, pady=20)

		# Seventh Row end	



		self.rightClickMenu = Menu(self.selectedFilesFrame, tearoff = 0)


	def handleCustomName(self, action):
		if action == 'add':

			replacing = self.Replacing.get()
			replacor = self.Replacor.get()

			if len(replacing) == 0:
				messagebox.showerror('ERROR!', 'Please use proper renaming conventions/rules. Click on help button to see how to use custom name feature')
			elif replacing == " ":
				resp = messagebox.askyesno('Confirm', "You have selected 'space' to be replaced from a filename. Do you want to replace a space, if yes then all the spaces in the filename will be replaced with whatever you will be choosing")
				if resp:
					# Before making changes to replacing and replacor variables to show it in the listbox, we will be saving it 
					# in a varaible so that we can use it while renaming
					self.customNameList[replacing] = replacor
					replacing = 'spaces'
					if replacor == "":
						replacor = f'nothing[means all {replacing} will be removed from filename]'
					self.addedNamesField.insert(END, f'>> all {replacing} will be replaced with {replacor}\n')
				else:
					return
			else:
				# Before making changes to replacing and replacor variables to show it in the listbox, we will be saving it 
				# in a varaible so that we can use it while renaming
				self.customNameList[replacing] = replacor

				if replacor == "":
					replacor = f'nothing[means all {replacing} will be removed from filename]'
				self.addedNamesField.insert(END, f'>> all {replacing} will be replaced with {replacor}\n')
		else:
			try:
				removedList = self.customNameList.popitem()
				self.addedNamesField.insert(END, f'>> REMOVED: {removedList[0]} - {removedList[1]}\n')
			except KeyError:
				messagebox.showinfo('Msg', 'Nothing to remove')


	def updateFields(self, path):
		global pathVal, filesValue, statusValue

		# Changing status value to Not started as well its color to grey
		statusValue.configure(text ='Not Started', fg='grey')


		# Saving path to class variable
		RenameFrame.browsed_path = path

		# Setting number of files[value] in 3rd row 
		noOfFiles = noOfFolders = 0
		lst = os.listdir(path)
		for file in lst:
			if os.path.isdir(path + '/' + file):
				noOfFolders += 1
			else:
				noOfFiles += 1
		filesValue.configure(text = f'{noOfFolders} Folders and {noOfFiles} Files')

		# Setting path value for [Selected Folder] Field which is an entry filed in first row
		pathVal.set(path) 

		# First Clearing the list ensuring that the list is empty before inserting new list values
		self.fileList.delete(0, END)

		# Configuring justify value of [self.fileList] widget to left and inserting new values
		self.fileList.configure(justify='left')
		files = os.listdir(path)
		for i in range(len(files)):
			self.fileList.insert(i, files[i])


	def startBrowsing(self):
		self.innitiateNavigationSystem()

	def changeRenameAction(self, action):
		self.renameAction = action
		if action == 'CustomPrefix':
			self.customNameFrame.grid_forget()
			self.customPrefixFrame.grid(row = 5, column = 0, columnspan = 3, padx=10, sticky='ew')
		elif action == 'CustomName':
			self.customPrefixFrame.grid_forget()
			self.customNameFrame.grid(row = 5, column = 0, columnspan = 3, padx=10, sticky='ew')
		else:
			self.customNameFrame.grid_forget()
			self.customPrefixFrame.grid_forget()


	def startRenaming(self):
		resp = messagebox.askyesno('Confirmation', 'Do you want to start renaming ?')
		if not resp:
			return

		global statusValue

		# Clearing the console if we already having entries
		self.logToConsole('', 'delete')

		# Checking if the user have selected CustomPrefix feature and not fields are added yet to the program will
		# prompt telling user that you haven't entered any fields yet, if you still want to proceed by default 'file'
		# prefix will be added to files if you want to abort renaming process then click on 'No'
		if self.renameAction == 'CustomName' and len(self.customNameList) == 0:
			resp = messagebox.askyesno('Warning', "WARNING! You haven't added any fileds yet, if you still wish to proceed then you can click 'Yes' in which case 'file' prefix will be added to all renamed files, click 'No' if you want to abort renaming process")
			if resp:
				self.renameAction = 'Default'
			else:
				return

		if RenameFrame.browsed_path == "":
			messagebox.showerror('Empty Path ERROR!', 'Please browse and select a folder to rename')
		else:
			file_list = os.listdir(RenameFrame.browsed_path)

			if self.renameAction == 'Default':
				prefixVal = 'file'
				num = 1
				for file in file_list:
					if os.path.isfile(RenameFrame.browsed_path + '/' + file):
						extension = file.split('.')[-1]
						os.rename(RenameFrame.browsed_path + '/' + file, RenameFrame.browsed_path + '/' + prefixVal + ' ' + str(num) + '.' + extension)
						newFilename = prefixVal + ' ' + str(num) + '.' + extension
						self.logToConsole(f'>> {file} is renamed to {newFilename}')
						num += 1

				# Changing status value from 'Not started' to 'Complted'
				statusValue.configure(text ='Completed', fg='#48A14D')

				self.logToConsole('')
				self.logToConsole('>> Renaming Completed Successfully')
				self.saveLogsToHistory()


			elif self.renameAction == 'CustomPrefix':
				prefixVal = self.customPrefixInput.get()
				if prefixVal == "":
					resp = messagebox.askyesno('Empty Prefix value', "If you leave Prefix value empty, by default program will use 'file' as prefix")
					if resp:
						prefixVal = 'file'
					else:
						return 
				num = 1
				for file in file_list:
					if os.path.isfile(RenameFrame.browsed_path + '/' + file):
						extension = file.split('.')[-1]
						os.rename(RenameFrame.browsed_path + '/' + file, RenameFrame.browsed_path + '/' + prefixVal + ' ' + str(num) + '.' + extension)
						newFilename = prefixVal + ' ' + str(num) + '.' + extension
						self.logToConsole(f'>> {file} is renamed to {newFilename}')
						num += 1

				# Changing status value from 'Not started' to 'Completed'
				statusValue.configure(text ='Completed', fg='#48A14D')

				self.logToConsole('')
				self.logToConsole('>> Renaming Completed Successfully')
				self.saveLogsToHistory()


			elif self.renameAction == 'CustomName':
				print(self.customNameList)
				for file in file_list:
					if os.path.isfile(RenameFrame.browsed_path + '/' + file):
						newFilename = file
						for key in self.customNameList:
							newFilename = newFilename.replace(key, self.customNameList[key])
						os.rename(RenameFrame.browsed_path + '/' + file, RenameFrame.browsed_path + '/' + newFilename)
						self.logToConsole(f'>> {file} is renamed to {newFilename}')

				# Changing status value from 'Not started' to 'Complted'
				statusValue.configure(text ='Completed', fg='#48A14D')

				self.logToConsole('')
				self.logToConsole('>> Renaming Completed Successfully')
				self.saveLogsToHistory()
			

	def logHistoryToConsole(self):
		self.logToConsole('', 'delete')
		with open('./packages/history.txt', 'r') as file:
			for line in file:
				self.logToConsole(line)


	def showHelp(self):
		self.initiateHelpWindow()
		
	def rightClickMenu(self, event):

		if self.fileList.curselection() == ():
			return
		
		# Checking if any list item is selected, if it's not then we will just return else we will 
		# proceed with execution
		selectionIndex = self.fileList.curselection()[0]
		selectionText = self.fileList.get(selectionIndex, selectionIndex)[0]
		print(selectionIndex, selectionText)

		print(self.ignoreFileWhileRenaming)
		# Before creating menu we will clear the menu items we inserted earlier so that there won't be 
		# any memory leack
		self.rightClickMenu.delete(0, END)

		# We will add menu items
		self.rightClickMenu.add_command(label='Copy Text', command=self.fileList.event_generate('<<Copy>>'))
		self.rightClickMenu.add_command(label='Remove from list',
			command = partial(self.rightClickMenuAcion, 'Remove', selectionText, selectionIndex))

		state = 'disabled' if self.ignoreFileWhileRenaming == [] else 'normal'
		self.rightClickMenu.add_command(label='Undo', state=state, 
			command= partial(self.rightClickMenuAcion, 'Undo'))
		self.rightClickMenu.add_command(label = 'Refresh', state=state,
			command = partial(self.rightClickMenuAcion, 'Refresh'))

		
		# tk_popup is very help full to remove menu when clicked elsewhere
		self.rightClickMenu.tk_popup(event.x_root, event.y_root)

	def rightClickMenuAcion(self, action='', selectionText='', selectionIndex=''):
		if action == 'Remove':
			self.ignoreFileWhileRenaming.append(selectionText)
			self.fileList.delete(selectionIndex, selectionIndex)
		elif action == 'Undo':
			self.fileList.insert(END, self.ignoreFileWhileRenaming[-1])
			self.ignoreFileWhileRenaming.pop()
		elif action == 'Refresh':
			for entry in self.ignoreFileWhileRenaming:
				self.fileList.insert(END, entry)
			self.ignoreFileWhileRenaming = []
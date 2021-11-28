from functools import partial
from tkinter import *
from tkinter import messagebox
from tkinter import Listbox
from tkinter import ttk
import os

class HelpFrame:

	def __init__(self):
		pass

	def initiateHelpWindow(self):
		self.helpRootWindow = Tk()
		self.helpRootWindow.title('HELP')
		self.helpRootWindow.configure(bg='#222222')
		self.helpRootWindow.resizable(False, False)
		# self.helpRootWindow.bind('<Configure>', self.resize)
		Grid.columnconfigure(self.helpRootWindow, 0, weight=1)



		
		textValue = ['Help with browse [Local Disks not showing]',
					 'Added local disk but still not showing while browsing',
					 'Understanding Default Prefix Feature',
					 'Understanding Custom Prefix Feature',
					 'Understanding Custom Name Feature'
		]
		commands = []

		for i in range(len(textValue)):
			helpBtn= Button(self.helpRootWindow, text=textValue[i], bg='#222222',
			fg='tomato', font=('Flux Regular', 12, 'bold'), activebackground='tomato', bd=0, relief='solid', 
			activeforeground='white', cursor='hand2', highlightthickness=1, highlightbackground='red')
			helpBtn.grid(row=i, column=0, sticky='ew', pady=(5, 5))

		self.helpRootWindow.update()
		
		windowWidth = self.helpRootWindow.winfo_width()
		windowHeight = self.helpRootWindow.winfo_height()

		print(windowWidth, windowHeight)

		# Gets both half the screen width/height and window width/height
		positionRight = int(self.helpRootWindow.winfo_screenwidth()/2 - windowWidth/2)
		positionDown = int(self.helpRootWindow.winfo_screenheight()/2 - windowHeight/2)

		self.helpRootWindow.geometry(f'{windowWidth}x{windowHeight}+{positionRight}+{positionDown}')

		self.helpRootWindow.mainloop()
		pass



	def displayHelpFrame1(self):
		self.helpWindow = Tk()
		self.helpWindow.title('HELP')
		self.helpWindow.attributes('-zoom', True)
		self.helpWindow.configure(bg='#222222')
		self.helpWindow.resizable(True, True)
		self.helpWindow.bind('<Configure>', self.resize)
		Grid.columnconfigure(self.helpWindow, 0, weight=1)


		# Main frame to display all the help required for renaming process
		renameFrameHelp = LabelFrame(self.helpWindow, text='Help For Rename Frame', height=50, fg='tomato',bg='#222222',
			font=('Flux Regular', 20, 'bold'), labelanchor='n')
		renameFrameHelp.grid(row=0, column=0, sticky='ew')
		Grid.columnconfigure(renameFrameHelp, 0, weight=1)

		self.browseHelp = LabelFrame(renameFrameHelp, text='Help with browse [Local Disks not showing]', fg='tomato',
		 bg='#222222', font=('Flux Regular', 12, 'bold'))
		self.browseHelp.grid(row=0, column=0, sticky='ew', padx=(10, 10), pady=(10, 10))
		Grid.columnconfigure(self.browseHelp, 0, weight=1)

		self.BH_text1_message = 'In case of Windows, the software will automatically compute the local disks present in the sytem and will show you when you click on browse, but thats not the case in linux distros. If you are using one of the linux distros then you have to mannually do some settings to Browse.'

		self.helpWindow.update_idletasks() # This line updates all the idle tasks so that we can get widtho fo self.browseHelp Frame
		self.BH_text1 = Label(self.browseHelp, text=self.BH_text1_message, wraplength=self.browseHelp.winfo_width(),
			justify='left', bg='#222222', fg='white')
		self.BH_text1.grid(row=0, column=0, sticky='ew')

		self.helpWindow.mainloop()

		# def resize(self, event):
	# 	try:
	# 		self.BH_text1 # Checking if the program have mounted this widget in fram, if not then it will throw 'AttributeError' and in except block we will just pass without performing anything
	# 	except:
	# 		pass
	# 	else: # So when try block is executed without any errors that means that all the widgets are mounted in respective frame and now we can configure it
	# 		self.helpWindow.update_idletasks()
	# 		self.BH_text1.configure(wraplength=self.browseHelp.winfo_width())
	# 		print(event.width)

if __name__ == '__main__':
	obj = HelpFrame()
	obj.initiateHelpWindow()
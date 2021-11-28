from functools import partial
from configparser import ConfigParser
from tkinter import *
from tkinter import messagebox
from tkinter import Listbox
from tkinter import ttk
import os

from packages.renameFrame import RenameFrame
from packages.menuFrame import MenuFrame
from packages.consoleStatusFrame import ConsoleStatusFrame

class Rename():

	def __init__(self, renameRootWindow):

		#  Configuring root window settings 
		renameRootWindow.configure(background = '#222222')
		if sys.platform == 'linux':
			renameRootWindow.attributes('-zoomed', True)
		else:
			renameRootWindow.state('zoomed')
		renameRootWindow.title('Rename 0.1')


	def initializeWindow(self):
		# M_Frame = MenuFrame.createMenuFrame(self, renameRootWindow)

		R_Frame = RenameFrame(renameRootWindow)

		# CS_Frame = ConsoleStatusFrame(renameRootWindow)
		# CS_Frame.createConsoleStatusFrame()


if __name__ == "__main__":

	renameRootWindow = Tk()

	# Creating instance of Rename class
	rename = Rename(renameRootWindow)

	# Initiating initializeWindow function of Rename class to start window
	rename.initializeWindow()

	renameRootWindow.mainloop()


# Upcoming features
# 1) Keyboard interactions while browsing
# 2) Right click options
# 3) Optimizing Browing window 
from functools import partial
from configparser import ConfigParser
from tkinter import *
from tkinter import messagebox
from tkinter import Listbox
import os, sys, string
from tkinter import ttk
# from ttkthemes import ThemedTk

from .validator import Validator


class Navigator(Validator):

    def __init__(self, win, renameFrameOBJ):
        self.win = win
        self.renameFrameOBJ = renameFrameOBJ
        self.completedKeyInteractionEntries = []
        self.currentSelectedValue = 0
        
        # Configuring windows
        if sys.platform == 'linux':
            win.attributes('-zoom', True)
        else:
            win.state('zoomed')
            
        win.title('Dialog Box')
        win.grid_columnconfigure(0,weight=1)
        win.grid_rowconfigure(1, weight=1)
        win.configure(background='#222222')

        # Saving system value
        self.system = sys.platform

        # initializing configParser for storing settings

        self.config_object = ConfigParser()

        # Initializing object attributes 

        self.path_list = {}
        self.forward_path = []
        self.path_history = ['/media/hackytech/'] if self.system == 'linux' else ['ROOT']


        # Setting back button, forward button, and path entry 
        BF_Frame = Frame(win, bg='#222222')
        BF_Frame.grid(column= 0 , row = 0, pady = 5, padx= 5)


        self.backButton = Button(BF_Frame, text='Back',width='15', cursor='X_cursor', state='disabled',
            bg='#444444', fg='white', bd='0', relief='solid', highlightbackground='#444444', activebackground='#375a7f', activeforeground='white',
            font=('', 10, 'bold'),command=partial(self.displayFiles, '', 'backward'))
        self.backButton.grid(column=0, row=0, sticky='W', padx=3)

        self.forwardButton = Button(BF_Frame, text='Forward',width='15', cursor='X_cursor', state='disabled',
            bg='#444444', fg='white', bd='0', relief='solid', highlightbackground='#444444', activebackground='#375a7f', activeforeground='white',
            font=('', 10, 'bold'),command=partial(self.displayFiles, '', 'forward'))
        self.forwardButton.grid(column=1, row=0, sticky='E', padx=3)


        self.currpathLabel = Entry(BF_Frame, text='Current No path', width='90')
        self.currpathLabel.grid(column = 2, row= 0, sticky='W', padx=3)


        self.selectButton = Button(BF_Frame, text='Select current folder',
        bg='tomato', bd='0', relief='solid', activebackground='#e74c3c', fg='white', font=('Flux Regular', 10, 'bold'),
        highlightbackground='#444444', activeforeground='white',cursor='hand2' ,command= self.selectCurrentFolder)
        self.selectButton.grid(column =3 , row = 0, padx=3, ipadx=5, ipady=2)



        # Initializing List Frame to display file names
        listFrame = Frame(win, bg='#222222')
        listFrame.grid(row=1, column=0, sticky='nsew')
        Grid.columnconfigure(listFrame, 0, weight=1)

        listFrame.update()

        width = listFrame.winfo_width() // 16
        self.listBox = Listbox(listFrame, width=width, height= 20,justify='center', font=('Flux Regular', 15),
            fg='white', selectbackground='#375a7f', selectforeground='white', bg='#222222', bd = 0,
            activestyle='none', highlightthickness=0)
        self.listBox.grid(ipadx=10, ipady=10)


        # binding keyboard and mouse events to frames and buttons
        self.listBox.bind('<Double-Button-1>', self.displayFiles)
        self.listBox.bind('<Return>', self.displayFiles)
        self.listBox.bind('<KP_Enter>', self.displayFiles)
        self.currpathLabel.bind('<Return>', self.displayFiles)
        self.currpathLabel.bind('<KP_Enter>', self.displayFiles)
        win.bind('<Key>', self.triggerBackButton)


    def triggerBackButton(self, event):
        # Clearing all the selections if we are going to use interactive keyboard feature, so that if will 
        # re select a new one instead of selecting the previous selection as well as the current selection
        self.listBox.selection_clear(0, END)

        if event.char == '':
            self.backButton.invoke()
        elif event.keysym == 'Up':
            print(self.currentSelectedValue)
            if self.currentSelectedValue:
                self.currentSelectedValue -= 1
                self.listBox.selection_set(self.currentSelectedValue, self.currentSelectedValue)
            else:
                self.currentSelectedValue = 1
                self.listBox.selection_set(0, 0)
        elif event.keysym == 'Down':
            if self.currentSelectedValue:
                self.currentSelectedValue += 1
                self.listBox.selection_set(self.currentSelectedValue, self.currentSelectedValue)
            else:
                self.currentSelectedValue = 1
                self.listBox.selection_set(0, 0)
        else:
            if event.char in string.ascii_lowercase:
                if self.path_history[-1] == 'ROOT':
                    return
                files = os.listdir(self.path_history[-1])
                for idx in range(len(files)):
                    if files[idx][0].lower() == event.char and files[idx] not in self.completedKeyInteractionEntries:
                        self.currentSelectedValue = idx
                        self.listBox.see(idx)
                        self.listBox.selection_set(idx, idx)
                        self.completedKeyInteractionEntries.append(files[idx])
                        break


    def innitiate(self):
        global BF_Frame
        global listBox

        # Just to make sure we don't have any list items present before
        self.listBox.delete(0, END)
        self.listBox.configure(justify='center') # Reconfiguring it to display text in center for local disk 

        localDisks = 'LINUX_LOCAL_DISKS' if self.system == 'linux' else 'WINDOWS_LOCAL_DISKS'

        try:
            self.config_object.read('./packages/config.ini')
            if len(self.config_object[localDisks]) == 0:
                messagebox.showerror(title='ERROR', message='Please add localdisk names before browsing')
            else:
                r = 0
                rec = {}

                for disk in self.config_object[localDisks]:
                    self.listBox.insert(r, disk.title())
                    rec[r] = self.config_object[localDisks][disk]
                    r += 1

                self.path_list = rec
        except Exception as e:
            if self.system == 'linux':
                messagebox.showerror(title='ERROR', message='Please add localdisk Names before browsing')
            elif self.system == 'win32':
                self.initiateAutoDiskSave()

    def initiateAutoDiskSave(self):
        print(self.system)
        self.config_object['WINDOWS_LOCAL_DISKS'] = {}
        for drive in list(string.ascii_uppercase):
            try:
                os.listdir(drive + ':/')
                print(drive)
                self.config_object['WINDOWS_LOCAL_DISKS']['Local Disk ' + drive] = drive + ':/'
                
            except Exception as e:
                print(e)
                pass

        with open('./packages/config.ini', 'w') as configFile:
            self.config_object.write(configFile)

        self.innitiate()


    def selectCurrentFolder(self):
        currPath = self.path_history[-1]
        if currPath == 'ROOT':
            messagebox.showinfo(title='MESSAGE', message="Local disks can't be selected ")
        else:
            lst = os.listdir(currPath)
            if len(lst) == 0:
                messagebox.showinfo(title='MESSAGE', message='Selecting empty directory is stupidity, what exactly are you planning to rename')
            else:
                resp = messagebox.askyesno(title='MESSAGE', message ="Do you want to select this folder for renaming")
                if resp:
                    self.win.destroy()
                    self.renameFrameOBJ.updateFields(currPath)
                    # self.renameFrameOBJ is itself object of RenameFrame class definied in constructor of Navigator class


    def notAFile(self, currPath):
        extensions = ['.csv', '.mkv', '.mp3', '.zip', 'mp4', '.jpg', '.jpeg', '.png', '.docx', '.gif', '.ts']
        for extension in extensions:
            if extension in currPath:
                return False 
        return True


    def displayFiles(self, clickEvent, action=''):
        global win
        # Reinitializing self.completedKeyInteractionEntries for this current path
        self.completedKeyInteractionEntries = []

        # Reconfiguring it to display file names at left
        self.listBox.configure(justify='left')

        # this if condition checks that this fuction was trigered by Double clikc using mouse OR by pasting path 
        # in path entry and hitting enter and then validating it. So if it gives us indexError means the 
        # User pasted the path and then tried going to that path
        if action == "": 
            try:
                currPath = self.path_list[self.listBox.curselection()[0]]
            except IndexError:
                currPath = self.currpathLabel.get()
                try:
                    os.listdir(currPath)
                except FileNotFoundError:
                    messagebox.showerror('ERROR!', "Please enter valid path")
                    return 

            if self.notAFile(currPath):
                self.path_history.append(currPath)
        else:
            # Checking if this function was triggered by forward or backward button

            if action == 'backward':
                currPath = self.path_history.pop(-1)
                self.forward_path.append(currPath)

                currPath = currPath.split('/')
                while currPath.pop(-1) == "":
                    pass
                currPath = '/'.join(currPath)
                if len(self.path_history) == 1 and self.path_history[0] == 'ROOT':
                    self.innitiate()
                    self.currpathLabel.delete(0, END) # Deleting all the path entrie

                    # Configure the back and forward button based on forward_path and path_history list
                    if (len(self.forward_path) > 0):
                        self.forwardButton.configure(state = 'normal', cursor='hand2')
                    else:
                        self.forwardButton.configure(state = 'disabled', cursor='X_cursor')
                    if (len(self.path_history) > 1):
                        self.backButton.configure(state = 'normal', cursor='hand2')
                    else:
                        self.backButton.configure(state = 'disabled', cursor='X_cursor')
                    return
            else:
                currPath = self.forward_path.pop(-1)
                if currPath == "":
                    currPath = self.forward_path.pop(-1)
                self.path_history.append(currPath)


        # Setting text value of currpathLabel and also delete the previous set value 
        self.currpathLabel.delete(0, END)
        self.currpathLabel.insert(0, self.path_history[-1])


        # Configure the back and forward button based on forward_path and path_history list
        if (len(self.forward_path) > 0):
            self.forwardButton.configure(state = 'normal', cursor='hand2')
        else:
            self.forwardButton.configure(state = 'disabled', cursor='X_cursor')
        if (len(self.path_history) > 1):
            self.backButton.configure(state = 'normal', cursor='hand2')
        else:
            self.backButton.configure(state = 'disabled', cursor='X_cursor')

        try:
            folders = os.listdir(currPath)

            #  Removing previous items from list
            self.listBox.delete(0, END)
            idx = 0
            rec = {}
            for folder in folders:
                self.listBox.insert(idx, folder)
                rec[idx] = currPath + '/' + folder
                idx += 1
            self.path_list = rec
        except NotADirectoryError:
            messagebox.showerror('ERROR!', "You can't open a file, please select a folder. In future we are planning to add image viewer \u263A")

        except FileNotFoundError as e:
            if currPath == "": # Temporary fix for FileNotFoundError at specified path ""
                return
            messagebox.showerror('ERROR!', 'This directory is not present in your system')
        except PermissionError:
            messagebox.showerror('ERROR!', "You don't have permission to open this directory")


    def innitiateNavigationSystem(self):
        self.browseWin = Toplevel(self.win)
        # browseWin.attributes('-topmost', True)

        # Creating an instance of Navigator class
        self.navigate = Navigator(self.browseWin, self)

        # Invoking innitiate funtion of Navigator class
        self.navigate.innitiate()
        self.browseWin.mainloop()


# Features
# 1) Menu -> HISTORY LOG
# 2) Menu -> FONT-SIZE
# 3) Menu -> SELECT FUNTIONALITY -> ZIPPER / RENAMER
# 4) Menu -> HELP
# 5) Menu -> SAVE LOCALDISKS
# 6) console to show current situation
# 7) Custom name or Selective name


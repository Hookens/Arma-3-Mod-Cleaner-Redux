# Arma 3 Mod Cleaner
# Copyright (C) 2023  Alexein https://gitlab.com/Alexein
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import webbrowser
import amcio

from os import name
if name == "nt":                                 #set for high dpi if run on windows
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

modlists = []
neededMods = {}
extraMods = {}
whitelist = {}

def changeListPath():
    listPath = filedialog.askdirectory()
    amcio.recordSettings(newListPath = listPath)
    refresh()
    
def changeModPath():
    modPath = filedialog.askdirectory()
    amcio.recordSettings(newModPath = modPath)
    refresh()

def saveToWhitelist():
    for index in extraModsList.curselection():
        whitelist.update({extraModsList.get(index): extraMods.get(extraModsList.get(index))})
    amcio.saveToWhitelist(whitelist)
    refresh()

def removeFromWhitelist():
    removeList = []
    for index in neededModsList.curselection():
        removeList.append(neededModsList.get(index).removeprefix("*"))
    amcio.removeFromWhitelist(removeList)
    refresh()    

def unsubOne():
    messagebox.showerror("Error", "Not yet implemented")

def unsubAll():
    messagebox.showerror("Error", "Not yet implemented")

def showExtra():
    global extraMods
    extraModsList.delete(0, tk.END)
    for extraMod in sorted(extraMods.keys(), key = str.lower):
        if extraMod.startswith("*"):
            if showInvalidVar.get():
                extraModsList.insert(tk.END, extraMod)
        else:   extraModsList.insert(tk.END, extraMod)

def checkUpdate():
    webbrowser.open_new_tab("https://gitlab.com/Alexein/arma-3-mod-cleaner/-/releases")

def neededSelect(event = None):
    if len(neededModsList.curselection()) > 0:   removeFromFileButton.config(state= tk.NORMAL)
    else:   removeFromFileButton.config(state= tk.DISABLED)

def extraSelect(event = None):
    if len(extraModsList.curselection()) > 0:
        unsubOneButton.config(state= tk.NORMAL)
        saveToFileButton.config(state= tk.NORMAL)
    else:
        unsubOneButton.config(state= tk.DISABLED)
        saveToFileButton.config(state= tk.DISABLED)

def emptyHtmls():
    messagebox.showerror("Error", "No modlists found.")

def modsNotFound():
    messagebox.showerror("Error", "Mod folder not found, manual setting required.")

def refresh():
        """scan for modlist files and the contained mods"""
        global extraMods
        global modlists
        try:
            amcio.getSettings()
            modlists = amcio.searchModlists()
        except Exception:
            modsNotFound()
        modlistList.delete(0, tk.END)
        neededModsList.delete(0, tk.END)
        extraSelect()
        neededSelect()
        if len(modlists) == 0: emptyHtmls()
        else:
            neededMods, neededDlcs = amcio.readModlists(modlists)
            whitelist = amcio.readWhitelist()
            extraMods = amcio.searchMods(neededMods.values(), whitelist.values())
            for html in sorted(modlists, key= str.lower): modlistList.insert(tk.END, html.removesuffix(".html").removesuffix(".preset2"))
                #progress.set(int(((modlists.index(html)+1)/len(modlists))*100))
            for neededMod in sorted(neededMods.keys(), key= str.lower):
                if neededMod in whitelist.keys():   star = "*"
                else: star = ""
                neededModsList.insert(tk.END, star + neededMod)
            if len(whitelist.keys()) > 0:
                neededModsList.insert(tk.END, "")
                neededModsList.insert(tk.END, "                               *Whitelist*")
                for whitelistedMod in sorted(whitelist.keys()): neededModsList.insert(tk.END, "*" + whitelistedMod)
            showExtra()
            #for neededdlc

#main window
mainWindow = tk.Tk()
mainWindow.title("Arma 3 Mod Cleaner")
icon = tk.PhotoImage(file = "amc_logo.gif")
mainWindow.tk.call("wm", "iconphoto", mainWindow._w, icon)
mainWindow.rowconfigure(0, weight= 1)
mainWindow.columnconfigure(0, weight= 1)
mainFrame = ttk.Frame(mainWindow, padding= "20 20 20 5")
mainFrame.rowconfigure([*range(9)], weight = 1)
mainFrame.columnconfigure([0, 3], weight= 1, uniform= "x")
mainFrame.columnconfigure([1,2], weight= 3)
mainFrame.grid(sticky= tk.NSEW)

#modlists
modlistLabel = ttk.Label(mainFrame, text= "Modlists")
modlistLabel.grid(row= 0, column= 0)
modlistFrame = ttk.Frame(mainFrame, relief= tk.GROOVE, borderwidth= 3)
modlistFrame.grid(row=1, column= 0, rowspan= 2, sticky= tk.NSEW)
modlistFrame.columnconfigure(0, weight= 2)
modlistFrame.rowconfigure(0, weight= 2)
modlistYScroll = ttk.Scrollbar(modlistFrame, orient= tk.VERTICAL)
modlistYScroll.grid(row = 0, column= 1, sticky= tk.NS)
modlistList = tk.Listbox(modlistFrame, activestyle= "none", height = 7, width= 28, listvariable= tk.Variable(value= modlists), yscrollcommand= modlistYScroll.set, exportselection= 0)
modlistList.grid(row= 0, column= 0, sticky= tk.NSEW)
modlistYScroll['command'] = modlistList.yview()

#modlists buttons
modButtonsFrame = ttk.Frame(mainFrame)
modButtonsFrame.grid(row= 3, column= 0, rowspan= 2, sticky= tk.NSEW)
modButtonsFrame.columnconfigure(0, weight= 1)
refreshModButton = ttk.Button(modButtonsFrame, text= "Refresh", command= refresh)
refreshModButton.grid(row= 3, column= 0, pady= (20, 10), sticky= tk.EW)
changeListPathButton = ttk.Button(modButtonsFrame, text= "Change modlist directory", command=changeListPath)
changeListPathButton.grid(row= 4, column= 0, pady= (10, 10), sticky= tk.EW)
changeModPathButton = ttk.Button(modButtonsFrame, text= "Change mod directory", command= changeModPath)
changeModPathButton.grid(row= 5, column= 0,pady= (10), sticky= tk.EW)

#progress bar
#progress = tk.IntVar()
#progressBar = ttk.Progressbar(mainFrame, mode= "determinate", variable= progress)
#progressBar.grid(row= 7, column= 0, sticky= tk.EW)

#needed mods list
neededModsLabel = ttk.Label(mainFrame, text= "Needed Mods")
neededModsLabel.grid(row= 0, column= 1, padx= (20, 10))
neededModsFrame = ttk.Frame(mainFrame, relief= tk.GROOVE, borderwidth= 3)
neededModsFrame.grid(row=1, column= 1, rowspan= 4, sticky= tk.NSEW, padx= (20, 20))
neededModsFrame.rowconfigure(0, weight= 1)
neededModsFrame.columnconfigure(0, weight= 1)
neededModsYScroll = ttk.Scrollbar(neededModsFrame, orient= tk.VERTICAL)
neededModsYScroll.grid(row = 0, column= 1, sticky= tk.NS)
neededModsList = tk.Listbox(neededModsFrame, activestyle= "none", height = 16, width= 40, listvariable= tk.Variable(value= neededMods), yscrollcommand= neededModsYScroll.set, exportselection= 0, selectmode= tk.MULTIPLE)
neededModsList.grid(row= 0, column= 0, sticky= tk.NSEW)
neededModsYScroll["command"] = neededModsList.yview

#extra mods list
extraModsLabel = ttk.Label(mainFrame, text= "Extra Mods")
extraModsLabel.grid(row= 0, column= 2, padx= (10, 20))
extraModsFrame = ttk.Frame(mainFrame, relief= tk.GROOVE, borderwidth= 3)
extraModsFrame.grid(row=1, column= 2, rowspan= 4, sticky= tk.NSEW, padx= (0, 20))
extraModsFrame.columnconfigure(0, weight= 1)
extraModsFrame.rowconfigure(0, weight=1)
extraModsYScroll = ttk.Scrollbar(extraModsFrame, orient= tk.VERTICAL)
extraModsYScroll.grid(row = 0, column= 1, sticky= tk.NS)
extraModsList = tk.Listbox(extraModsFrame, activestyle= "none", height = 16, width= 40, listvariable= tk.Variable(value= extraMods), yscrollcommand= extraModsYScroll.set, exportselection= 0, selectmode= tk.MULTIPLE)
extraModsList.grid(row= 0, column= 0, sticky= tk.NSEW)
extraModsYScroll["command"] = extraModsList.yview

#extra mods buttons
extraButtonsFrame = ttk.Frame(mainFrame)
extraButtonsFrame.grid(row= 1, column= 3, rowspan= 4, sticky= tk.NSEW)
extraButtonsFrame.columnconfigure(0, weight= 1)
unsubOneButton = ttk.Button(extraButtonsFrame, text= "  Unsub extra mods ", command= unsubOne, state= tk.DISABLED)
unsubOneButton.grid(row= 0, column= 0, sticky= tk.EW, pady= (0, 20))
unsubAllButton = ttk.Button(extraButtonsFrame, text= "Unsub all extra mods", command= unsubAll)
unsubAllButton.grid(row= 1, column= 0, sticky= tk.EW, pady= (0, 20))
saveToFileButton = ttk.Button(extraButtonsFrame, text= "Whitelist extra mods", command= saveToWhitelist, state= tk.DISABLED)
saveToFileButton.grid(row= 2, column= 0, sticky= tk.EW, pady= (0, 20))
removeFromFileButton = ttk.Button(extraButtonsFrame, text= "Remove from whitelist", command= removeFromWhitelist, state= tk.DISABLED)
removeFromFileButton.grid(row= 3, column= 0, sticky= tk.EW, pady= (0, 20))
showInvalidVar = tk.BooleanVar(value= False)
showInvalidCheck = ttk.Checkbutton(extraButtonsFrame, text= "Show invalid mods", command= showExtra, variable= showInvalidVar)
showInvalidCheck.grid(row= 4, column= 0)

#mods buttons events
neededModsList.bind("<<ListboxSelect>>", neededSelect)
extraModsList.bind("<<ListboxSelect>>", extraSelect)

#additional buttons
checkUpdateButton = ttk.Button(mainFrame, text= "Check for updates", command= checkUpdate)
checkUpdateButton.grid(row= 4, column= 3, sticky= tk.S + tk.EW)
checkSiteLabel = ttk.Label(mainFrame, text= "Arma 3 Mod Cleaner by Alexein v0.9.3")
checkSiteLabel.grid(row= 7, column= 3, sticky= tk.S + tk.E)

refresh()
mainWindow.mainloop()
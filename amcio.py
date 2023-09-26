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
import os

listPath = ""
modPath = ""

def getSettings():
    """set work path from settings file or system default"""
    global listPath
    global modPath
    if os.path.exists("settings.txt"):
        with open("settings.txt") as settingsFile:
            settings = settingsFile.readlines()
            listPath = settings[0].split("=", 1)[1].rstrip()
            modPath = settings[1].split("=", 1)[1].rstrip()
            #stuff
    else:
        if os.name == "nt":                         #need to input correct paths!
            if os.path.exists("."):  listPath = "."
            if os.path.exists("."):  modPath = "."
            else:   raise FileNotFoundError("modPath")
        elif os.name == "posix":
            if os.path.exists("."):  listPath = "."
            if os.path.exists("."):  modPath = "."
            else:   raise FileNotFoundError("modPath")

def recordSettings(newListPath = "", newModPath = ""):
    global listPath
    global modPath
    if newListPath != "":   listPath = newListPath
    if newModPath != "":   modPath = newModPath    
    with open("settings.txt", "w") as settingsFile:
        settingsFile.write("listPath=" + listPath + "\n")
        settingsFile.write("modPath=" + modPath + "\n")

def searchModlists():
    """find all modlists in selected path"""
    modlists = []
    with os.scandir(listPath) as files:
        for file in files:
            if file.path.endswith(".html"):  modlists.append(file.path.removeprefix(listPath + os.sep))
    return modlists

def readModlists(htmls):
    """read all modlists, put mod and relative number together, same for dlc"""
    modlists = []
    mods = {}
    dlcs = {}
    for i in range(len(htmls)):
        with open(os.path.join(listPath, htmls[i])) as html:
            modlists.append(html.readlines())
            for j in range(len(modlists[i])):
                if j < 89: pass 
                elif modlists[i][j].startswith('          <td data-type="DisplayName">'):
                    key = modlists[i][j].removeprefix('          <td data-type="DisplayName">').split("<")[0]
                elif modlists[i][j].startswith('            <a href="'):
                    value = modlists[i][j].split('"', 2)[1]
                    if len(value.split("=")) > 1:  mods.update({key: value.split("=")[-1]})
                    else:  dlcs.update({key: value.rsplit("/", 1)[1]})
    return mods, dlcs

def readWhitelist():
    whitelistL = []
    whitelist = {}
    if os.path.exists("whitelist.txt"):
        with open("whitelist.txt") as whiteFile: 
            whitelistL = whiteFile.readlines()
            for i in range(len(whitelistL)):   
                whitelist.update({whitelistL[i].split("/")[0]: whitelistL[i].split("/")[1].rstrip()}) 
    return whitelist

def searchExtraMods(mods, whitelist):
    """check mod folder and filter the unused ones"""
    allModFolders = []
    allMods = {}
    if os.path.exists(modPath):
        with os.scandir(modPath) as files:
            for file in files:
                if file.is_dir():  allModFolders.append(file.path.removeprefix(modPath + os.sep))
    for mod in mods:
        if mod in allModFolders:  allModFolders.remove(mod)
    for mod in whitelist:
        if mod in allModFolders:  allModFolders.remove(mod)
    for mod in allModFolders:
        try:
            with open(os.path.join(modPath, mod + os.sep + "meta.cpp")) as cpp:
                content = cpp.readlines()
                modName = content[2]
                allMods.update({modName.split('"')[1]: mod})
        except Exception:
            allMods.update({"*INVALID* " + mod: mod})
    return allMods

def saveToWhitelist(whitelist):
    """add mods to a whitelist"""
    with open("whitelist.txt", "a") as whiteFile:
        for mod in whitelist.keys():
            whiteFile.writelines(mod + "/" + whitelist.get(mod) + "\n")

def removeFromWhitelist(removeList):
    """remove mods from whitelist"""
    whitelist = readWhitelist()
    with open("whitelist.txt", "w") as whiteFile:
        for mod in removeList:
            if mod in whitelist:   whitelist.pop(mod)
        for mod in whitelist.keys():
            whiteFile.writelines(mod + "/" + whitelist.get(mod) + "\n")

import os

path = ""

def setPath():
    """set work path from settings file or system default"""
    global path
    if os.path.exists("settings.txt"):
        with open("settings.txt") as settingsFile:
            settings = settingsFile.readlines()
            path = settings[0].split("=", 1)[1]
            #stuff
    else:
        if os.name == "nt":
            if os.path.exists("."):  path = "."
            else:   path = "."
        elif os.name == "posix":
            if os.path.exists("."):  path = "."
            else:   path = "."

def searchModlists():
    """find all modlists in selected path"""
    modlists = []
    with os.scandir(path) as files:
        for file in files:
            if file.path.endswith(".html"):  modlists.append(file.path.removeprefix(path + os.sep))
    return modlists

def readModlists(htmls):
    """read all modlists, put mod and relative number together, same for dlc"""
    modlists = []
    mods = {}
    dlcs = {}
    for i in range(len(htmls)):
        with open(os.path.join(path, htmls[i])) as html:
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

def searchExtraMods(mods):
    """check mod folder and filter the unused ones"""
    allModFolders = []
    allMods = {}
    with os.scandir(path) as files:
        for file in files:
            if file.is_dir():  allModFolders.append(file.path.removeprefix(path + os.sep))
    for mod in mods:
        if mod in allModFolders:  allModFolders.remove(mod)
    for mod in allModFolders:
        with open(os.path.join(path, mod + os.sep + "meta.cpp")) as cpp:
            content = cpp.readlines()
            modName = content[2]
            allMods.update({modName.split('"')[1]: mod})
    return allMods

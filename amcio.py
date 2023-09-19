import os

def searchModlists(path = "."):
    """find all modlists in selected path or default if no argument"""
    modlists = []
    files = os.scandir(path)
    for file in files:
        if file.path.endswith(".html"):  modlists.append(file.path.removeprefix(path + os.sep))
    return modlists


def readModlists(htmls):
    """read all modlists, put mod and relative number together, same for dlc"""
    modlists = []
    mods = {}
    dlcs = {}
    for i in range(len(htmls)):
        with open(htmls[i]) as html:
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


def searchExtraMods(mods = [], path = "."):
    """check mod folder and filter the unused ones"""
    allMods = []
    files = os.scandir(path)
    for file in files:
        allMods.append(file.path.removeprefix(path + os.sep))
    files.close()
    for mod in mods:
        if mod in allMods:  allMods.remove(mod)
    return sorted(allMods, key = str.lower)

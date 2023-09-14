import glob

def searchModlists():
    """find all modlists in selected path or default if no argument"""
    return glob.glob("*.html")


def readModlists(htmls):
    """read all modlists, put mod and relative number together, same for dlc"""
    modlists = []
    mods = {}
    dlcs = {}
    for i in range(len(htmls)):                         #
        # debug print("found: " + htmls[i].removesuffix(".html"))
        with open(htmls[i]) as html:
            modlists.append(html.readlines())
            for j in range(len(modlists[i])):
                if j < 89: pass 
                elif modlists[i][j].startswith('          <td data-type="DisplayName">'):
                    key = modlists[i][j].removeprefix('          <td data-type="DisplayName">').split("<")[0]
                elif modlists[i][j].startswith('            <a href="'):
                    value = modlists[i][j].split('"', 2)[1]
                    if len(value.split("=")) > 1:   mods.update({key: value.split("=")[-1]})
                    else:   dlcs.update({key: value.rsplit("/", 1)[1]})
    return htmls, mods, dlcs

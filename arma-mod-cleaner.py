import amcui
import amcio

#debug
print("Arma mod cleaner by Alex\n")

__htmls = []
__mods = {}
__dlcs = {}

def refresh():
        """scan for modlist files and the contained mods"""
        htmls = amcio.searchModlists()
        mods, dlcs = amcio.readModlists(htmls)
        return htmls, mods, dlcs

htmls, mods, dlcs = refresh()

if len(htmls) == 0:                                 #this should be in amcui
        print("no modlists found, exiting")
        amcui.emptyHtmls()
        exit()


#debug
print(sorted(mods.items()))
print(dlcs)
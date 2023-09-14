import amcui
import amcio

print("Arma mod cleaner by Alex\n")

htmls = amcio.searchModlists()
if len(htmls) == 0:                                 #this shuold be in amcui
        print("no modlists found, exiting")
        amcui.emptyHtmls()
        exit()

mods = {}
dlcs = {}
mods, dlcs = amcio.readModlists(htmls)

#debug
print(sorted(mods.items()))
print(dlcs)
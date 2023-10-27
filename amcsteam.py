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
#using the SteamworksPy API https://github.com/philippj/SteamworksPy licensed undet MIT License
from steamworks import STEAMWORKS
steamworks = STEAMWORKS()

def callback(result):
    print(result)

def unsubscribe(mods):
    steamworks.initialize()
    for mod in mods:
        steamworks.Workshop.UnsubscribeItem(int(mod), callback)
    steamworks.unload()
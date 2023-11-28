# Arma Mod Cleaner

Arma Mod Cleaner is a tool for tracking and removing unused mods from Arma 3.

## Description

The program detects the mods not used in any modlist for an easy removal. It checks in the default install directories but different ones can also be specified.

## Installation

Download the latest release from [here](https://gitlab.com/Alexein/arma-3-mod-cleaner/-/releases) and unpack it in a folder.  
Some Linux distributions lack the `tk` library so if you encounter problems running it you will have to install it through your package manager:
- for debian based distros  
`sudo apt install python-tk`  
- for arch based distros  
`sudo pacman -S python-tk`  

## Visuals 

![default screen](/images/Standard.jpg "default screen")  default screen  
![when selecting a mod for unsubscription](/images/Mod_selected.jpg "when selecting a mod for unsubscription")  when selecting a mod for unsubscription  
![after a successful unsubscription](/images/Mod_unsubbed.jpg "after a successful unsubscription")  after a successful unsubscription

## Usage

After opening the program, it will separate mods that are used in one or more modlists and separate the ones that are currently unused. At this point you can either select one by one the mods you want to unsubscribe and press the `Unsub extra mods` button, or `Whitelist extra mods` to whitelist them and place them to the bottom of the needed mods box. The `Unsub all extra mods` will remove all mods in the extra mods box regardless of selection.
Because of the way Steam integration works, you may need to close the program and wait a few minutes for Steam to remove the files from your pc. This may lead to still seeing the mods you unsubscribed if they're not yet deleted when reopening the program. 
The `show invalid mods` will let you see the mods that don't follow usual structure, this may happen for single player mission, ace compatibility mods etc. The program won't let you unsubscribe these.

## License

This program and its components are licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html)
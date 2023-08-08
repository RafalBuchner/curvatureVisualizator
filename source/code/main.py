from mojo.extensions import registerExtensionDefaults, ExtensionBundle
from curvatureVisualizator.curvatureVisualizatorSubscriber import CurvatureVisualizatorSubscriber
from curvatureVisualizator.curvatureVisualizatorSettings import ExtensionSettingsWindow, extensionName, camelCaseToSpaced
from mojo.tools import CallbackWrapper
from mojo import subscriber, events
from collections import OrderedDict
import yaml, pprint, AppKit

## https://stackoverflow.com/questions/7367438/sort-nsmenuitems-alphabetically-and-by-whether-they-have-submenus-or-not
def sortMenu(menu):
    itemArray = menu.itemArray().copy()
    menu.removeAllItems()

    # create a descriptor that will sort files alphabetically
    alphaDescriptor = AppKit.NSSortDescriptor.alloc().initWithKey_ascending_("title", True)
    itemArray = itemArray.sortedArrayUsingDescriptors_([alphaDescriptor])

    # create a descriptor that will sort files alphabetically and based on existance of submenus
    # submenuDescriptor = AppKit.NSSortDescriptor.alloc().initWithKey_ascending_("hasSubmenu", False)
    # itemArray = itemArray.sortedArrayUsingDescriptors_([submenuDescriptor,alphaDescriptor])
    for item in itemArray:
        menu.addItem_(item)

        # The following code fixes NSPopUpButton's confusion that occurs when
        # we sort this list. NSPopUpButton listens to the NSMenu's add notifications
        # and hides the first item. Sorting this blows it up.
        if item.isHidden():
            item.setHidden_(False)

        # While we're looping, if there's a submenu, go ahead and sort that, too.
        if item.hasSubmenu():
            sortMenu(item.submenu())

class ExtensionSettings:
    def __init__(self):
        # self.window = ExtensionSettingsWindow()
        events.addObserver(self, "waitForActive", "applicationDidFinishLaunching")

    def waitForActive(self, info):
        events.addObserver(self, "addMenuItem", "applicationDidBecomeActive")

    def addMenuItem(self, info):
        events.removeObserver(self, "applicationDidBecomeActive")
        events.removeObserver(self, "applicationDidFinishLaunching")

        menubar = AppKit.NSApp().mainMenu()

        title = camelCaseToSpaced(extensionName)

        extensionsItem = menubar.itemWithTitle_("Extensions")
        extensionsMenu = extensionsItem.submenu()
        mySubMenuItem = extensionsMenu.itemWithTitle_(title)

        if not mySubMenuItem:
            # If it doesn't exist, create a new NSMenuItem with the title "Copy Version Info..." and add it to the menu below the About item
            #help(AppKit.NSMenuItem)
            mySubMenu = AppKit.NSMenu.alloc().init()
            mySubMenuItem = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(title, "", "")
            mySubMenuItem.setSubmenu_(mySubMenu)

            # create settings NSMenuItem
            self.extensionSettingsInfoTarget = CallbackWrapper(self.extensionSettingsInfoCallback)
            extensionSettingsMenuItem = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
                title+" Settings",
                "action:",
                ""
            )
            extensionSettingsMenuItem.setTarget_(self.extensionSettingsInfoTarget)
            mySubMenu.insertItem_atIndex_(extensionSettingsMenuItem, 0)

            extensionsMenu.insertItem_atIndex_(mySubMenuItem, 0)
            sortMenu(extensionsMenu)



    def extensionSettingsInfoCallback(self, sender):
        ExtensionSettingsWindow()

ExtensionSettings()
subscriber.registerGlyphEditorSubscriber(CurvatureVisualizatorSubscriber)

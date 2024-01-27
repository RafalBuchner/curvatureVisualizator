from mojo.extensions import registerExtensionDefaults, ExtensionBundle
from curvatureVisualizator.curvatureVisualizatorSubscriber import CurvatureVisualizatorSubscriber
from curvatureVisualizator.curvatureVisualizatorSettings import ExtensionSettingsWindow, extensionName, camelCaseToSpaced
from mojo.tools import CallbackWrapper
from mojo import subscriber, events
from collections import OrderedDict
import yaml, pprint, AppKit


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
                "Settings",
                "action:",
                ""
            )
            extensionSettingsMenuItem.setTarget_(self.extensionSettingsInfoTarget)
            mySubMenu.addItem_(extensionSettingsMenuItem)

            extensionsMenu.addItem_(mySubMenuItem)

        # really stupid way to examine if zenExtensions
        zenExtensionsInstalled = ExtensionBundle("ZenExtensions").bundleExists()
        
        self.sortMenu(extensionsMenu, zenExtensionsInstalled)


    def sortMenu(self, menu, zenExtensionsInstalled):
        itemArray = menu.itemArray().copy()

        # Create a descriptor that will sort files alphabetically
        alphaDescriptor = AppKit.NSSortDescriptor.alloc().initWithKey_ascending_("title", True)

        # Create a descriptor that will sort files alphabetically and based on existance of submenus
        submenuDescriptor = AppKit.NSSortDescriptor.alloc().initWithKey_ascending_("hasSubmenu", False)
        if zenExtensionsInstalled:
            itemArray = itemArray.sortedArrayUsingDescriptors_([submenuDescriptor, alphaDescriptor])
        else:
            itemArray = itemArray.sortedArrayUsingDescriptors_([alphaDescriptor])
        bottomItems = []
        newItemArray = AppKit.NSMutableArray.alloc().init()
        for item in itemArray:
            if item.title() in ["Mechanic 2"]:
                bottomItems.append(item)
                continue
            newItemArray.addObject_(item)
            # The following code fixes NSPopUpButton's confusion that occurs when
            # we sort this list. NSPopUpButton listens to the NSMenu's add notifications
            # and hides the first item. Sorting this blows it up.
            if item.isHidden():
                item.setHidden_(False)

        newItemArray.addObject_(AppKit.NSMenuItem.separatorItem())
        for item in bottomItems:
            newItemArray.addObject_(item)
        test = AppKit.NSArray.alloc().initWithArray_(newItemArray)
        menu.setItemArray_(test)




    def extensionSettingsInfoCallback(self, sender):
        ExtensionSettingsWindow()

ExtensionSettings()
subscriber.registerGlyphEditorSubscriber(CurvatureVisualizatorSubscriber)

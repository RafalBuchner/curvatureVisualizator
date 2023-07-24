from vanilla.vanillaBase import VanillaCallbackWrapper
from mojo.subscriber import Subscriber
from AppKit import NSMenuItem

def _getDisplayPopUpMenuFromEditWindow(editWindow):
    if editWindow is None:
        return
    for subview in editWindow.getGlyphStatusBar().getNSView().subviews():
        if hasattr(subview, "title"):
            if subview.title() == "Display...":
                return subview

def _createCustomVisualizerSeparator(displayPopUp):
    if len(displayPopUp.itemArray()) == 27:
        menu = displayPopUp.menu()
        menu.addItem_(NSMenuItem.separatorItem())

    elif displayPopUp.itemArray()[27].isSeparatorItem():
        menu = displayPopUp.menu()
        menu.addItem_(NSMenuItem.separatorItem())

# ====================================
# S U B S C R I B E R
# ====================================

class DisplaySuscriber(Subscriber):
    debug = True

    title = None

    def getButtonState(self):
        return bool(self._menuItem.state())

    def _menuItemCallback(self, nsMenuItem):
        self._menuItem.setState_(not self._menuItem.state())
        self.menuButtonWasPressed(nsMenuItem)

    def menuButtonWasPressed(self, nsMenuItem):
        NotImplemented

    def _appendMenuItemToDisplayMenu(self, window):
        assert self.title is not None, "title wasn't set"
        assert isinstance(self.title, str), "title must be a string"
        displayPopUp = _getDisplayPopUpMenuFromEditWindow(window)
        if displayPopUp is None:
            return
        
        # creating the separator in Display... menu
        _createCustomVisualizerSeparator(displayPopUp)

        self._menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.title, "", "")
        wrapper = VanillaCallbackWrapper(self._menuItemCallback)
        self._menuItemCallbackWrappers = []
        self._menuItemCallbackWrappers.append(wrapper)
        self._menuItem.setTarget_(wrapper)
        self._menuItem.setAction_("action:")
        menu = displayPopUp.menu()
        menu.addItem_(self._menuItem)

    def glyphEditorDidOpen(self, info):
        """
        Whenever you want to use glyphEditorDidOpen event in your own DisplaySuscriber class, please
        use super method of glyphEditorDidOpen
        """
        self._appendMenuItemToDisplayMenu(info["glyphEditor"])
 


from vanilla.vanillaBase import VanillaCallbackWrapper
from mojo.subscriber import Subscriber
from AppKit import NSMenuItem
from curvatureVisualizator.curvatureVisualizatorSettings import (
    internalGetDefault,
    internalSetDefault,
    extensionID
)

def _getDisplayPopUpMenuFromEditWindow(editWindow):
    if editWindow is None:
        return
    return editWindow.getGlyphStatusBar().displayButton

def _createCustomVisualizerSeparator(displayPopUp):
    if len(displayPopUp.getItems()) == 27:
        menu = displayPopUp.getNSPopUpButton().menu()
        menu.addItem_(NSMenuItem.separatorItem())

    elif displayPopUp.getNSPopUpButton().itemArray()[27].isSeparatorItem():
        return

# =========================================
#  S U B S C R I B E R (with basic events)
# =========================================

class DisplaySuscriber(Subscriber):
    debug = True

    title = None

    def menuButtonWasPressed(self, nsMenuItem):
        if self.getButtonState():
            self.showMe = True
        else:
            self.showMe = False

    @property
    def showMe(self):
        return self._showMe

    @showMe.setter
    def showMe(self, value):
        if value:
            self.toggleOn()

        else:
            self.toggleOff()

        internalSetDefault("isVisible", value)
        self._showMe = value

    def getButtonState(self):
        return bool(self._menuItem.state())

    def _menuItemCallback(self, nsMenuItem):
        self._menuItem.setState_(not self._menuItem.state())
        self.menuButtonWasPressed(nsMenuItem)

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
        menu = displayPopUp.getNSPopUpButton().menu()
        menu.addItem_(self._menuItem)

    def toggleOff(self):
        NotImplemented

    def toggleOn(self):
        NotImplemented

    def glyphEditorDidOpen(self, info):
        """
        Whenever you want to use glyphEditorDidOpen event in your own DisplaySuscriber class, please
        use super method of glyphEditorDidOpen
        """
        self._appendMenuItemToDisplayMenu(info["glyphEditor"])
        self.showMe = internalGetDefault("isVisible")
        self._menuItem.setState_(self.showMe)

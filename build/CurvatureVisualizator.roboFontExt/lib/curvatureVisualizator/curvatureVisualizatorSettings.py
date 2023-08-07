import vanilla as vui
from collections import OrderedDict
import AppKit, pprint
import sys
import yaml
import ezui
from mojo.UI import AccordionView
from mojo import events
from mojo.extensions import (
    registerExtensionDefaults,
    getExtensionDefault,
    setExtensionDefault,
    ExtensionBundle
)

__DEBUG__ = True

def getDefaultsFromYaml():
    bundle = ExtensionBundle("CurvatureVisualizator")
    settings_file = bundle.getResourceFilePath("defaults",ext='yaml')
    stream = open(settings_file, 'r')
    settings_dictionary = yaml_load_ordered(stream)
    stream.close()
    extensionName = settings_dictionary["extensionName"]
    extensionID = settings_dictionary["developerID"] + "." + extensionName
    extensionKeyStub = extensionID + "."

    __defaults__ = {}
    for default_name, default_dict in settings_dictionary["__defaults__"].items():
        vanillaObj = default_dict["vanillaObj"]
        value = default_dict["value"]

        attributes = ""
        if "attributes" in default_dict.keys():
            attributes = "_"+"_".join( default_dict["attributes"] )

        default_key = f"exst_{default_name}_{vanillaObj}{attributes}"
        __defaults__[extensionKeyStub+default_key] = value
    return __defaults__, extensionName, extensionID, extensionKeyStub

def yaml_load_ordered(yaml_data):
    """
    Load yaml data to ordered dictionary
    """
    class OrderedLoader(yaml.SafeLoader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return OrderedDict(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)

    return yaml.load(yaml_data, OrderedLoader)


__defaults__, extensionName, extensionID, extensionKeyStub = getDefaultsFromYaml()
displayMenuDefault = {extensionKeyStub+"isVisible":False}
__defaults__.update(displayMenuDefault)



# def internalRegisterDefaults():
#     if __DEBUG__:
#         print(f"internalRegisterDefaults initialised defaults:")
#         pprint.pprint(__defaults__)
#     registerExtensionDefaults(__defaults__)

# internalRegisterDefaults()

def internalGetDefault(key):
    key = extensionKeyStub + key
    return getExtensionDefault(key)

def internalSetDefault(key, value):
    key = extensionKeyStub + key
    setExtensionDefault(key, value)

def camelCaseToSpaced(txt):
    return ''.join(map(lambda x: x if x.islower() else " "+x, txt))

def convertRGBA_to_NSColor(color):
    if isinstance(color, AppKit.NSColor):
        return color
    return AppKit.NSColor.colorWithCalibratedRed_green_blue_alpha_(*color)

def convertNSColor_to_RGBA(color):
    color = color.colorUsingColorSpace_(AppKit.NSColorSpace.genericRGBColorSpace())
    r = color.redComponent()
    g = color.greenComponent()
    b = color.blueComponent()
    a = color.alphaComponent()
    return (r, g, b, a)



def registerDefaultsToExtensionsSettings(your_extension_ID, defaultsDict):
    registerExtensionDefaults(defaultsDict)
    exst_key = "com.rafalbuchner.ExtensionsSettings.registeredDefaults"
    defaults = getExtensionDefault(exst_key)

    if defaults is None:
        defaults = {}
    if your_extension_ID in defaults.keys():
        del(defaults[your_extension_ID])
    defaults[your_extension_ID] = defaultsDict
    setExtensionDefault(exst_key, defaults)

order = {extensionKeyStub + "order":list(__defaults__.keys())}
__defaults__.update(order)
registerDefaultsToExtensionsSettings(extensionID, __defaults__)
registerExtensionDefaults(__defaults__)


class ExtensionSettingsWindow:
    def __init__(self, __defaults__) -> None:
        self._defaults = __defaults__


        content = """
        = TwoColumnForm

        : Visualisation Type:
        (counterclockwise | clockwise | both)                  @exst_visualisationType_SegmentedButton_counterclockwise_clockwise_both
        
        : Division Steps:

        [_123_](±)                       @exst_divisionSteps_EditText_int

        : Stroke Width:

        [_123_](±)                                  @exst_strokeWidth_EditText_int

        [ ] Text Size                               @exst_showOptionsButtonInGlyphWindow_CheckBox

        [ ] Zoom Visualisation                      @exst_zoomVisualisation_CheckBox

        : Oval Size:
        ---X---                                  @exst_visualisationSize_Slider

        : Line Size:
        * ColorWell                                 @exst_fillColor_ColorWell

        : Base Color:
        * ColorWell                                 @exst_strokeColor_ColorWell


        """
        colorWellWidth = 100
        colorWellHeight = 20
        numberEntryWidth = 75
        descriptionData = dict(
            content=dict(
                titleColumnWidth=125,
                itemColumnWidth=265
            ),
            exst_visualisationType_SegmentedButton_counterclockwise_clockwise_both=dict(
                selected=internalGetDefault("exst_visualisationType_SegmentedButton_counterclockwise_clockwise_both")
            ),
            exst_divisionSteps_EditText_int=dict(
                width=numberEntryWidth,
                valueType="number",
                value=internalGetDefault("exst_divisionSteps_EditText_int")
            ),
            exst_strokeWidth_EditText_int=dict(
                width=numberEntryWidth,
                valueType="number",
                value=internalGetDefault("exst_strokeWidth_EditText_int")
            ),
            exst_showOptionsButtonInGlyphWindow_CheckBox=dict(
                value=internalGetDefault("exst_showOptionsButtonInGlyphWindow_CheckBox")
            ),
            exst_zoomVisualisation_CheckBox=dict(
                value=internalGetDefault("exst_zoomVisualisation_CheckBox")
            ),
            exst_visualisationSize_Slider=dict(
                continuous=False,
                minValue=internalGetDefault("exst_visualisationSize_Slider")["minValue"],
                maxValue=internalGetDefault("exst_visualisationSize_Slider")["maxValue"],
                value=internalGetDefault("exst_visualisationSize_Slider")["value"]
            ),
            exst_fillColor_ColorWell=dict(
                width=colorWellWidth,
                height=colorWellHeight,
                color=tuple(internalGetDefault("exst_fillColor_ColorWell"))
            ),
            exst_strokeColor_ColorWell=dict(
                width=colorWellWidth,
                height=colorWellHeight,
                color=tuple(internalGetDefault("exst_strokeColor_ColorWell"))
            ),
        )
        self.w = ezui.EZWindow(
            title="Stem Plow Settings",
            content=content,
            descriptionData=descriptionData,
            controller=self
        )
        self.w.open()

    # def started(self):
    #     self.w.open()

    def contentCallback(self, sender):
        for key, value in sender.getItemValues().items():
            print(key, value)
        #     existing = internalGetDefault(key)
        #     print(key, value, existing)
        #     if existing == value:
        #         continue
        #     internalSetDefault(key, value)
        # postEvent(
        #     extensionID + ".defaultsChanged"
        # )




note = """
The settings window is only available in
RoboFont 4.2+
""".strip()

def StemPlowSettingsWindowController(*args, **kwargs):
    from mojo import roboFont

    version = roboFont.version
    versionMajor, versionMinor = version.split(".", 1)
    versionMinor = versionMinor.split(".")[0]
    versionMajor = "".join([i for i in versionMajor if i in "0123456789"])
    versionMinor = "".join([i for i in versionMinor if i in "0123456789"])
    versionMajor = int(versionMajor)
    versionMinor = int(versionMinor)
    if versionMajor == 4 and versionMinor < 2:
        print(note)
    else:
        _StemPlowSettingsWindowController(*args, **kwargs)

ExtensionSettingsWindow(__defaults__)
# if __name__ == "__main__" and "RoboFont" not in sys.executable:
#     from vanilla.test.testTools import executeVanillaTest
#     executeVanillaTest(ExtensionSettingsWindow, **dict(defaults=__defaults__))

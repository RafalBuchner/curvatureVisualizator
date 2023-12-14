import vanilla as vui
from collections import OrderedDict
import AppKit, pprint
import sys
import yaml
import ezui
from mojo.events import postEvent
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
        if vanillaObj == "ColorWell":
            value = tuple(value)

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

def internalGetDefault(key):
    key = extensionKeyStub + key
    return getExtensionDefault(key)

def internalSetDefault(key, value):
    key = extensionKeyStub + key
    setExtensionDefault(key, value)

def camelCaseToSpaced(txt):
    return ''.join(map(lambda x: x if x.islower() else " "+x, txt)).strip()

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
    _defaults = __defaults__
    def __init__(self):

        content, descriptionData= self.buildContnentAndDescription()

        self.w = ezui.EZWindow(
            title=f"{camelCaseToSpaced(extensionName)} Settings",
            content=content,
            descriptionData=descriptionData,
            controller=self
        )
        self.w.open()

    def buildContnentAndDescription(self):
        colorWellWidth = 100
        colorWellHeight = 20
        numberEntryWidth = 75

        descriptionData = dict(
            content=dict(
                titleColumnWidth=125,
                itemColumnWidth=265
            )
        )
        content = "= TwoColumnForm\n\n"

        for keyEntry in self._defaults:
            key = keyEntry.split(".")[-1]
            if "_" not in key:
                continue
            keyElements = key.split("_")[1:]
            title = camelCaseToSpaced(keyElements[0]).title()
            vanillaObjName = keyElements[1]
            args = keyElements[2:]
            #print(f"t:{title} vo:{vanillaObjName} args:{args} key:{key}")
            txt = "---"
            if vanillaObjName == "CheckBox":
                txt = f"[ ] {title.lower()}                        @{key}"
                _descriptionData = {
                    key:dict(
                        value=internalGetDefault(key)
                    )
                }

            elif vanillaObjName == "Slider":
                txt = f": {title}:\n---X---                        @{key}"
                _descriptionData = {
                    key:dict(
                        continuous=True,
                        minValue=internalGetDefault(key)["minValue"],
                        maxValue=internalGetDefault(key)["maxValue"],
                        value=internalGetDefault(key)["value"]
                    )
                }

            elif vanillaObjName == "ColorWell":
                txt = f": {title}:\n* ColorWell                        @{key}"
                _descriptionData = {
                    key:dict(
                        width=colorWellWidth,
                        height=colorWellHeight,
                        color=tuple(internalGetDefault(key))
                    )
                }

            elif vanillaObjName == "EditText":
                txt = f": {title}:\n[__]                        @{key}"
                _descriptionData = {
                    key:dict(
                        valueType="string",
                        value=internalGetDefault(key)
                    )
                }

                if "int" in args:
                    minValue = 0
                    if "division" in key:
                        minValue = 3
                    txt = f": {title}:\n[_123_](±)                        @{key}"
                    _descriptionData = {
                        key:dict(
                            width=numberEntryWidth,
                            valueType="number",
                            minValue=minValue,
                            value=internalGetDefault(key)
                        )
                    }

            elif vanillaObjName == "SegmentedButton":
                txt = f": {title}:\n({' | '.join(args)})                       @{key}"
                _descriptionData = {
                    key:dict(
                        selected=internalGetDefault(key)
                    )
                }

            txt += "\n\n"
            content += txt
            descriptionData.update(_descriptionData)
        # print("="*100)
        # print('"""')
        # print(content)
        # print('"""')
        # pprint.pprint(descriptionData)
        ezui.knownItemTypes()




        return content, descriptionData

    def contentCallback(self, sender):
        for key, value in sender.getItemValues().items():
            if "_Slider" in key :
                item = sender.getItem(key)
                minValue = item.getNSSlider().minValue()
                maxValue = item.getNSSlider().maxValue()
                _value = dict(
                    minValue=minValue,
                    value=value,
                    maxValue=maxValue,
                )
                if "_int" in key :
                        _value = dict(
                        minValue=minValue,
                        value=int(value),
                        maxValue=maxValue,
                    )
                value = _value
            elif "_int" in key :
                value = int(value)

            existing = internalGetDefault(key)
            if existing == value:
                continue
            internalSetDefault(key, value)
        postEvent(
            extensionID + ".defaultsChanged"
        )




note = """
The settings window is only available in
RoboFont 4.2+
""".strip()

def ExtensionSettingsWindowController(*args, **kwargs):
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
        _ExtensionwSettingsWindowController(*args, **kwargs)

# from mojo.UI import OutputWindow
# OutputWindow().clear()
# ExtensionSettingsWindow()
# if __name__ == "__main__" and "RoboFont" not in sys.executable:
#     from vanilla.test.testTools import executeVanillaTest
#     executeVanillaTest(ExtensionSettingsWindow, **dict(defaults=__defaults__))

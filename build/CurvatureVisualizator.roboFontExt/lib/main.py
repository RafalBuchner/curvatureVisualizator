from mojo.extensions import registerExtensionDefaults
from curvatureVisualizator.curvatureVisualizatorSubscriber import CurvatureVisualizatorSubscriber
from mojo import subscriber
from mojo.extensions import ExtensionBundle
from collections import OrderedDict
import yaml, pprint

def getDefaultsFromYaml():
    bundle = ExtensionBundle("CurvatureVisualizator")
    settings_file = bundle.getResourceFilePath("defaults",ext='yaml')
    with open(settings_file, 'r', encoding="utf-8") as stream:
        settings_dictionary = yaml_load_ordered(stream)

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
    return None, None, None, None

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

__defaults__, _,_,_ = getDefaultsFromYaml()
pprint.pprint(__defaults__)
registerExtensionDefaults(__defaults__)
subscriber.registerGlyphEditorSubscriber(CurvatureVisualizatorSubscriber)

import pprint
from collections import OrderedDict
import yaml

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
stream = open("test.yaml", 'r')
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
    __defaults__[default_key] = value
pprint.pprint(__defaults__)

from mojo.extensions import (
    registerExtensionDefaults,
    getExtensionDefault,
    setExtensionDefault
)

extensionID = "com.rafalbuchner.CurveVisualizator"
extensionKeyStub = extensionID + "."

__defaults__ = {
    extensionKeyStub + "isVisible": False,
    extensionKeyStub + "divisionSteps_int": 77,
    extensionKeyStub + "strokeWidth_int": 2,
    extensionKeyStub + "outlineType_RadioButton": 0,
    extensionKeyStub + "showOptionsButtonInGlyphWindow_CheckBox": True,
    extensionKeyStub + "zoomVisualisation_CheckBox": False,
    extensionKeyStub + "visualisationSize_SliderInt": dict(minValue=0,maxValue=8000,value=1600),
    extensionKeyStub + "visualisationType_SegmentedButton_counterclockwise_clockwise_both": 2,
    extensionKeyStub + "fillColor_Color": (1,.8,0,.5),
    extensionKeyStub + "strokeColor_Color": (1,.8,0,.1),
}

def internalRegisterDefaults():
    registerExtensionDefaults(__defaults__)

def internalGetDefault(key):
    key = extensionKeyStub + key
    return getExtensionDefault(key)

def internalSetDefault(key, value):
    key = extensionKeyStub + key
    setExtensionDefault(key, value)

internalRegisterDefaults()

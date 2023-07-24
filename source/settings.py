from mojo.extensions import (
    registerExtensionDefaults,
    getExtensionDefault,
    setExtensionDefault
)

extensionID = "com.rafalbuchner.CurveVisualizator"
extensionKeyStub = extensionID + "."

defaults = {
    extensionKeyStub + "isVisible": False,
}

registerExtensionDefaults(defaults)

def internalGetDefault(key):
    key = extensionKeyStub + key
    return getExtensionDefault(key)


def internalSetDefault(key, value):
    key = extensionKeyStub + key
    setExtensionDefault(key, value)
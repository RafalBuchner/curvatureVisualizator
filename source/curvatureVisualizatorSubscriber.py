from displaySubscriber import DisplaySuscriber
from mojo import subscriber

# ====================================
# Example
# ====================================       

class CurvatureVisualizatorSubscriber(subscriber.DisplaySuscriber):
    debug = True

    title = "this is my subscriber button" 

    def menuButtonWasPressed(self, nsMenuItem):
        print(f"current state of '{self.title}' button: {self.getButtonState()}")        
        print(nsMenuItem)
    
    def glyphEditorDidOpen(self, info):
        super().glyphEditorDidOpen(info) 
        print("glyph editor did open!!!")

subscriber.registerGlyphEditorSubscriber(CurvatureVisualizatorSubscriber)
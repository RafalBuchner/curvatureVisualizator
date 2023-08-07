import ezui



class DemoController(ezui.WindowController):

    def build(self):
        content = """
        = ScrollingVerticalStack
        [_ ?] Search
        * Accordion: Accordion 1 @accordion1
        > * Box
        > > (Button 1)              @button1
        > > (Button 2)              @button2
        * Accordion: Accordion 2 @accordion2
        > * Box
        > > (Button 3)              @button3
        > > (Button 4)              @button4
        * Accordion: Accordion 3 @accordion3
        > * Box
        > > (Button 5)              @button5
        > > (Button 6)              @button6
        * Accordion: Accordion 4 @accordion4
        > * Box
        > > (Button 7)              @button7
        > > (Button 8)              @button8
        * Accordion: Accordion 5 @accordion5
        > * Box
        > > (Button 9)              @button9
        > > (Button 10)             @button10


        """
        descriptionData = dict(
        )
        self.w = ezui.EZWindow(
            title="Demo",
            size=(200, 200),
            minSize=(200,200),
            content=content,
            descriptionData=descriptionData,
            controller=self
        )

    def started(self):
        self.w.open()

DemoController()

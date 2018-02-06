from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.graphics import Line, Color
import math
Window.clearcolor = (1, 1, 1, 1)
Window.size = (600,400)
builder = Builder.load_string("""
<slopeField>:
    id: slopeField
    BoxLayout:
        size: root.width, root.height/10
        id: mainLayout
        TextInput:
            id: points
            text: "(-10,10),(-10,10)"
            size_hint: .3,1
        TextInput:
            id: equation
            text: "x*y"
            size_hint: .3,1
        TextInput:
            id: increment
            text: "1"
            size_hint: .2, 1
        Button:
            text: "Submit"
            on_press: root.callback()
            size_hint: .3,1
    BoxLayout:
        id: lineScreen
        size_hint:1,.9
""")
class slopeField(Widget):
    myFormula = "x^2"
    mySize = []
    startx = 0
    starty = 0
    endx = 0
    endy = 0
    def findSize(self):
        pointString = self.ids["points"].text
        size = []
        first = pointString.index(")")
        firstTuple = pointString[1:first]
        secondTuple = pointString[first+3:len(pointString)-1]
        #size.append(secondTuple[0:secondTuple.index(",")] - firstTuple[0:firstTuple.index(",")])
        self.startx = (int)(firstTuple[0:firstTuple.index(",")])
        self.endx = (int)(firstTuple[firstTuple.index(",")+1::])
        self.starty = (int)(secondTuple[0:secondTuple.index(",")])
        self.endy = (int)(secondTuple[secondTuple.index(",")+1::])
        size.append(abs(self.endx - self.startx))
        size.append(abs(self.endy - self.starty))
        self.mySize = size
    def fix(self):
        self.myFormula = self.fixHelper(self.myFormula)
    def fixHelper(self, formula):
        for x in range(len(formula)-1):
            if formula[x] == "^":
                return self.fixHelper(formula[0:x] + "**" + formula[x+1::])
            if x <= len(formula)-3 and formula[x:x+3] == "tan" and (x==0 or not formula[x-1] == "."):
                return self.fixHelper(formula[0:x] + "math.tan" + formula[x+3::])
            if x <= len(formula)-3 and formula[x:x+3] == "cos" and (x==0 or not formula[x-1] == "."):
                return self.fixHelper(formula[0:x] + "math.cos" + formula[x+3::])
            if x <= len(formula)-3 and formula[x:x+3] == "sin" and (x==0 or not formula[x-1] == "."):
                return self.fixHelper(formula[0:x] + "math.sin" + formula[x+3::])
            if x <= len(formula)-3 and formula[x:x+3] == "log" and (x==0 or not formula[x-1] == "."):
                return self.fixHelper(formula[0:x] + "math.log" + formula[x+3::])
            if x <= len(formula)-1 and formula[x] == "e" and (x==0 or not formula[x-1] == "."):
                return self.fixHelper(formula[0:x] + "math.e" + formula[x+1::])
        return formula
    def yVal(self, x, y):
        x = (float)(x)
        y = (float)(y)
        try: 
            return (float)(eval(self.myFormula))
        except ZeroDivisionError:
            return 9999999
        except ValueError:
            return None
    def displayLines(self):
        increment = (float)(self.ids["increment"].text)
        xBuffer = (self.size[0]/self.mySize[0])/2.
        yBuffer = self.size[1]*.1+(self.size[1]/self.mySize[1])/2.
        xMult = self.size[0]/self.mySize[0]
        yMult = self.size[1]/self.mySize[1]*.9
        for myX in range((int)((self.mySize[0]+1)/increment)):
            for myY in range((int)((self.mySize[1]+1)/increment)):
                realX = myX * increment
                realY = myY * increment
                if not self.yVal(realX+self.startx, realY+self.starty) == None:
                    myLength = (.81 + abs((realY-.45*self.yVal(realX+self.startx, realY+self.starty)) - (realY + .45*self.yVal(realX+self.startx, realY+self.starty)))**2)**.5
                    lMult = 1./myLength*increment
                    with self.ids["lineScreen"].canvas:
                        Color(0,0,0)
                        Line(points = ((realX-.45*lMult)*xMult+xBuffer,(realY-.45*self.yVal(realX+self.startx, realY+self.starty)*lMult)*yMult+yBuffer,(realX+.45*lMult)*xMult+xBuffer,(realY + .45*self.yVal(realX+self.startx,realY+self.starty)*lMult)*yMult+yBuffer), width = 1)
        with self.ids["lineScreen"].canvas:
            Color(1,0,0)
            Line(points = (0, -self.starty*yMult+yBuffer, (self.size[0]+1)*xMult, -self.starty*yMult+yBuffer), width = 1, dash_offset = 30, dash_length = 30)
            Line(points = (-self.startx*xMult+xBuffer, self.size[1]*.1, -self.startx*xMult+xBuffer, (self.size[1] + 1)*yMult), width = 1, dash_offset = 30, dash_length = 30)
    def callback(self):
        self.ids["lineScreen"].canvas.clear()
        self.findSize()
        self.myFormula = self.ids["equation"].text
        self.fix()
        self.displayLines()
class Aaron_Nhans_Slope_FieldApp(App):
    def build(self):
        return slopeField()
Aaron_Nhans_Slope_FieldApp().run()

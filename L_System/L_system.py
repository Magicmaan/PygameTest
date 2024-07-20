import turtle
import math

global tturtle 
tturtle = turtle.Turtle()  # recursive turtle
tturtle.screen.title("L-System Derivation")
tturtle.speed(0)  # adjust as needed (0 = fastest)
#turtle_screen = turtle.Screen()  # create graphics window
#turtle_screen.screensize(1500, 1500)
tturtle.hideturtle()


def function_fwd(turtle,step):
    turtle.forward(step)

def function_fwdNodraw(turtle,step):
    turtle.penup()  # pen up - not drawing
    turtle.forward(step)

def function_rotRight(turtle,angleStep):
    turtle.right(angleStep)

def function_rotLeft(turtle,angleStep):
    turtle.left(angleStep)

def function_widthIncrease(turtle,widthStep):
    currentWidth = turtle.pensize()
    turtle.pensize(currentWidth + widthStep)

def function_widthDecrease(turtle,widthStep):
    currentWidth = turtle.pensize()
    turtle.pensize(currentWidth - widthStep)

def function_flower():
    pass




#Base instruction set bindings for functions of turtle
commandList = {
    "F" :           function_fwd,           #Move Forward and draw
    "f" :           function_fwdNodraw,     #Move and don't draw
    "+" :           function_rotRight,      #Rotate Right
    "-" :           function_rotLeft,       #Rotate Left
    "!" :           function_widthIncrease, #Decrease branch Width
    "@" :           function_widthDecrease, #Increase branch Width
    "%" :           function_flower,        #flower / bud
}

#Rule Set
#defines shorthand for commands
#loops can be formed with [ ] which allow to branch off and then return
rules = {
    "G" : "F[+L]-L",
    "L" : "F+FF"
}


class LSys():
    def __init__(self,turtle,axiom,mode=0):
        self.turtle = turtle

        self.settings = {
            "seg_length" : 10,
            "angle" : 30,
            "widthStep" : 1,
            "depth" : 10 ,
            "axiom" : axiom
        }
        #decompress input axiom to instructions
        self.instructions = "".join(self._decompressAxiom())
        self.vars = {}
        self.expressionCache = {}

        #draw it
        self._drawBasic(0)
    

    def _drawBasic(self,string):
        self.stack = []
        #for command in the turtles instructions
        for cmd in self.instructions:
            self.turtle.pd()
            if cmd in commandList:
                func = commandList[cmd]

                #if next "cmd" is (, then regex and eval expression (or store)
                #create cache   
                #expression = 
                #param = self._evalExpression(expression)

                if "fwd" in func.__name__:
                     param = self.settings["seg_length"]
                elif "rot" in func.__name__:
                     param = self.settings["angle"]
                elif "width" in func.__name__:
                    param = self.settings["widthStep"]

                output = func(self.turtle,param)
            
            if cmd == "[":
                self._function_enterLoop()
            if cmd == "]":
                print("CLOSE LOOP ")
                self._function_exitLoop()


    #Internal functions -----------------------------------------------------------------------------------------

    def _function_enterLoop(self):
        self.stack.append([self.turtle.position(),self.turtle.heading(),self.turtle.pensize()])

    def _function_exitLoop(self):
        position, heading, pen = self.stack.pop()
        self.turtle.pu()
        self.turtle.setpos(position)
        self.turtle.setheading(heading)
        self.turtle.pensize(pen)

    def _evalExpression(self,expression):
        if not expression in self.expressionCache:
            self.expressionCache[expression] = eval(expression)
        
        result = self.expressionCache[expression]
        return result
    
    def _decompressExpression(self,expression):
        #extractedString = regex that shit

        return

    def _decompressAxiom(self):
        #Decompress a rule shorthand into instructionset for turtle / draw
        instructionset,currentString = "G","G"
        instructions = ""
        nextAxiom = instructionset
        #how many times to repeat pattern recursively
        for loop in range(self.settings["depth"]):
            #get last Axiom
            #find corresponding instructionset for the Rule and unpack
            nextRule = self._decompressRule(nextAxiom)
            instructions += nextRule
        
        return instructions
    
    def _decompressRule(self,rule):
        #if its a rule, return the rules instruction

        #i.e. input rule = F
        #in rules look for dict entry F, return val

        #if none is found, rules.get will return the input rule
        return rules.get(rule)

    
    








#input ruleset, creates instruction path for a turtle and draws it
test = LSys(tturtle,"G",0)

#test._drawBasic("--FF+FF+F-FF!!FFFF!!FFFF---FFFFFFfffFFFFF")

tturtle.getscreen().exitonclick()
import turtle
import math

tturtle = turtle.Turtle()  # recursive turtle
tturtle.screen.title("L-System Derivation")
tturtle.speed(0)  # adjust as needed (0 = fastest)
turtle_screen = turtle.Screen()  # create graphics window
turtle_screen.screensize(1500, 1500)


def function_Fwd(settings):
    tturtle.forward(settings["seg_length"])

def function_FwdNodraw(settings):
    tturtle.pu()  # pen up - not drawing
    tturtle.forward(settings["seg_length"])
    tturtle.pd()

def function_rotRight(settings):
    tturtle.right(settings["seg_length"])

def function_rotLeft(settings):
    tturtle.left(settings["angle"])

def function_widthIncrease(settings):
    currentWidth = tturtle.pensize()
    tturtle.pensize(currentWidth + settings["widthStep"])

def function_widthDecrease(settings):
    currentWidth = tturtle.pensize()
    tturtle.pensize(min(0,currentWidth - settings["widthStep"]))

def function_flower():
    pass


#Base instruction set bindings for functions of turtle
commandList = {
    "F" :           function_Fwd,           #Move Forward and draw
    "f" :           function_FwdNodraw,     #Move and don't draw
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
    "G" : "-FF[+++FFF---]FF"
}


class LSys():
    def __init__(self,axiom,mode=0):
        self.settings = {
            "seg_length" : 10,
            "angle" : 45,
            "widthStep" : 1,
            "depth" : 8 ,
            "axiom" : axiom
        }
        #decompress input axiom to instructions
        self.instructions = "".join(self._decompressAxiom())

        #draw it
        self._drawBasic(0)




    def _decompressAxiom(self):
        #Decompress a rule shorthand into instructionset for turtle / draw
        instructionset = "G"
        instructions = []

        #how many times to repeat pattern recursively
        for loop in range(self.settings["depth"]):
            #get last Axiom
            nextAxiom = instructionset[-1]
            #find corresponding instructionset for the Rule and unpack
            nextSequence = [self._decompressRule(char) for char in nextAxiom]
            instructions.append("".join(nextSequence))
        
        return instructions
    
    def _decompressRule(self,rule):
        #if its a rule, return the rules instruction
        if rule in rules.keys():
            return rules[rule]
        #else return itself i.e. its already an instruction
        return rule
    
    def _drawBasic(self,string):
        #for command in the turtles instructions
        for cmd in self.instructions:
            print(cmd)

            #start a closed loop
            # 1,2, [4,3,2,1], 3,4
            if cmd == "[":
                pos = turtle.pos()
            elif cmd == "]":
                #backtrack turtle to position before loop
                turtle.pu()
                turtle.goto(pos)
                turtle.pd()
                pos = turtle.pos()
                print(" ")

            #if corresponding command in instructionset, do its function
            #F = function_Fwd etc
            if cmd in commandList.keys():
                commandList[cmd](self.settings)
            else:
                print("COMMAND: " + cmd + " invalid")







#input ruleset, creates instruction path for a turtle and draws it
test = LSys("G",0)

#test._drawBasic("--FF+FF+F-FF!!FFFF!!FFFF---FFFFFFfffFFFFF")

turtle_screen.exitonclick()
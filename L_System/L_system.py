import turtle
import math

tturtle = turtle.Turtle()  # recursive turtle
tturtle.screen.title("L-System Derivation")
tturtle.speed(0)  # adjust as needed (0 = fastest)
turtle_screen = turtle.Screen()  # create graphics window
turtle_screen.screensize(1500, 1500)
tturtle.hideturtle()


def function_Fwd(turtle,settings):
    turtle.forward(settings["seg_length"])

def function_FwdNodraw(turtle,settings):
    turtle.penup()  # pen up - not drawing
    turtle.forward(settings["seg_length"])

def function_rotRight(turtle,settings):
    turtle.right(settings["angle"])

def function_rotLeft(turtle,settings):
    turtle.left(settings["angle"])

def function_widthIncrease(turtle,settings):
    currentWidth = turtle.pensize()
    turtle.pensize(currentWidth + settings["widthStep"])

def function_widthDecrease(turtle,settings):
    currentWidth = turtle.pensize()
    turtle.pensize(min(0,currentWidth - settings["widthStep"]))
def function_flower():
    pass
def function_setPosRot(turtle,position,angle=False):
    turtle.pu()
    turtle.goto(position)
    if angle:
        turtle.setheading(angle)


#Base instruction set bindings for functions of turtle
commandList = {
    "F" :           function_Fwd,           #Move Forward and draw
    "f" :           function_FwdNodraw,     #Move and don't draw
    "+" :           function_rotRight,      #Rotate Right
    "-" :           function_rotLeft,       #Rotate Left
    "!" :           function_widthIncrease, #Decrease branch Width
    "@" :           function_widthDecrease, #Increase branch Width
    "%" :           function_flower,        #flower / bud
    "£" :           function_setPosRot,
}

#Rule Set
#defines shorthand for commands
#loops can be formed with [ ] which allow to branch off and then return
rules = {
    "G" : "FFFF[+ffffFFF]FFFF+"
}


class LSys():
    def __init__(self,turtle,axiom,mode=0):
        self.turtle = turtle

        self.settings = {
            "seg_length" : 10,
            "angle" : 90,
            "widthStep" : 1,
            "depth" : 1 ,
            "axiom" : axiom
        }
        #decompress input axiom to instructions
        self.instructions = "".join(self._decompressAxiom())

        #draw it
        self._drawBasic(0)

    def _decompressAxiom(self):
        #Decompress a rule shorthand into instructionset for turtle / draw
        instructionset,currentString = "G","G"
        instructions = ""
        nextAxiom = instructionset
        #how many times to repeat pattern recursively
        for loop in range(self.settings["depth"]):
            #get last Axiom
            #find corresponding instructionset for the Rule and unpack
            nextSequence = self._decompressRule(nextAxiom)
            instructions += nextSequence
        
        return instructions
    
    def _decompressRule(self,rule):
        #if its a rule, return the rules instruction
        return rules.get(rule)

    
    def _drawBasic(self,string):
        inloop = True
        stack = []
        #for command in the turtles instructions
        for cmd in self.instructions:
            turtle.pd()
            print(cmd)

            if cmd in commandList.keys():
                commandList[cmd](self.turtle,self.settings)
            else:
                print(cmd + " Not Found -------------------")
                if cmd == "[":
                    # Save the current state
                    stack.append((turtle.position(), turtle.heading()))
                if cmd == "]":
                    # Restore the last saved state
                    turtle.pu()  # pen up - not drawing
                    position, heading = stack.pop()
                    turtle.goto(position)
                    turtle.setheading(heading)
                '''elif False:
                    elif cmd == "F":
                        turtle.forward(self.settings["seg_length"])
                    elif cmd == "+":
                        turtle.right(self.settings["angle"])
                    elif cmd == "-":
                        turtle.left(self.settings["angle"])    '''    
            '''
            #start a closed loop
            # 1,2, [4,3,2,1], 3,4
            if cmd == "[":
                stack.append((turtle.position(), turtle.heading()))
            elif cmd == "]":
                turtle.pu()  # pen up - not drawing
                position, heading = stack.pop()
                turtle.goto(position)
                turtle.setheading(heading)
                

            #if corresponding command in instructionset, do its function
            #F = function_Fwd etc
            if cmd in commandList.keys():
                commandList[cmd](self.turtle,self.settings)
            else:
                print("COMMAND: " + cmd + " invalid ----------")'''







#input ruleset, creates instruction path for a turtle and draws it
test = LSys(tturtle,"G",0)

#test._drawBasic("--FF+FF+F-FF!!FFFF!!FFFF---FFFFFFfffFFFFF")

turtle_screen.exitonclick()
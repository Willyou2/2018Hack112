from tkinter import *

####################################
# customize these functions
####################################


root = Tk()

# Set up the model data with init
# init is called once, at the beginning of the program
# data is a Struct, which can be given new data values using data.name = value
# data will be shared across all animation functions- it's aliased!
def init(data):
    # data comes preset with width and height, from the run function
    data.color = "black"
    data.function = "pen"
    data.points = []
    data.cursor = (data.width/2, data.height/2)
    data.pressed = False
    data.colors = ["black", "red", "blue", "green", "yellow", "purple", "brown"]
    data.functions = ["pointer", "pen", "fill", "erase", "save"]
    data.rectWidth = data.width // 10
    data.rectHeight = data.height // len(data.colors)
    data.temp = "black"
    
def pen(data):
    if data.pressed:
        data.points.append(data.cursor)

def erase(data):
    if data.pressed:
        data.color = "white"
        pen(data)
        
def motion(event, data):
    data.cursor = (event.x, event.y)
    
def mousePressed(event, data):
    data.pressed = True
    
def mouseReleased(event, data):
    data.pressed = False

# Track and respond to key presses
# The event variable holds all of the data captured by the event loop
# For keyPressed, this is event.char and event.keysym
# event.char holds the direct key that was pressed, "a", "3", "@", etc.
# event.keysym holds special names for certain keys non-alphanumeric keys
# for example, "space", "BackSpace", "parenleft", "exclam"
def keyPressed(event, data):
    data.charText = event.char
    data.keysymText = event.keysym

# Draw graphics normally with redrawAll
# Main difference: the data struct contains helpful information to assist drawing
# Also, the canvas will get cleared and this will be called again
# constantly by the event loop.
def redrawAll(canvas, data):
    if len(data.points)>=1:
        if data.color == "white":
            #canvas.create_oval(data.cursor[0]-10, data.cursor[1]-10, 
            #                   data.cursor[0]+10, data.cursor[1]+10)
            canvas.create_oval(data.points[-1][0]-10,data.points[-1][1]-10,
                           data.points[-1][0]+10,data.points[-1][1]+10,
                           fill=data.color, width = 0)
        else:
            canvas.create_oval(data.points[-1][0]-5,data.points[-1][1]-5,
                           data.points[-1][0]+5,data.points[-1][1]+5,
                           fill=data.color, width = 0)
                           
def changeColor(color, data):
    data.color = color
    data.temp = color
    
def changeFunction(function, data):
    data.function = function
    if data.function == "pen":
        data.color = data.temp
    
def drawButtons(canvas, data):
    data.colorButtons = [None]*len(data.colors)
    for num in range(len(data.colors)):
        button1 = Button(canvas, text = data.colors[num],anchor = CENTER)
        button1.configure(width = data.rectWidth//8,height=data.rectHeight//15, 
                          activebackground = "#33B5E5")
        data.colorButtons[num]=(button1)
    data.colorButtons[0].configure(command=lambda:changeColor(data.colors[0],data))
    data.colorButtons[1].configure(command=lambda:changeColor(data.colors[1],data))
    data.colorButtons[2].configure(command=lambda:changeColor(data.colors[2],data))
    data.colorButtons[3].configure(command=lambda:changeColor(data.colors[3],data))
    data.colorButtons[4].configure(command=lambda:changeColor(data.colors[4],data))
    data.colorButtons[5].configure(command=lambda:changeColor(data.colors[5],data))
    data.colorButtons[6].configure(command=lambda:changeColor(data.colors[6],data))
    for num in range(len(data.colorButtons)):
        data.colorButtons[num].place(x=data.width-data.rectWidth,
                                     y=data.rectHeight*num)
    data.functionButtons = [None]*len(data.functions)
    for num in range(len(data.functions)):
        button1 = Button(canvas, text = data.functions[num],anchor = CENTER)
        button1.configure(width = data.rectWidth//8,height=data.rectHeight//15,
                          activebackground = "#33B5E5")
        data.functionButtons[num]=(button1)
    data.functionButtons[0].configure(command=lambda:changeFunction(data.functions[0],data))
    data.functionButtons[1].configure(command=lambda:changeFunction(data.functions[1],data))
    data.functionButtons[2].configure(command=lambda:changeFunction(data.functions[2],data))
    data.functionButtons[3].configure(command=lambda:changeFunction(data.functions[3],data))
    data.functionButtons[4].configure(command=lambda:changeFunction(data.functions[4],data))
    for num in range(len(data.functionButtons)):
        data.functionButtons[num].place(x=data.width-2*data.rectWidth,
                                        y=data.rectHeight*num)
        
                           
def timerFired(canvas, data):
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    data.cursor = (root.winfo_pointerx()-root.winfo_rootx(), 
                   root.winfo_pointery()-root.winfo_rooty())
    if data.function == "pen":
        pen(data)
    if data.function == "erase":
        erase(data)
    
####################################
# use the run function as-is
####################################
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        #canvas.delete(ALL)
        #canvas.create_rectangle(0, 0, data.width, data.height,
                                #fill='white', width=0)
                                
        redrawAll(canvas, data)
        canvas.update()    

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
        
    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)
        
    def mouseReleasedWrapper(event, canvas, data):
        mouseReleased(event, data)
        redrawAllWrapper(canvas, data)
        
    def motionWrapper(event, canvas, data):
        motion(event, data)
        redrawAllWrapper(canvas, data)
        
    def timerFiredWrapper(canvas, data):
        timerFired(canvas, data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1 # milliseconds
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<ButtonRelease-1>", lambda event: 
                            mouseReleasedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind('<Motion>', lambda event: 
                            motionWrapper(event, canvas, data))
    canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
    timerFiredWrapper(canvas, data)
    drawButtons(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(700, 700)
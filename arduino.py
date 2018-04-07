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
    data.color = "purple"
    data.function = "pen"
    data.points = []
    data.cursor = (data.width/2, data.height/2)
    data.pressed = False
    
def pen(data):
    if data.pressed:
        data.points.append(data.cursor)
        
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
        canvas.create_oval(data.points[-1][0]-5,data.points[-1][1]-5,data.points[-1][0]+5,data.points[-1][1]+5,fill=data.color, width = 0)
                           
def timerFired(canvas, data):
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    data.cursor = (root.winfo_pointerx() - root.winfo_rootx(), root.winfo_pointery() - root.winfo_rooty())
    if data.function == "pen":
        pen(data)
    
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
    root.bind("<ButtonRelease-1>", lambda event: mouseReleasedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind('<Motion>', lambda event: motionWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(700, 700)
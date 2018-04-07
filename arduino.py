from tkinter import *
from math import *

####################################
# customize these functions
####################################


root = Tk()
sys.setrecursionlimit(490000)

# Set up the model data with init
# init is called once, at the beginning of the program
# data is a Struct, which can be given new data values using data.name = value
# data will be shared across all animation functions- it's aliased!
def init(data):
    data.radius = 5 #radius of our eraser
    # data comes preset with width and height, from the run function
    data.color = 0
    data.function = 0
    data.cursor = (data.width//2, data.height//2)
    data.pressed = False
    data.colors = ["black", "red", "blue", "green", "yellow", "purple", "brown", "white"]
    data.functions = ["pointer", "pen", "fill", "erase", "thicker", "thinner", "save"]
    data.rectWidth = data.width // 10
    data.rectHeight = data.height // len(data.colors)
    data.board = []
    data.cellWidth = 10
    for i in range(data.height):
        data.board += [[7]*((data.width))]
    data.temp = 0
    
def pen(data):
    x = data.cursor[0]
    y = data.cursor[1]
    #print(data.color)
    if data.pressed:
        for i in range(data.radius//2):
            for j in range(int(2*pi)):
                if 0 <= int(y+i*sin(j)) < data.height and 0 <= int(x+i*cos(j)) < data.width:
                    data.board[int(y+i*sin(j))][int(x+i*cos(j))] = data.color
    #print(data.board)
       # data.board[int(data.cursor[1])][int(data.cursor[0])] = data.color

def erase(data):
    data.color = 7
    x = data.cursor[0]
    y = data.cursor[1]
    #print(data.color)
    if data.pressed:
        for i in range(data.radius):
            for j in range(int(2*pi)):
                if 0 <= int(y+i*sin(j)) < data.height and 0 <= int(x+i*cos(j)) < data.width:
                    data.board[int(y+i*sin(j))][int(x+i*cos(j))] = data.color
    #print(data.board)
    
def fill(canvas, data, x, y):
    #"hidden" stop clause - not reinvoking for "c" or "b", only for "a"
    if x==0 or y==0 or x==len(data.board)-1 or y==len(data.board[x])-1:
        return
    if data.board[x][y]!=7:
        return
    if data.board[x][y] == 7:
        data.board[x][y] = data.color
        canvas.create_rectangle(y,x,y+1,x+1,fill=data.colors[data.board[x][y]], width=0)
        #recursively invoke flood fill on all surrounding cells:
        if x > 0:
            fill(canvas, data, x-1, y)
        if x < len(data.board[y])-1:
            fill(canvas, data,x+1,y)
        if y > 0:
            fill(canvas, data,x,y-1)
        if y < len(data.board)-1:
            fill(canvas, data,x,y+1)

def thicken(data):
    if data.radius + 2 < 21:
        data.radius += 2

def thin(data):
    if data.radius - 2 >0:
        data.radius -= 2
'''def fill(data):
    smallest = []
    lst = giveListOfBiggerX(data)
    for i in range(lst):'''


def motion(event, data):
    data.cursor = (root.winfo_pointerx()-root.winfo_rootx(), \
        root.winfo_pointery()-root.winfo_rooty())
    #print(data.cursor)
    
def mousePressed(canvas, event, data):
    if event.x>data.width-2*data.rectWidth:
        print("no")
        return
    data.pressed = True
    if data.function == 2:
        fill(canvas, data, int(event.y), int(event.x))
    
def mouseReleased(event, data):
    data.pressed = False

'''def giveListOfBiggerX(data):
    lst = []
    for point in range(data.points):
        if point[0] >= data.cursor:
            lst += [point]
    return lst'''

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
    if data.functions[data.function] == "erase" and data.pressed:
        #canvas.create_oval(data.cursor[0]-10, data.cursor[1]-10, 
        #                   data.cursor[0]+10, data.cursor[1]+10)
        x1,y1 = data.cursor[0]-data.radius, data.cursor[1]-data.radius
        x2,y2 = data.cursor[0]+data.radius, data.cursor[1]+data.radius
        canvas.create_oval(x1,y1,x2,y2, fill=data.colors[7], width = 0)

    elif data.functions[data.function] == "pen" and data.pressed:
        x1,y1 = data.cursor[0]-data.radius/2, data.cursor[1]-data.radius/2
        x2,y2 = data.cursor[0]+data.radius/2, data.cursor[1]+data.radius/2
        canvas.create_oval(x1, y1, x2, y2, fill=data.colors[data.color], width = 0)
        
    #elif data.functions[data.function] == "fill" and data.pressed:
        # x,y=data.cursor[0],data.cursor[1]
        # toBeFilled = {(x, y)}
        # while toBeFilled:
        #     tbf = set()
        #     for x, y in toBeFilled:
        #         try:
        #             if data.board[x][y] == 7: continue #Pixel is already 1 -> no action
        #         except IndexError: continue #Index is out of bounds
        #         canvas.create_rectangle(x-1,y-1,x+1,y+1,fill=data.colors[data.color])
        #         for xoff, yoff in ((1, -1), (1, 0), (1, 1), (0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)):
        #             tbf |= {(x + xoff, y + yoff)} #add adjacent pixels
        #     toBeFilled = tbf
                    

                           
def changeColor(color, data):
    data.color = color
    data.temp = color
    
def changeFunction(function, data):
    data.function = function
    print(data.function)
    if data.functions[data.function] == "pen":
        data.color = data.temp
    
def drawButtons(canvas, data):
    data.colorButtons = [None]*len(data.colors)
    for num in range(len(data.colors)):
        button1 = Button(canvas, text = data.colors[num],anchor = CENTER)
        button1.configure(width = data.rectWidth//8,height=data.rectHeight//15, 
                          activebackground = "#33B5E5")
        data.colorButtons[num]=(button1)
    data.colorButtons[0].configure(command=lambda:changeColor(0,data))
    data.colorButtons[1].configure(command=lambda:changeColor(1,data))
    data.colorButtons[2].configure(command=lambda:changeColor(2,data))
    data.colorButtons[3].configure(command=lambda:changeColor(3,data))
    data.colorButtons[4].configure(command=lambda:changeColor(4,data)) 
    data.colorButtons[5].configure(command=lambda:changeColor(5,data))
    data.colorButtons[6].configure(command=lambda:changeColor(6,data))
    for num in range(len(data.colorButtons)-1):
        data.colorButtons[num].place(x=data.width-data.rectWidth,
                                     y=data.rectHeight*num)
    data.functionButtons = [None]*len(data.functions)
    for num in range(len(data.functions)):
        button1 = Button(canvas, text = data.functions[num],anchor = CENTER)
        button1.configure(width = data.rectWidth//8,height=data.rectHeight//15,
                          activebackground = "#33B5E5")
        data.functionButtons[num]=(button1)
    data.functionButtons[0].configure(command=lambda:changeFunction(0,data))
    data.functionButtons[1].configure(command=lambda:changeFunction(1,data))
    data.functionButtons[2].configure(command=lambda:changeFunction(2,data))
    data.functionButtons[3].configure(command=lambda:changeFunction(3,data))
    data.functionButtons[4].configure(command=lambda:thicken(data))
    data.functionButtons[5].configure(command=lambda:thin(data))
    data.functionButtons[6].configure(command=lambda:changeFunction(6,data))
    for num in range(len(data.functionButtons)):
        data.functionButtons[num].place(x=data.width-2*data.rectWidth,
                                        y=data.rectHeight*num)
        
                           
def timerFired(canvas, data):
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    #data.cursor = (root.winfo_pointerx()-root.winfo_rootx(), 
    #               root.winfo_pointery()-root.winfo_rooty())
    if data.functions[data.function] == "pen":
        pen(data)
    if data.functions[data.function] == "erase":
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
        mousePressed(canvas, event, data)
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

run(300, 300)
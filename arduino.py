from tkinter import *
from math import *
import string
from PIL import Image, ImageDraw, ImageTk
#import tkSimpleDialog

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
    data.functions = ["pointer", "pen", "fill", "erase", "thicker", "thinner", "save", "load"]
    data.rectWidth = data.width // 10
    data.rectHeight = data.height // len(data.colors)
    data.board = []
    data.cellWidth = 10
    for i in range(data.height):
        data.board += [[7]*((data.width))]
    data.temp = 0
    data.colorCode = [(0,0,0), (255,0,0), (0,0,255), (0,128,0), (255,255,0), (128,0,128), (165,42,42), (255,255,255)]#[(1,1,1), (170,39,31), (25,8,146), (36,107,31), (227,244,106), (95,24,100), (120,59,74), (255,255,255)] #Drawing red in PIL is different from generic red
    data.filename = "Example.jpg"
    data.previousText = "Selected: " + data.functions[data.function].upper() + " " + "Color: " + data.colors[data.color].upper() + " " + str(data.radius//2)

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
    if data.radius - 2 > 0:
        data.radius -= 2

def save(data):
    '''filename = open("Example.txt","w")'''
    '''for i in range(len(data.board)):
        for j in range(len(data.board[0])):
            if j != len(data.board[0])-1:
                filename.write(str(data.board[i][j]) + ",")
            else:
                filename.write(str(data.board[i][j]))
            #filename.write("hi!")
        if i != len(data.board)-1:
            filename.write('|\n')
    filename.close()'''
    image1 = Image.new("RGB", (data.width, data.height), 'white')
    draw = ImageDraw.Draw(image1)
    for i in range(len(data.board)):
        for j in range(len(data.board[0])):
            draw.point([(j,i)], fill = data.colors[data.board[i][j]])
    image1.save(data.filename)

'''def readFile(path):
    with open(path, "rt") as f:
        return f.read()'''

def load(canvas, data):
    '''
    filename = readFile("Example.txt")
    temp = []
    #print(filename)
    #print(type(filename))
    for row in range(len(filename.split("|"))): #The split function is way to laggy because of the huge amount of data we are looking at
        a = []
        for col in range(len((filename.split('|')[row]).split(","))):
            value = int(filename.split('|')[row].split(',')[col])
            canvas.create_oval(row,col, row+1, col + 1, fill = data.colors[value], width = 0)
            a += [int(value)]
        temp += [a]
    data.board = temp
    #except:
    #    print("Invalid File")
    '''
    try:
        image = Image.open(data.filename)
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0,0, anchor = NW, image = photo)
        img = Image.open(data.filename).convert("RGB")
        pix = img.load()
    except:
        print("Error, file not Found")
    for i in range(len(data.board)):
        for j in range(len(data.board[0])):
            data.board[i][j] = data.colorCode.index(pix[j,i])
        
    #if pix[j,i] in data.colorCode:
    '''minVal = 100
    mini = (255,255,255)
    for k in data.colorCode:
        if pix[j,i][0] - k[0] + pix[j,i][1] - k[1] + pix[j,i][2] - k[2] < minVal:
            mini = k
            minVal = pix[j,i][0] - k[0] + pix[j,i][1] - k[1] + pix[j,i][2] - k[2]
    data.board[i][j] = data.colorCode.index(mini)'''
    #print(pix[i,j])
    

'''def saveFile(canvas, data):
    name = StringVar()
    entry_box = Entry(root, textvariable=name, width = 25, bg='white').place(x=data.width//2, y=data.height//2)
    saver = Button(root, text = "Save", width = 30, height = 30, bg = 'lightblue', command=save).place(x=data.width//2, y=data.height*2//3)'''
def fill(canvas, data, x, y):
    #"hidden" stop clause - not reinvoking for "c" or "b", only for "a"
    if x==0 or y==0 or x==len(data.board)-1 or y==len(data.board[x])-1:
        return
    if data.board[x][y]!=7 or data.board[x-1][y-1]!=7 or data.board[x-1][y+1]!=7 or data.board[x+1][y-1]!=7 or data.board[x+1][y+1]!=7:
        return
    if data.board[x][y] == 7:
        data.board[x][y] = data.color
        data.board[x+1][y]=data.color
        data.board[x-1][y]=data.color
        data.board[x][y+1]=data.color
        data.board[x][y-1]=data.color
        canvas.create_rectangle(y-1,x-1,y+2,x+2,fill=data.colors[data.board[x][y]], width=0)
        #recursively invoke flood fill on all surrounding cells:
        if x > 0:
            fill(canvas, data,x-2,y)
        if x < len(data.board[y])-1:
            fill(canvas, data,x+2,y)
        if y > 0:
            fill(canvas, data,x,y-2)
        if y < len(data.board)-1:
            fill(canvas, data,x,y+2)

def motion(event, data):
    data.cursor = (root.winfo_pointerx()-root.winfo_rootx(), \
        root.winfo_pointery()-root.winfo_rooty())
    #print(data.cursor)
    
def mousePressed(canvas, event, data):
    if root.winfo_pointerx()-root.winfo_rootx()>data.width-2*data.rectWidth:
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
    #if data.functions[data.function] == "save":
    #    tkSimpleDialog.askstring(title, prompt [initialvalue])
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
    #canvas.create_text(5, data.height, anchor = SW, text = data.previousText, fill = "white", width = 0)
    #canvas.create_text(5,data.height, anchor = SW, text = "Selected: " + data.functions[data.function].upper() + " " + "Color: " + data.colors[data.color].upper() + " " + str(data.radius//2), width = 0)
    #data.previousText = "Selected: " + data.functions[data.function].upper() + " " + "Color: " + data.colors[data.color].upper() + " " + str(data.radius//2)
        
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
    #print(data.function)
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
    data.functionButtons[6].configure(command=lambda:save(data))
    data.functionButtons[7].configure(command=lambda:load(canvas,data))
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
    #if data.functions[data.function] == "save":
    #    saveFile(canvas, data)
    
####################################
# use the run function as-is
####################################
def run(width=300, height=300):
    '''def printtext():
        
        name = StringVar()
        string = name.get()
        print(string)
        print('hi')'''
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
    #print(data.function)
    # and launch the app
    '''name = StringVar()
    e = Entry(root)
    e.pack()
    e.focus_set()

    b = Button(root,text='okay',command=printtext)
    b.pack(side='bottom')'''
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(500,500)
from tkinter import filedialog
from tkinter import colorchooser
from tkinter import *
from math import *
import string
from PIL import Image, ImageDraw, ImageTk
#import tkSimpleDialog

#Thanks to the contribution by William Cen --> https://github.com/Willyou2/2018Hack112/commits/master version: 3ab60e0
#Thanks to Bresenham algorithm
#Thanks to Matt Kong for Mentor help
#

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
    data.radius = 5 #radius of our eraser, which is 2 times the radius of the pen
    # data comes preset with width and height, from the run function
    data.color = (0,0,0)
    data.function = 0
    data.cursor = (data.width//2, data.height//2)
    data.pressed = False
    data.colors = ["black", "red", "blue", "green", "yellow", "purple", "brown", "white", "Help"] #Careful, includes new functions
    data.functions = ["pointer", "pen", "fill", "erase", "thicker", "thinner", "save", "load", "clear", "rect", "line", "edit color"]#, "testEntry"]
    data.rectWidth = data.width // 10
    data.rectHeight = data.height // len(data.functions)
    data.functHeight = data.height // len(data.functions)
    data.board = []
    data.cellWidth = 10
    #IF FLOODFILL FAILS JUST ADJUST THE HEIGHT BACK TO REGULAR
    for i in range(data.height + 1): #+1 because the board pixels go from 0 to 500, so there needs to be a 500th cell
        data.board += [[(255,255,255)]*((data.width-2*data.rectWidth+1))] #-data.rectWidth//4 because 2times the width of the rectangles. Change later when you configure it properly
    data.temp = (0,0,0)
    data.colorCode = [(0,0,0), (255,0,0), (0,0,255), (0,128,0), (255,255,0), (128,0,128), (165,42,42), (255,255,255)]#[(1,1,1), (170,39,31), (25,8,146), (36,107,31), (227,244,106), (95,24,100), (120,59,74), (255,255,255)] #Drawing red in PIL is different from generic red
    data.filename = "Example.jpg"
    #data.previousText = "Selected: " + data.functions[data.function].upper() + " " + "Color: " + data.colors[data.color].upper() + " " + str(data.radius//2)
    image = Image.open("Title.jpg")
    data.title = ImageTk.PhotoImage(image)
    data.count = 0
    data.colorFill = data.color #If you select a box to fill, the color of the pixel is what it will check for your box to be equal to
    ####### Shape Parameters #######
    data.rect = [(0,0),(0,0)] #Might consider making rect a class and making a list of those classes so you can select and move these shapes. First coord is the initial point, which will be set by a buttonpressed function. The second is the point where you're dragging it to. When you button-release, it will draw the rectangle.
    data.oval = [(0,0),(0,0)]
    data.line = [(0,0),(0,0),0] #third coordinate is the slope. The x0,y0 and xf,yf are the midpoints of the pixel. Slope calculated by midpoints
    data.shape = None #This will be set equal to some create_something depending on shape draw so it can be deleted and recreated. It's arbitrary since what it's set equal to will be deleted and recreated depending on your shape
    data.sWidth = 5 #Shape width

def rgbtoTk(rgb):
    a, b, c = int(rgb[0]), int(rgb[1]), int(rgb[2])
    colorval = "#%02x%02x%02x" % (a,b,c)
    return colorval

def fillDot(data, row, col, center, color): #Center is a tuple that is constant
    #FIX THE ERROR IN THE ELIF = DATA.COLOR BY FIRST RUNNING A REUCURSIVE FUNC THAT FINDS IF THERES A WHITE SPOT STILL WITHIN RADIUS THEN SEND THAT INITIAL ROW/COL HERE BUT KEEP CENTER
    centerBox = (row+0.5, col + 0.5) #Finds center of current box
    dist = (centerBox[0]-center[0])**2 + (centerBox[1]-center[1])**2
    if row <= 0 or col <= 0 or row >= len(data.board)-1 or col >= len(data.board[row]):
        return
    elif data.board[row][col] == color: #This is to prevent issues with crashing (which is due to infinite loop since each move goes around the circle infinitely) but it brings the issue of if you click a circle in another and the center immediately is surrounded by the color, it wont fill
        return
    elif dist > data.radius**2 and data.function == 3:
        return
    elif dist > 0.25*data.radius**2 and data.function != 3: #0.25 because radius is radius of eraser
        return
    else:
        data.board[row][col] = color
        fillDot(data, row+1, col, center, color)
        fillDot(data, row-1, col, center, color)
        fillDot(data, row, col + 1, center, color)
        fillDot(data, row, col - 1, center, color)

def findDiffColor(data, row, col, center): #Make sure this recursive function calls the fillDot whenever it finds a whitespot
    #I can tell this will be one hell of an AIDS inducing backtracking thing
    pass

def pen(data):
    row = data.cursor[1]
    col = data.cursor[0]
    #print(data.color)
    if data.pressed:
        '''for i in range(data.radius//2):
            for j in range(int(2*pi)):
                if 0 <= int(y+i*sin(j)) < data.height and 0 <= int(x+i*cos(j)) < data.width:
                    data.board[int(y+i*sin(j))][int(x+i*cos(j))] = data.color'''
        fillDot(data, row, col, (row+0.5, col+0.5), data.color)
    #print(data.board)
       # data.board[int(data.cursor[1])][in  t(data.cursor[0])] = data.color

def erase(data):
    data.temp = data.colorCode[7]
    x = data.cursor[1]
    y = data.cursor[0]
    #print(data.color)
    if data.pressed:
        '''for i in range(data.radius): #The issue with this is that you are looping through integer values for radius and theta, so you dont really reach all boxes. This is evident by the fact that your values are stars
            for j in range(int(2*pi)):
                if 0 <= int(y+i*sin(j)) < data.height and 0 <= int(x+i*cos(j)) < data.width:
                    data.board[int(y+i*sin(j))][int(x+i*cos(j))] = data.color'''
        fillDot(data, x, y, (x+0.5, y + 0.5), data.temp)            
    #print(data.board)
    
'''def fill(canvas, data, x, y):
    #"hidden" stop clause - not reinvoking for "c" or "b", only for "a"
    if x<=0 or y<=0 or x==len(data.board)-1 or y==len(data.board[x])-1:
        return
    if data.board[x][y]!=data.colorFill:
        return
    if data.board[x][y] == data.colorFill:
        data.board[x][y] = data.color
        canvas.create_rectangle(y,x,y+1,x+1,fill=data.colors[data.board[x][y]], width=0)
        #recursively invoke flood fill on all surrounding cells:
        #if x > 0:
        fill(canvas, data, x-1, y)
        #if x < len(data.board[y])-1:
        fill(canvas, data,x+1,y)
        #if y > 0:
        fill(canvas, data,x,y-1)
        #if y < len(data.board)-1:
        fill(canvas, data,x,y+1)'''

def thicken(data):
    if data.radius + 2 < 21:
        data.radius += 2

def thin(data):
    if data.radius - 2 > 0:
        data.radius -= 2

def testEntry(data):
    master = Tk()
    e = Entry(master)
    e.grid(row=0, column=1)
    #e.focus_set()
    Label(master, text="SaveName").grid(row=0)
    #Label(master, text="Last Name").grid(row=1)

    #e1 = Entry(master)
    #e2 = Entry(master)

    #e1.grid(row=0, column=1)
    #e2.grid(row=1, column=1)
    def callback():
        print(e.get())

    def combine_funcs(*funcs): #Cited from https://stackoverflow.com/questions/13865009/have-multiple-commands-when-button-is-pressed
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func
    b = Button(master, text = "get", width = 10, command=callback)
    b.grid(row=1)
    #b.pack()
    c = Button(master, text = "close", width = 10, command=combine_funcs(e.grid_remove, master.destroy))
    c.grid(row=2)
    #c.pack()
    d = Button(master, text = "quit", width = 10, command=master.destroy)
    d.grid(row=3)
    #d.pack()
    master.mainloop()
    #e= Entry(root, width = 50)
    #e.pack()
    #text = e.get()

def saveData(data, name):
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
    image1 = Image.new("RGB", (len(data.board[0])-1, len(data.board)-1), 'white') #Maybe subtract 1 because goes from 0 to that point whereas board is different
    #Image.new("RGB", (len(data.board[0]), len(data.board[1])), 'white')
    draw = ImageDraw.Draw(image1)
    for i in range(len(data.board)):
        for j in range(len(data.board[0])):
            draw.point([(j,i)], fill = data.board[i][j])
    filename = name# + ".jpg"
    #print(filename)
    image1.save(filename)

    '''def readFile(path):
        with open(path, "rt") as f:
            return f.read()'''


def save(data):
    master = Tk()
    filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file", defaultextension = "*.*", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    print(filename)
    #filename.split("/")
    e = Entry(master)
    e.grid(row=0, column=1)
    e.delete(0, END)
    e.insert(0, filename)
    #e.focus_set()
    Label(master, text="SaveName").grid(row=0)
    #Label(master, text="Last Name").grid(row=1)

    #e1 = Entry(master)
    #e2 = Entry(master)

    #e1.grid(row=0, column=1)
    #e2.grid(row=1, column=1)
    def callback():
        print(e.get())

    def combine_funcs(*funcs): #Cited from https://stackoverflow.com/questions/13865009/have-multiple-commands-when-button-is-pressed
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func
    def saver(data, name = e.get()):
        saveData(data, name)
    #if filename == '':
    #    filename = e.get()
    #b = Button(master, text = "get", width = 10, command=callback)
    #b.grid(row=1)
    #b.pack()
    c = Button(master, text = "Save", width = 10, command= lambda:combine_funcs(saveData(data, e.get()),master.destroy()))
    c.grid(row=1)
    #c.pack()
    d = Button(master, text = "quit", width = 10, command=master.destroy)
    d.grid(row=2)
    #d.pack()
    master.mainloop()
    #e= Entry(root, width = 50)
    #e.pack()
    #text = e.get()

def load(canvas, data):
    master = Tk()
    filename = filedialog.askopenfilename(initialdir = '/', title = 'Select File', filetypes = (("jpeg files","*.jpg"),("all files", "*.*")))
    print(filename)
    e = Entry(master)
    e.grid(row=0, column=1)
    e.delete(0, END)
    e.insert(0, filename)
    #e.focus_set()
    Label(master, text="SaveName").grid(row=0)
    #Label(master, text="Last Name").grid(row=1)

    #e1 = Entry(master)
    #e2 = Entry(master)

    #e1.grid(row=0, column=1)
    #e2.grid(row=1, column=1)
    def callback():
        print(e.get())

    def combine_funcs(*funcs): #Cited from https://stackoverflow.com/questions/13865009/have-multiple-commands-when-button-is-pressed
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func
    #def saver(data, name = e.get()):
    #    saveData(data, name)

    #b = Button(master, text = "get", width = 10, command=callback)
    #b.grid(row=1)
    #b.pack()
    c = Button(master, text = "Load", width = 10, command= lambda:combine_funcs(loadData(canvas, data, e.get()), master.destroy())) #Doesnt destroy because load fails because of rgb problem. Easy fix just use rgbs instead of color names
    c.grid(row=1)
    #c.pack()
    d = Button(master, text = "quit", width = 10, command=master.destroy)
    d.grid(row=2)
    #d.pack()
    master.mainloop()
    #e= Entry(root, width = 50)
    #e.pack()
    #text = e.get()


def loadData(canvas, data, name): #LOAD PROBLEM: AFTER CLEARING BOARD CANT SEEM TO LOAD UNLESS RESTART APP
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
    filename = name
    try:
        image = Image.open(filename)
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0,0, anchor = NW, image = photo)
        img = Image.open(filename).convert("RGB")
        pix = img.load()
    except:
        print("Error, file not Found")
    print(pix[50,50])
    for i in range(len(data.board)+1):
            for j in range(len(data.board[0])):
                data.board[i][j] = pix[j,i]
        
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

#Increase stack size

def chooseColor(data):
    color = colorchooser.askcolor()[0]
    color = list(color)
    color[0] = int(color[0])
    color[1] = int(color[1])
    color[2] = int(color[2])
    data.color = (color[0],color[1],color[2])

def callWithLargeStack(f,*args):
    import sys
    import threading
    threading.stack_size(2**27)  # 64MB stack
    sys.setrecursionlimit(2**27) # will hit 64MB stack limit first
    # need new thread to get the redefined stack size
    def wrappedFn(resultWrapper): resultWrapper[0] = f(*args)
    resultWrapper = [None]
    #thread = threading.Thread(target=f, args=args)
    thread = threading.Thread(target=wrappedFn, args=[resultWrapper])
    thread.start()
    thread.join()
    return resultWrapper[0]

def fill(canvas, data, x, y): #might be stack overflow because the edges are no longer smooth but rather jagged due to circles?
    #"hidden" stop clause - not reinvoking for "c" or "b", only for "a"
    print(y,x)
    if x-1<=0 or y-1<=0 or x+1>=len(data.board)-1 or y+1>=len(data.board[0])-1: 
        return
    elif data.color == data.colorFill:
        return
    elif data.board[x][y]!=data.colorFill:# or data.board[x-1][y-1]!= data.colorFill or data.board[x-1][y+1]!=data.colorFill or data.board[x+1][y-1]!=data.colorFill or data.board[x+1][y+1]!=data.colorFill:
        return
    elif data.board[x][y] == data.colorFill: #Even though this is correct, it runs into error if you fill in a spot with the same color you want to fill it with ex: filling in an already black circle with black
        data.board[x][y] = data.color
        #data.board[x+1][y]=data.color
        #data.board[x-1][y]=data.color
        #data.board[x][y+1]=data.color
        #data.board[x][y-1]=data.color
        #canvas.create_rectangle(y-1,x-1,y+2,x+2,fill=data.colors[data.board[x][y]], width=0)
        color = rgbtoTk(data.color)
        canvas.create_rectangle(y,x,y+1,x+1,fill=color, width=0)
        #recursively invoke flood fill on all surrounding cells:
        #if x > 0: 

        ################ REMEMBER X IS Y COORD AND Y IS X COORD 

        fill(canvas, data,x-1,y)
        fill(canvas, data,x,y-1) #Commenting this out also crashes python and only this
        #if x < len(data.board[y])-1:
        fill(canvas, data,x+1,y)
        #if y > 0:
        
        #if y < len(data.board)-1:
        fill(canvas, data,x,y+1)
        #Notes: Shawn's fill function works better than mine which is by changing everything to not fill x-2 but rather x-1 and commenting out the above if statements of like data.board[x-1][y-1]!= data.colorFill
        #This is either efficiency reason or because there are gaps in the object when i fill in a space no matter how thick (cuz pixels are small af)
        #To fix this, try to make the draw function properly hit every pixel 


def clearBoard(canvas, data):
    data.board = []
    for i in range(data.height + 1): #+1 because the board pixels go from 0 to 500, so there needs to be a 500th cell
        data.board += [[(255,255,255)]*((data.width-2*data.rectWidth+1))]
    canvas.delete(ALL)
    white = rgbtoTk((255,255,255))
    canvas.create_rectangle(0, 0, data.width, data.height,\
                                fill=white, width=0)

def motion(event, data):
    data.cursor = (root.winfo_pointerx()-root.winfo_rootx(), \
        root.winfo_pointery()-root.winfo_rooty())
    #print(data.cursor)
    
def mousePressed(canvas, event, data):
    if root.winfo_pointerx()-root.winfo_rootx()>data.width-2*data.rectWidth:#Keep not //8 because otherwise crashes
        return
    data.pressed = True
    if data.function == 2:
        #print(event.x, event.y)
        data.colorFill = data.board[event.y][event.x]
        
        fill(canvas, data, int(event.y), int(event.x)) #Ask shawn why he passed event.y then event.x instead of the other way around
    
def mouseReleased(event, data):
    data.pressed = False
    #print("Event: (" + str(event.x) + "," + str(event.y))
    #print("Event: (" + str(root.winfo_pointerx()-root.winfo_rootx()) + "," + str(root.winfo_pointery()-root.winfo_rooty())) #To compare winfo to event

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

def keyPressed(event, data): #DEBUGGING
    if event.char == "a":
        print(data.board)
    if event.char == "b":
        print(data.cursor[0], data.cursor[1], end = ' ')
        print(len(data.board), len(data.board[0]))
    if event.char == "c":
        print(data.height, data.width, '')

    if event.char == "d":
        print(data.cursor[0], data.cursor[1], end = ' ')
        print(event.x, event.y )
    if event.keysym == "Escape":
        quit()
    if event.char == "2":
        print(data.color, end = " ")
        print(rgbtoTk(data.color))
    if event.char == "3":
        print(data.board[10][10])
    data.charText = event.char
    data.keysymText = event.keysym


###############################
######## Shape Drawing ########
###############################

def initPoint(canvas, data): #On mouse clicked
    if data.functions[data.function] == "rect":
        x = root.winfo_pointerx()-root.winfo_rootx()
        y = root.winfo_pointery()-root.winfo_rooty()
        data.rect[0] = (x, y)
        data.rect[1] = (x, y) #initialize this even though it will change
        data.shape = canvas.create_rectangle(data.rect[0], data.rect[1], fill = '')
    if data.functions[data.function] == "oval":
        x = root.winfo_pointerx()-root.winfo_rootx()
        y = root.winfo_pointery()-root.winfo_rooty()
        data.oval[0] = (x, y)
        data.oval[1] = (x, y) #initialize this even though it will change
        data.shape = canvas.create_oval(data.oval[0], data.oval[1], fill = '')
    if data.functions[data.function] == "line":
        x = root.winfo_pointerx()-root.winfo_rootx()
        y = root.winfo_pointery()-root.winfo_rooty()
        data.line[0] = (x, y)
        data.line[1] = (x, y)
        data.line[2] = 0
        color = rgbtoTk(data.color)
        data.shape = canvas.create_line(data.line[0], data.line[1], fill = color)


def drawShape(canvas, data): #On b1-motion
    #The following if elif else are to determine whether you're inside the box or not
    color = rgbtoTk(data.color)
    if root.winfo_pointerx()-root.winfo_rootx() > len(data.board[0])-1:
        x = len(data.board[0]) - 1
    elif root.winfo_pointerx()-root.winfo_rootx() < 0:
        x = 0
    else:
        x = root.winfo_pointerx()-root.winfo_rootx()
    if root.winfo_pointery()-root.winfo_rooty() > len(data.board)-1:
        y = len(data.board)-1
    elif root.winfo_pointery()-root.winfo_rooty() < 0:
        y = 0
    else:
        y = root.winfo_pointery()-root.winfo_rooty()
    if data.functions[data.function] == "rect":
        data.rect[1] = (x,y)
        canvas.delete(data.shape) #Deletes previous shape, but wont keep deleting since this function only works if both B1 and motion
        data.shape = canvas.create_rectangle(data.rect[0], data.rect[1], fill = '', width = data.sWidth, outline = color)
    # Implement a line drawing function with arbitrary width. Idea to have thickness bigger than 1 is to simply do 2 way bresenham alg: first to draw a 1d line, then add more lines above it. However, to make sure the lines above are started at the right point, depending on the angled line, u have another line (the width of the line) that is orthogonal, so use bresenham to decide start points
    if data.functions[data.function] == "line":
        data.line[1] = (x,y)
        try:data.line[2] = (y-data.line[0][1])/(x-data.line[0][0])
        except: data.line[2] = (y-data.line[0][1]+1)/(x-data.line[0][0]+1)
        canvas.delete(data.shape)
        data.shape = canvas.create_line(data.line[0], x, y, fill = color, width = data.sWidth)

def getHelp(data):
    root2 = Tk()
    #canvas2 = Canvas(root2, 500, 500)
    #canvas.pack()
    #canvas2.create

    #################
    ##### SETUP #####
    #################
    helpFrame = []
    for i in range(len(data.functions)):
        helpFrame += [(Text(root2, height=20, width=30), Text(root2, height=20, width=50), Scrollbar(root2, command=helpFrame[i][1].yview))] #First frame is picture frame, Second frame is instruction frame, Third is scrollbar
        helpFrame[i][1].configure(yscrollcommand=helpFrame[i][2].set)
        helpFrame[i][1].tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
        helpFrame[i][1].tag_configure('big', font=('Verdana', 20, 'bold'))
        helpFrame[i][1].tag_configure('color', foreground='#476042', font=('Tempus Sans ITC', 12, 'bold'))



def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

def smallLineDraw(canvas, data, x, y, xf, yf, yBase): #put this in make shape. This is an implementation of Bresenham's algorithm
    #Assume abs(slope) less than 1 (diagonal down right). 
    #x0 and y0 are the midpoints of the pixel you are at, yBase initially is y0, slope is m
    #Pseudocode: step x+1
    #y+m. If y+m - yBase > 0.5, yBase += 1. Fill box of yBase
    #Recursively call itself again and change its y and x coord. 
    #base case: x, y equal final x and y #xF and yF are midpoints of box. Slope is calculated via those midpoints, so of course should eventually reach the point
    #dont worry abotu checking base case after x+1 or y+1 because the way we calculate slope, in order for it to reach the final point, it must complete the rise and run, otherwise it wont be a straight line
    if almostEqual(x,xf) and almostEqual(y, yf):
        return
    x += 1
    y += data.line[2]
    if abs(y - yBase) > 0.5: #Dont need to check this again for slope < 1 becasue it cannot possible cover more than 2 boxes in 1 try. If running slope > 1, then need to use a xBase instead
        if data.line[2] > 0:
            yBase += 1
        if data.line[2] < 0:
            yBase += -1
        #yBase += 1
    data.board[int(yBase - 0.5)][int(x - 0.5)] = data.color #yBase is fine instead of yBase + 1 because remember that y increases downwards. Also -0.5 because we are using midpoint for x as well
    smallLineDraw(canvas, data, x, y, xf, yf, yBase)

def largeLineDraw(canvas, data, x, y, xf, yf, xBase): #put this in make shape. This is an implementation of Bresenham's algorithm
    #Assumes slope is greater than 1 
    #Use dx/dy instead of dy/dx. Simply do 1/(dy/dx)
    #print("Initials", x, y, "Finals: ", xf, yf) 
    #NEED TO ROUND X AND Y ACCORDINGLY. ALSO, IF YOU DRAW A LINE DIFF DIRECTION, YOU ARE NO LONGER MOVING RIGHT DIRECTION
    if almostEqual(x,xf) and almostEqual(y, yf):
        return
    x += 1/data.line[2] #since dx/dy instead of dy/dx
    y += 1
    if abs(x - xBase) > 0.5: #Dont need to check this again for slope < 1 becasue it cannot possible cover more than 2 boxes in 1 try. If running slope > 1, then need to use a xBase instead
        if data.line[2] > 0: #Originally used for dealing with arbitrary situation, but we can just swap values if they dont work
            xBase += 1
        if data.line[2] < 0:
            xBase += -1
    #print(xBase, x)
    data.board[int(y - 0.5)][int(xBase - 0.5)] = data.color #yBase is fine instead of yBase + 1 because remember that y increases downwards. Also -0.5 because we are using midpoint for x as well
    largeLineDraw(canvas, data, x, y, xf, yf, xBase)

##########WIDTH DRAWERS################
#The xf and yf are the xf and yf of the width function (just calculate it)
#KEEP TRACK OF WHAT IS DEFINED AS DATA.LINE BECAUSE YOU SEND IN DIFF VALUES DEPENDING ON WHIH ONE IS LEFT SIDE WHICH IS RIGHT SIDE 
#Make sure to choose your x and y inital for smallDrawWidth to be the proper starting location (not necessarily data.line[0]. data.ne[0] is used and adjusted initially for the line creator)


#For x,y, determine inital x,y and final x,y 
def smallDrawWidth(canvas, data, x, y, yBase): #This is used when width slope is smaller than 1

    dist = ((data.line[0][0]-x)**2 + (data.line[0][1]-y)**2)**0.5
    if dist > data.sWidth:
        return
    #put this before changing values to ensure that it runs for every case
    longxf = x - data.line[0][0] + data.line[1][0]#++0.5 #adds difference to the end points to create new xf and yf for those
    longyf = y - data.line[0][1] + data.line[1][1]#+0.5 
    xBase = x
    largeLineDraw(canvas, data, x, y, longxf, longyf, xBase) #if the width has a small slope, then the orthogonal is large

    x += 1
    y += -1/data.line[2]

    if abs(y - yBase) > 0.5: #Dont need to check this again for slope < 1 becasue it cannot possible cover more than 2 boxes in 1 try. If running slope > 1, then need to use a xBase instead
        if data.line[2] > 0:
            yBase += 1
        if data.line[2] < 0:
            yBase += -1
    data.board[int(yBase - 0.5)][int(x - 0.5)] = data.color #yBase is fine instead of yBase + 1 because remember that y increases downwards. Also -0.5 because we are using midpoint for x as well
    smallDrawWidth(canvas, data, x, y, yBase)

def largeDrawWidth(canvas, data, x, y, xBase):
    dist = ((data.line[0][0]-x)**2 + (data.line[0][1]-y)**2)**0.5
    if dist > data.sWidth:
        return
    longxf = x - data.line[0][0] + data.line[1][0] #adds difference to the end points to create new xf and yf for those
    longyf = y - data.line[0][1] + data.line[1][1]
    yBase = y 
    smallLineDraw(canvas, data, x, y, longxf, longyf, yBase)

    x += -1*data.line[2]
    y += 1
    if abs(x - xBase) > 0.5: #Dont need to check this again for slope < 1 becasue it cannot possible cover more than 2 boxes in 1 try. If running slope > 1, then need to use a xBase instead
        if data.line[2] > 0:
            xBase += 1
        if data.line[2] < 0:
            xBase += -1
    data.board[int(y - 0.5)][int(xBase - 0.5)] = data.color #yBase is fine instead of yBase + 1 because remember that y increases downwards. Also -0.5 because we are using midpoint for x as well
    largeDrawWidth(canvas, data, x, y, xBase)


def makeShape(canvas, data): #on mouse released
    color = rgbtoTk(data.color)

    canvas.delete(data.shape)
    x = root.winfo_pointerx()-root.winfo_rootx()
    y = root.winfo_pointery()-root.winfo_rooty()
    if data.functions[data.function] == "rect":
        if abs(data.rect[0][0] - data.rect[1][0]) <= 10 or abs(data.rect[0][1] - data.rect[1][1]) <= 10: #If the difference is too small, it will create a rectangle of fixed size
            try: dx = (data.rect[1][0] - data.rect[0][0])/abs(data.rect[1][0] - data.rect[0][0])
            except: dx = (data.rect[1][0] - data.rect[0][0]+1)/abs(data.rect[1][0] - data.rect[0][0]+1)
            try: dy = (data.rect[1][1] - data.rect[0][1])/abs(data.rect[1][1] - data.rect[0][1])
            except: dy = (data.rect[1][1] - data.rect[0][1]+1)/abs(data.rect[1][1] - data.rect[0][1]+1)
            x = int(data.rect[0][0] + 10*dx)
            y = int(data.rect[0][1] + 10*dy)
            canvas.create_rectangle(data.rect[0], x, y, fill = color, width = data.sWidth, outline = color) #Choose some width for the rectangle
            for i in range(min(data.rect[0][1], y)-data.sWidth//2, max(data.rect[0][1], y)+data.sWidth//2+1):
                for j in range(min(data.rect[0][0], x)-data.sWidth//2, max(data.rect[0][0], x)+data.sWidth//2+1):
                    data.board[i][j] = data.color
        else:
            canvas.create_rectangle(data.rect[0], data.rect[1], fill = color, width = data.sWidth, outline = color)
            for i in range(min(data.rect[0][1], data.rect[1][1]) - data.sWidth//2, max(data.rect[0][1], data.rect[1][1])+data.sWidth//2+1):
                for j in range(min(data.rect[0][0], data.rect[1][0])- data.sWidth//2, max(data.rect[0][0], data.rect[1][0])+ data.sWidth//2+1):
                    data.board[i][j] = data.color
        #only looks smaller cuz we had to do an int divide since its possible for your cursor to be in a decimal location
    #This function creates it with the mind that our line width is gonna be created from left to right
    elif data.functions[data.function] == "line":
        data.line[1] = (x,y)
        data.line[2] = (y-data.line[0][1])/(x-data.line[0][0])
        wSlope = -1/data.line[2] #parametrize this to calculate final point
        #print(data.line[2])
        #data.xComp = 1
        #data.yComp = -1/data.line[2]
        canvas.create_line(data.line[0],data.line[1], fill = color, width = data.sWidth)
        #Makes the midpoints the values
        a = data.line[0][0] + 0.5
        b = data.line[0][1] + 0.5
        data.line[0] = (a,b)
        a = data.line[1][0] + 0.5
        b = data.line[1][1] + 0.5
        data.line[1] = (a,b)
        if abs(wSlope) > 1 and data.line[0][0] > data.line[1][0]:
            #Makes sure leftside one is the data.rect[0]
            temp = data.line[1]
            data.line[1] = data.line[0]
            data.line[0] = temp
        elif abs(wSlope) < 1 and data.line[0][1] > data.line[1][1]:
            #Makes sure leftside one is the data.rect[0]
            temp = data.line[1]
            data.line[1] = data.line[0]
            data.line[0] = temp
        if abs(wSlope) < 1:
            yBase = data.line[0][1]
            smallDrawWidth(canvas, data, data.line[0][0], data.line[0][1], yBase)
        elif abs(wSlope) > 1:
            xBase = data.line[0][0]
            largeDrawWidth(canvas, data, data.line[0][0], data.line[0][1], xBase)
# Draw graphics normally with redrawAll
# Main difference: the data struct contains helpful information to assist drawing
# Also, the canvas will get cleared and this will be called again
# constantly by the event loop.
def redrawAll(canvas, data):
    color = rgbtoTk(data.color)
    white = rgbtoTk((255,255,255))
    #if data.functions[data.function] == "save":
    #    tkSimpleDialog.askstring(title, prompt [initialvalue])\
    if data.count == 0:
        #canvas.create_image(0,0, anchor = NW, image = data.title)
        data.count += 1

    if data.functions[data.function] == "erase" and data.pressed:
        erase(data)
        #canvas.create_oval(data.cursor[0]-10, data.cursor[1]-10, 
        #                   data.cursor[0]+10, data.cursor[1]+10)

        x1,y1 = data.cursor[0]-data.radius, data.cursor[1]-data.radius
        x2,y2 = data.cursor[0]+data.radius, data.cursor[1]+data.radius
        canvas.create_oval(x1,y1,x2,y2, fill=white, width = 0)

    elif data.functions[data.function] == "pen" and data.pressed:
        pen(data)
        x1,y1 = data.cursor[0]-data.radius/2, data.cursor[1]-data.radius/2
        x2,y2 = data.cursor[0]+data.radius/2, data.cursor[1]+data.radius/2
        canvas.create_oval(x1, y1, x2, y2, fill=color, width = 0)
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
    data.color = data.colorCode[color]
    data.temp = data.colorCode[color]
    
def changeFunction(function, data):
    data.function = function
    #print(data.function)
    #if data.functions[data.function] == "pen":
    #    data.color = data.temp
    
def drawButtons(canvas, data):
    data.colorButtons = [None]*len(data.colors)
    for num in range(len(data.colors)):
        button1 = Button(canvas, text = data.colors[num], anchor = CENTER)
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
    data.colorButtons[7].configure(command=lambda:changeColor(7,data))
    data.colorButtons[8].configure(command=lambda:getHelp())
    for num in range(len(data.colorButtons)):
        data.colorButtons[num].place(x=data.width-data.rectWidth,
                                     y=data.rectHeight*num)
    data.functionButtons = [None]*len(data.functions)
    for num in range(len(data.functions)):
        button1 = Button(canvas, text = data.functions[num],anchor = CENTER)
        button1.configure(width = data.rectWidth//8,height=data.functHeight//15,
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
    data.functionButtons[8].configure(command=lambda:clearBoard(canvas,data))
    data.functionButtons[9].configure(command=lambda:changeFunction(9,data))
    data.functionButtons[10].configure(command=lambda:changeFunction(10, data))
    data.functionButtons[11].configure(command=lambda:chooseColor(data))
    #data.functionButtons[11].configure(command=lambda:testEntry(data))
    for num in range(len(data.functionButtons)):
        data.functionButtons[num].place(x=data.width-2*data.rectWidth,
                                        y=data.functHeight*num)
        
                           
def timerFired(canvas, data): #Absolutely useless function 
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    #print(x,y)
    #data.cursor = (root.winfo_pointerx()-root.winfo_rootx(), 
    #               root.winfo_pointery()-root.winfo_rooty())
    #if data.functions[data.function] == "pen":
    #    pen(data)
    #if data.functions[data.function] == "erase":
    #    erase(data)
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
    def startShapeWrapper(canvas, data):
        #print("hi")
        initPoint(canvas, data)
        redrawAllWrapper(canvas, data)

    def drawShapeWrapper(canvas, data):
        drawShape(canvas, data)
        redrawAllWrapper(canvas, data)

    def makeShapeWrapper(canvas, data):
        makeShape(canvas, data)
        redrawAllWrapper(canvas, data)

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
    #frame = Frame(root, width = data.width, height = data.height)
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<ButtonRelease-1>", lambda event: 
                            mouseReleasedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind('<Motion>', lambda event: 
                            motionWrapper(event, canvas, data))
    canvas.bind('<Button-1>', lambda event: #Binding here causes none of the other functions to work. Trying canvas works but it may cause other erros
                            startShapeWrapper(canvas, data))
    canvas.bind('<B1-Motion>', lambda event:
                            drawShapeWrapper(canvas, data))
    canvas.bind('<ButtonRelease-1>', lambda event:
                            makeShapeWrapper(canvas, data))
    #frame.pack()
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

run(700, 700)
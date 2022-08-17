
from asyncio import events
from cgitb import text
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
#import numpy as np
import pickle
from turtle import onclick, position
from webbrowser import get

from cv2 import scaleAdd
import Datapoint as Dp
import ChildClass as CCD
import ChildCanvas as CCV
import Report
from PIL import ImageTk, Image, ImageDraw
import numpy as np
import cv2
import glob
from tkinter import colorchooser,filedialog
import os,sys
import win32print
import win32api
import tempfile
from tkinter.messagebox import showinfo
from win32api import GetSystemMetrics
#from screeninfo import get_monitors

#for m in get_monitors():
#    print(str(m))



PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "GUI Test.ui")

class GuiTestApp:
    def __init__(self, master=None):
        # build ui
        self.titleData = "untitle.pkl"
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.toplevel1.title("Silk Design Program - {}".format(self.titleData))
        width= self.toplevel1.winfo_screenwidth()
        height= self.toplevel1.winfo_screenheight()
        #setting tkinter window size
        self.toplevel1.geometry("%dx%d" % (width,height))
        
        self.scale = 8
        self.scale_int = 8
        
        #canvas Parameter
        self.canvas_width = 1200     
        self.canvas_height = 900

        #CanvasDraw
        self.canvas_draw_width = 50*self.scale
        self.canvas_draw_height = 50*self.scale

        self.canvasMini_height =10
        self.canvasMini_width =10

        
        self.frame1 = ttk.Frame(self.toplevel1)
        
        self.canvasMain = tk.Canvas(self.frame1, bd=0)
        #self.canvasMain2 = tk.Canvas(self.canvasMain)
        #self.toplevel1.attributes("-fullscreen", True)

        
        
        
        self.canvasMain.configure(background='#FFFFFF', borderwidth='0', closeenough='1', confine='true')
        self.canvasMain.configure( highlightcolor='#100000', insertwidth='0')
        self.canvasMain.configure()
        self.canvasMain.grid(column='0', row='0')
        self.canvasMain.grid(row='0', column='0')
        
   
    
        #Scroll bar 
        frame=Frame(self.canvasMain)
        frame.pack(expand = True, fill=BOTH)

        #self.canvasMain = Canvas(frame,bg='white',height=self.canvas_draw_height,width=self.canvas_draw_width,
        self.canvasMain = Canvas(frame,bg='white',height=self.canvas_height,width=self.canvas_width,
                    scrollregion=(0,0,50*self.scale,50*self.scale))
        
        
        hbar = Scrollbar(frame,orient = HORIZONTAL)
        hbar.pack(side = BOTTOM, fill = X)
        hbar.config(command = self.canvasMain.xview)

        vbar = Scrollbar(frame,orient = VERTICAL)
        vbar.pack(side = RIGHT, fill = Y)
        vbar.config(command = self.canvasMain.yview)

        
        self.canvasMain.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvasMain.pack(side=LEFT, expand = True, fill = BOTH)
        


        self.frame1.configure()
        self.frame1.grid(column='0', padx='10', row='0', sticky='ne')
        self.frame3 = ttk.Frame(self.toplevel1)
        self.frame4 = ttk.Frame(self.frame3)
        self.canvasMini = tk.Canvas(self.frame4,bd=0)
        self.canvasMini.configure(background='#DDDDDD', height='100', width='100')
        self.canvasMini.grid(column='0', row='0')
        
        self.listbox1 = tk.Listbox(self.frame4)
        self.listbox1.configure(exportselection='true', height='5', width='20')
        self.listbox1.grid(column='0', row='1')
        self.scrollbar = tk.Scrollbar(self.frame4, orient="vertical",command=self.listbox1.yview)
        self.scrollbar.grid(column='1', row='1', ipady='20',sticky=N+S)
        self.listbox1.config(yscrollcommand=self.scrollbar.set)

        #ฟังก์ชั่นภาพย่อย
        self.LoadMini = ttk.Button(self.frame4)
        self.LoadMini.configure(text='โหลด', width='5')
        self.LoadMini.grid(column='0', ipadx='5', padx='5', row='2', sticky='nw')
        self.LoadMini.rowconfigure('2', minsize='0')
        self.CancelMini = ttk.Button(self.frame4)
        self.CancelMini.configure(text='ยกเลิก', width='7')
        self.CancelMini.grid(column='0', padx='5', row='2', sticky='ne')
        self.CancelMini.rowconfigure('2', minsize='0')
        self.frame4.configure(height='100', width='100')
        self.frame4.grid(column='0', row='5', sticky='n')
        self.DeleteMini = ttk.Button(self.frame4)
        self.DeleteMini.configure(text='ลบ', width='5')
        self.DeleteMini.grid(column='1', ipadx='5', padx='5', row='2', sticky='nw')
        self.DeleteMini.rowconfigure('2', minsize='0')
        
        self.frame6 = ttk.Frame(self.frame3)
        self.labelframe1 = ttk.Labelframe(self.frame6)
        self.New = ttk.Button(self.labelframe1)
        self.New.configure(text='สร้างใหม่', width='15',command=self.create_windowsBox)
        self.New.pack(side='top')
        self.button4 = ttk.Button(self.labelframe1)
        self.button4.configure(text='โหลดข้อมูลเดิม', width='15',command=self.openData)
        self.button4.pack(side='top')
        self.Save = ttk.Button(self.labelframe1)
        self.Save.configure(text='บันทึก', width='15',command=self.saveData)
        self.Save.pack(side='top')
        self.SaveAs = ttk.Button(self.labelframe1)
        self.SaveAs.configure(text='บันทึกเป็น', width='15',command=self.saveasData)
        self.SaveAs.pack(side='top')
        self.createTem = ttk.Button(self.labelframe1)
        self.createTem.configure(text='สร้างรูปย่อย', width='15')
        self.createTem.pack(side='top')
        self.colorSelect = ttk.Button(self.labelframe1)
        self.colorSelect.configure(text='เลือกสี', width='15')
        self.colorSelect.pack(side='top')
        self.printReport = ttk.Button(self.labelframe1)
        self.printReport.configure(text='ส่งออกเป็น PDF', width='15',command=self.reportExample)
        self.printReport.pack(side='top')
        self.printReport1 = ttk.Button(self.labelframe1)
        self.printReport1.configure(text='Print', width='15',command=self.locprinter)
        self.printReport1.pack(side='top')
        
        
        self.zoomin1 = ttk.Button(self.labelframe1)
        self.zoomin1.configure(text='zoom in', width='15',command=self.zoomin)
        self.zoomin1.pack(side='left')
        self.zoomout2 = ttk.Button(self.labelframe1)
        self.zoomout2.configure(text='zoom out', width='15',command=self.zoomout)
        self.zoomout2.pack(side='right')

        print("Width =", GetSystemMetrics(0))
        print("Height =", GetSystemMetrics(1))


        self.labelframe1.configure(height='100', labelanchor='nw', padding='20', relief='groove')
        self.labelframe1.configure(takefocus=True, text='เครื่องมือ', width='100')
        self.labelframe1.grid(column='0', columnspan='20', row='0', rowspan='20', sticky='e')
        self.frame6.configure(height='100', width='100')
        self.frame6.grid(column='0', row='6')
        self.frame3.configure(height='400', width='100')
        self.frame3.grid(column='1', row='0', sticky='ne')

        self.toplevel1.configure()
        self.toplevel1.resizable(True, True)
        #Tk.attributes("-fullscreen", False)
        # Main widget
        self.mainwindow = self.toplevel1
        
        # bind function
        self.canvasMain.bind( "<ButtonPress-1>", self.paintButton_Press)
        self.canvasMain.bind( "<B1-Motion>", self.paintButton_Move)
        # self.canvasMain.bind("<ButtonPress-1>", self.on_button_press)
        # self.canvasMain.bind("<B1-Motion>", self.on_move_press)
        self.canvasMain.bind("<ButtonRelease-1>", self.on_button_release)
        self.listbox1.bind("<<ListboxSelect>>", self.selectitem)
        self.canvasMain.bind("<Motion>", self.move_window)
        self.toplevel1.bind("<F11>", lambda event: self.toplevel1.attributes("-fullscreen",not self.toplevel1.attributes("-fullscreen")))
        self.toplevel1.bind("<Escape>", lambda event: self.toplevel1.attributes("-fullscreen", False))

        #bind colorbutton
        self.colorSelect['command'] = self.selectcolor
        self.colorSelect.pack()

        self.LoadMini['command'] = self.overLayImage
        self.CancelMini['command'] = self.cancleMode
        self.createTem['command'] = lambda: self.changemode(2)
        self.createTem.pack()

        

        ### image parameter
        self.moveImage = None
        self.FullImageBackground = None
        self.Fullthumnal = None
        ## image array 
        self.ImageBackground = None
        self.thumnal = None


         # general parameter
        self.GdataPointObj = Dp.Datapoint()
        self.currentindexX = ""
        self.currentindexY = ""
        self.changemode(mode=1)

        #parameter rectangle draw
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.x = self.y = 0

        self.line_distance = 1
       
        ######## call init grid
        self.drawgrid()
        #### reloadListthermail image
        self.reloadListImage()
        
    ################# This function for create sub Windows
    def cancleMode(self):
        self.canvasMain.delete("all")
        self.drawgrid()
        self.paintwithDataPoint()
        self.changemode(1)


    def create_windowsBox(self):
        self.kid = CCD.ChildClass(self)

        
    def move_window(self,event):
        event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))
        if self.mode == 3:
            cx, cy = event2canvas(event, self.canvasMain)
            x,y = (int(cx),int(cy))
            self.window_data = self.thumnal
            self.bg_img = self.ImageBackground.copy()
            ### find Current Index
            indexx = (x//10)*10
            indexy = (y//10)*10
            print(indexx,indexy)
            print(self.bg_img.shape[0])
            if indexx+self.thumnal.shape[1] <= self.bg_img.shape[1] and indexy+self.thumnal.shape[0] <= self.bg_img.shape[0]:
                self.bg_img[indexy:indexy+self.thumnal.shape[0],indexx:indexx+self.thumnal.shape[1]] = self.window_data
                self.img = ImageTk.PhotoImage(Image.fromarray(self.bg_img))
                self.canvasMain.create_image(0, 0,image=self.img,anchor="nw")
                # self.ImageBackground = ImageBackground
                print("xx")
    ########### Main Function 
    def convertColor(self,colorCode):
        return (int(colorCode, 16))

    def regenImageWithData(self):
        self.ImageBackground = np.ones((self.canvas_draw_height,self.canvas_draw_width,3),dtype=np.uint8)*255
        for indexPoint,colorconvert in enumerate(self.GdataPointObj.colorpoint):
            color1 = self.convertColor(colorconvert[1:3])
            color2 = self.convertColor(colorconvert[3:5])
            color3 = self.convertColor(colorconvert[5:])
            x,y = self.GdataPointObj.datapoint[indexPoint]
            x,y = int(x),int(y)
            self.ImageBackground[y:y+10,x:x+10,0] = color1
            self.ImageBackground[y:y+10,x:x+10,1] = color2
            self.ImageBackground[y:y+10,x:x+10,2] = color3

        color = (0, 0, 0)
        thickness = 1

        #draw grid
        # vertical lines at an interval of "line_distance" pixel
        for x in range(0,self.canvas_draw_height,self.line_distance):
            self.ImageBackground = cv2.line(self.ImageBackground,(x, 0), ( x, self.canvas_draw_height), color, thickness)
        # horizontal lines at an interval of "line_distance" pixel
        for y in range(0,self.canvas_draw_width,self.line_distance):
            self.ImageBackground = cv2.line(self.ImageBackground,(0, y), (self.canvas_draw_width, y), color, thickness)

    def regenImageThumnal(self):
        color = (0, 0, 0)
        thickness = 1
        #draw grid
        # vertical lines at an interval of "line_distance" pixel
        for x in range(0,self.thumnal.shape[1],self.line_distance):
            self.thumnal = cv2.line(self.thumnal,(x, 0), ( x,self.thumnal.shape[0]), color, thickness)
        # horizontal lines at an interval of "line_distance" pixel
        for y in range(0,self.thumnal.shape[0],self.line_distance):
            self.thumnal = cv2.line(self.thumnal,(0, y), (self.thumnal.shape[1], y), color, thickness)

        self.thumnal = cv2.rectangle(self.thumnal,(0,0),(self.thumnal.shape[1],self.thumnal.shape[0]),\
            (255,0,0),2)

    def overLayImage(self):
        self.regenImageWithData()
        self.regenImageThumnal()
        # Here is where the mouse coordinates should be injected to move the window over the background image
        self.window_data = self.thumnal
        self.bg_img = self.ImageBackground.copy() 
        # Here is where the mouse coordinates should be injected to move the window over the background image
        x,y = (0,0)
        self.bg_img[y:y+self.window_data.shape[0],x:x+self.window_data.shape[1]] = self.window_data
        self.img = ImageTk.PhotoImage(Image.fromarray(self.bg_img))
        ### disable All button

    
        self.changemode(mode=3)


        self.canvasMain.update()

    def drawgrid(self):
        #self.canvasMain.config(width=self.canvas_draw_width, height=self.canvas_draw_width)

        # vertical lines at an interval of "line_distance" pixel
        for x in range(0,int(self.canvas_draw_width),int(self.line_distance*self.scale)):
            if x%(5*self.scale) == 0:
               self.canvasMain.create_line(x, 0, x, int(self.canvas_draw_width), fill="black")
            else: 
                self.canvasMain.create_line(x, 0, x, int(self.canvas_draw_width), fill="gray")
        # horizontal lines at an interval of "line_distance" pixel
        for y in range(0,int(self.canvas_draw_height),int(self.line_distance*self.scale)):
            if y%(5*self.scale) == 0:
               self.canvasMain.create_line(0, y, int(self.canvas_draw_height), y, fill="black")
            else: 
                self.canvasMain.create_line(0, y, int(self.canvas_draw_height), y, fill="gray")
        self.canvasMain.update()
    def selectcolor(self):
        my_clolor = colorchooser.askcolor()
        #    dataPointObj.currentColor = my_clolor[1]
        #print(my_clolor)
        self.GdataPointObj.currentColor = my_clolor[1]

    def changemode(self,mode=1):  
        self.mode= mode
        if self.mode == 3:
            self.button4['state'] = tk.DISABLED
            self.Save['state'] = tk.DISABLED
            self.createTem['state'] = tk.DISABLED
            self.colorSelect['state'] = tk.DISABLED
            self.New['state'] = tk.DISABLED
        elif self.mode == 2:
            self.button4['state'] = tk.DISABLED
            self.Save['state'] = tk.DISABLED
            self.createTem['state'] = tk.DISABLED
            self.colorSelect['state'] = tk.DISABLED
            self.New['state'] = tk.DISABLED
            self.LoadMini['state'] = tk.DISABLED
            self.CancelMini['state'] = tk.DISABLED
        elif self.mode == 1:
            self.button4['state'] = tk.NORMAL
            self.Save['state'] = tk.NORMAL
            self.createTem['state'] = tk.NORMAL
            self.colorSelect['state'] = tk.NORMAL
            self.New['state'] = tk.NORMAL
            self.LoadMini['state'] = tk.NORMAL
            self.CancelMini['state'] = tk.NORMAL

    def saveMenu_click(self):
        self.saveData(self.GdataPointObj)

    ### general function 
    def showinfo(self, title, message):
        self.title("xxxx")

    def saveasData(self): 
        data = [('pkl', '*.pkl')]
        filesave = filedialog.asksaveasfile(filetypes=data,defaultextension='pkl',initialfile ='untitle')
        print(filesave)
        if (filesave != None): 
            self.GdataPointObj.setfilename(filesave.name)
            with open(filesave.name, 'wb') as output:
                pickle.dump(self.GdataPointObj, output, pickle.HIGHEST_PROTOCOL)
            
            (filename, ext) = os.path.splitext(os.path.basename(self.GdataPointObj.getfilename()))
            self.toplevel1.title("Skill Design Program - {}.pkl".format(filename))

            filesave.close()

    def saveData(self):
        if self.GdataPointObj.getfilename() != "":
                with open(self.GdataPointObj.getfilename(), 'wb') as output:
                    pickle.dump(self.GdataPointObj, output, pickle.HIGHEST_PROTOCOL)

                (filename, ext) = os.path.splitext(os.path.basename(self.GdataPointObj.getfilename()))
                self.toplevel1.title("Skill Design Program - {}.pkl".format(filename))
        else:
                self.saveasData()

    def openData(self):
        data = [('pkl', '*.pkl')]
        fileopen = filedialog.askopenfile(filetypes=data,defaultextension='pkl')
        print(fileopen.name)

        if (fileopen != None): 
            with open(fileopen.name, 'rb') as input:
                dataPointObj = pickle.load(input)
                print(dataPointObj.datapoint)  
                print(dataPointObj.colorpoint) 
                # master.title( "Painting using Ovals" )
                ## call reprint dataporint 
                self.GdataPointObj=dataPointObj
                print(self.GdataPointObj.datapoint)
                fileopen.close()
                #list
                #numpy libery
                self.canvasMain.delete("all")
                self.canvas_draw_height = self.GdataPointObj.height
                self.canvas_draw_width = self.GdataPointObj.width

                self.drawgrid()
                self.paintwithDataPoint()
                (filename, ext) = os.path.splitext(os.path.basename(fileopen.name))
                self.toplevel1.title("Skill Design Program - {}.pkl".format(filename))

    def newsheet(self):
        self.paintwithDataPoint(fixcolor=True)
        self.GdataPointObj = Dp.Datapoint()
        self.GdataPointObj.height = self.canvas_draw_height
        self.GdataPointObj.width = self.canvas_draw_width

    ## print datapoint
    def paintwithDataPoint(self,fixcolor=False):
        ratio = self.line_distance
        for indexpoint,datapointindex in enumerate(self.GdataPointObj.datapoint):    
            indexx=datapointindex[0]
            indexy=datapointindex[1]
            colorpoint = self.GdataPointObj.colorpoint[indexpoint]
            if fixcolor:
                colorpoint = "#FFFFFF" 
            #print("scale",self.scale)
           
        #    myrectangle = self.canvasMain.create_rectangle(1079.0,1081.0, 1100.0+(ratio*self.scale), 1100.0+(ratio*self.scale), fill='black')
            myrectangle = self.canvasMain.create_rectangle((indexx*self.scale), indexy*self.scale, indexx*self.scale+(ratio*self.scale),indexy*self.scale+(ratio*self.scale), fill='black')
            self.canvasMain.itemconfig(myrectangle, fill=colorpoint)


    def paintwithDataPoint2(self,fixcolor=False):
        ratio = 10
        for indexpoint,datapointindex in enumerate(self.GdataPointObj.datapoint): 
            (indexx)=datapointindex[0]
            (indexy)=datapointindex[1]
            colorpoint = self.GdataPointObj.colorpoint[indexpoint]
            if fixcolor:
                colorpoint = "#FFFFFF"
           #print("scale",self.scale)
        #    myrectangle = self.canvasMain.create_rectangle(1079.0,1081.0, 1100.0+(ratio*self.scale), 1100.0+(ratio*self.scale), fill='black')
            if self.scale ==1 :
                indexx//2
                indexy//2
                #print("Scale6666",self.scale)
            myrectangle = self.canvasMain.create_rectangle(indexx//2, indexy//2, indexx//2+(ratio*self.scale),indexy//2+(ratio*self.scale), fill='black')
            self.canvasMain.itemconfig(myrectangle, fill=colorpoint)


    def clearCanvas(self,start=(0,0),width=30,height=50):
        for x in range(start[0],start[0]+width,self.line_distance):
            for y in range(start[1],start[1]+height,self.line_distance):
                if [x,y] in self.GdataPointObj.datapoint:
                    ## 
                    indexofList = self.GdataPointObj.datapoint.index([x,y])
                    del self.GdataPointObj.datapoint[indexofList]
                    del self.GdataPointObj.colorpoint[indexofList]
                myrectangle = self.canvasMain.create_rectangle(x, y, x+10, y+10, fill='red')
                self.canvasMain.itemconfig(myrectangle, fill='white')

    def paintButton_Move(self,event):

        ## for draw mega pixel
        ratio = self.line_distance*self.scale
        
        x = self.canvasMain.canvasx(event.x)
        y = self.canvasMain.canvasy(event.y)
        indexx = (x//ratio)*ratio
        indexy = (y//ratio)*ratio
        if x >= self.canvas_draw_width-1:
            indexx = (((self.canvas_draw_width-1))*ratio)*self.scale 
        if y >= self.canvas_draw_height-1:
            indexy = (((self.canvas_draw_height-1)//ratio)*ratio)*self.scale 
            
        
        if self.mode == 1:
            ## for draw mega pixel
            current_color = self.GdataPointObj.currentColor
            #print(event.x,event.y)
            #print("curcer {},{} index {},{} current {},{}".format(x,y,indexx,indexy,self.currentindexX,self.currentindexY))


            dataPoint = self.GdataPointObj.datapoint
            if [indexx,indexy] in dataPoint:
                #print( indexx,indexy)         ### It filled
                ### filled white color and remove indexx, indexy
                if (str(event.type) == "Motion" and\
                    (self.currentindexX != indexx or self.currentindexY != indexy)):
                    
                    indexofList = dataPoint.index([indexx,indexy])
                    del self.GdataPointObj.datapoint[indexofList]
                    del self.GdataPointObj.colorpoint[indexofList]

                    myrectangle = self.canvasMain.create_rectangle(indexx, indexy, indexx+10, indexy+10, fill='black')
                    self.canvasMain.itemconfig(myrectangle, fill='white')
            else:
                if str(event.type) == "Motion" and (self.currentindexX != indexx or self.currentindexY != indexy):
                    self.GdataPointObj.datapoint +=[[indexx,indexy]] ## new filled
                    self.GdataPointObj.colorpoint+=[self.GdataPointObj.currentColor]
                    myrectangle = self.canvasMain.create_rectangle(indexx, indexy, indexx+10, indexy+10, fill='black')
                    self.canvasMain.itemconfig(myrectangle, fill=current_color)
            #print(self.GdataPointObj.datapoint)

        elif self.mode ==2: # draw rectangle mode
            
            if x > self.canvas_draw_width:
                indexx = (self.canvas_draw_width//10)*10
            if y > self.canvas_draw_height:
                indexy = (self.canvas_draw_height//10)*10


            curX = self.canvasMain.canvasx(indexx)
            curY = self.canvasMain.canvasy(indexy)
            w, h = self.canvasMain.winfo_width(), self.canvasMain.winfo_height()
            # expand rectangle as you drag the mouse
            self.canvasMain.coords(self.rect, self.start_x, self.start_y, curX, curY) 
        self.currentindexX = indexx
        self.currentindexY = indexy

    def paintButton_Press(self,event):
        ## for draw mega pixel
        
        ratio = self.line_distance*self.scale
        
        x = self.canvasMain.canvasx(event.x)
        y = self.canvasMain.canvasy(event.y)

        #print("canvaspoint1 = {},{}".format(self.canvasMain.canvasx(x),self.canvasMain.canvasy(y)))

        indexx = (x//ratio)*ratio
        indexy = (y//ratio)*ratio
        if x >= self.canvas_draw_width-1:
            indexx = (((self.canvas_draw_width-1))*ratio)*self.scale 
        if y >= self.canvas_draw_height-1:
            indexy = (((self.canvas_draw_height-1)//ratio)*ratio)*self.scale 
            
        if self.mode == 1:
            current_color = self.GdataPointObj.currentColor
         
           # print("curcer {},{} index {},{} current {},{}".format(x,y,indexx,indexy,self.currentindexX,self.currentindexY))


            dataPoint = self.GdataPointObj.datapoint
            indexx_s1,indexy_s1 = indexx//self.scale,indexy//self.scale
            if [indexx_s1,indexy_s1] in dataPoint:
                #print( indexx_s1,indexy_s1)         ### It filled
                ### filled white color and remove indexx, indexy

                if (str(event.type) == "4"): #Button Press
                    indexofList = dataPoint.index([indexx_s1,indexy_s1])
                    del self.GdataPointObj.datapoint[indexofList]
                    del self.GdataPointObj.colorpoint[indexofList]

                    myrectangle = self.canvasMain.create_rectangle(indexx,indexy, indexx+(ratio),indexy+(ratio), fill='black')
                    self.canvasMain.itemconfig(myrectangle, fill='white')
            else:
                if str(event.type) == "4":
                    self.GdataPointObj.datapoint +=[[indexx_s1,indexy_s1]] ## new filled
                    self.GdataPointObj.colorpoint+=[self.GdataPointObj.currentColor]
                    myrectangle = self.canvasMain.create_rectangle(indexx,indexy, indexx+(ratio),indexy+(ratio), fill='black')
                    self.canvasMain.itemconfig(myrectangle, fill=current_color)

            #print(self.GdataPointObj.datapoint)
            
        elif self.mode == 2: # draw rec mode
            self.start_x = self.canvasMain.canvasx(indexx)+2
            self.start_y = self.canvasMain.canvasy(indexy)+2

            # create rectangle if not yet exist
            if not self.rect:
                self.rect = self.canvasMain.create_rectangle(self.x, self.y, 0, 0, outline='red',width=2)
        elif self.mode == 3:
            #### replace data to mainCanvas
            indexx = (x//ratio)*ratio
            indexy = (y//ratio)*ratio
            print("Helloooo")
            self.clearCanvas(start=(indexx,indexy),width=self.MiniGDataPoint.width,height=self.MiniGDataPoint.height)
            array_temp = np.array(self.MiniGDataPoint.datapoint)
            array_temp[:,:] =array_temp[:,:] + np.array([indexx,indexy])
            array_temp = array_temp.astype(np.int)
            miniDatapoint = array_temp.tolist()
            self.GdataPointObj.datapoint += miniDatapoint
            self.GdataPointObj.colorpoint += self.MiniGDataPoint.colorpoint
            
            
            self.drawgrid()
            self.paintwithDataPoint()
            self.changemode(mode=1)
            
        self.currentindexX = indexx
        self.currentindexY = indexy
            
    def on_button_release(self,event):
        if self.mode == 2:
            self.changemode(mode=1)

            self.canvasMain.coords(self.rect, 0, 0, 0, 0) 

            self.kid_canvas = CCV.ChildCanvas(self)

            startX = min(self.start_x//self.scale,self.currentindexX//self.scale)
            startY = min(self.start_y//self.scale,self.currentindexY//self.scale)
            endX = max(self.start_x//self.scale,self.currentindexX//self.scale)
            endY = max(self.start_y//self.scale,self.currentindexY//self.scale)
            tempData = []
            tempColor = []
            for indexPoint,(x,y) in enumerate(self.GdataPointObj.datapoint):
                if  x >= startX and x < endX and y>=startY and y<endY:
                    tempData += [[x-startX,y-startY]]         ## with Reindexing
                    tempColor += [self.GdataPointObj.colorpoint[indexPoint]]
            dwidth = int(endX - startX)
            dheight  = int(endY - startY)
        #   print(dwidth,dheight)
            self.kid_canvas.canvas_width = dwidth
            self.kid_canvas.canvas_height = dheight
            self.canvasMini_width = dwidth
            self.canvasMini_height = dheight
           # print(self.kid_canvas.scale)
            self.kid_canvas.canvasDrawGrid(tempData,tempColor)
            self.kid_canvas.paintDataPoint()
            



        # ------------------------------ หน้าต่างแสดงตัวอย่างภาพย่อยที่บันทึกแล้ว -------------------------------------
    def redrawCanvasMini(self):
        # self.canvasMini.config(width=100, height=100)
        # self.canvasMini.config(height=self.canvasMini_height,width=self.canvasMini_width)
        #print(self.Fullthumnal.width())
        #print(self.Fullthumnal.height())
        self.canvasMini.configure(background='#FFFFFF', height=self.Fullthumnal.height()*self.scale, width=self.Fullthumnal.width()*self.scale)
        self.canvasMini.create_image(0,0, anchor=NW, image=self.Fullthumnal)     

        # vertical lines at an interval of "line_distance" pixel
        for x in range(0,self.Fullthumnal.width()*self.scale,self.line_distance*self.scale):
            if x%(5*self.scale) == 0:
                self.canvasMini.create_line(x, 0, x, self.Fullthumnal.height()*self.scale, fill="black")
            else: 
                self.canvasMini.create_line(x, 0, x, self.Fullthumnal.height()*self.scale, fill="gray")

        for y in range(0,self.Fullthumnal.height()*self.scale,int(self.line_distance*self.scale)):
            if y%(5*self.scale) == 0:
               self.canvasMini.create_line(0, y, self.Fullthumnal.width()*self.scale, y, fill="black")
            else: 
                self.canvasMini.create_line(0, y, self.Fullthumnal.width()*self.scale, y, fill="gray")

   






    def reloadImageTemp(self,fileData):
        with open("./ImageMini/{}.pk".format(fileData), 'rb') as input:
            self.thumnal = pickle.load(input)
            #print(self.thumnal)
            img = ImageTk.PhotoImage(Image.fromarray(self.thumnal))
            self.Fullthumnal = img
        
        with open("./ImageMini/R_{}.pk".format(fileData), 'rb') as input:
            self.MiniGDataPoint = pickle.load(input)

        self.redrawCanvasMini()
        






    def selectitem(self,event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            print(data)
            #### reload  Data Items
            self.reloadImageTemp(data)
        else:
            print("No Data")

    def reloadListImage(self):  
        if os.path.isdir("ImageMini"):
            listFile = os.listdir("ImageMini")
            listFile=glob.glob("ImageMini/Image*.pk")
                # clear listbox
            self.listbox1.delete(0, 'end')
            for filename in listFile:
                (file, ext) = os.path.splitext(os.path.basename(filename))
                self.listbox1.insert(END, file) 
        else:
            os.makedirs("ImageMini")
            with open("ImageMini/IndexImage.txt","w") as readIndex:
                readIndex.write("{:04d}".format(0))

    def reportExample(self):
        c = Report.Report(self.GdataPointObj,self.canvas_draw_height,self.canvas_draw_width)

   

 


    def installed_printer():
        printers = win32print.EnumPrinters(2)
        for p in printers:
            return(p)

    printerdef = ''

    def locprinter(self):
        pt = Toplevel()
    ##    pt.geometry("250x250")
        pt.title("choose printer")
        var1 = StringVar()
        LABEL = Label(pt, text="Select Printer",bg='goldenrod2',fg='black').pack(fill=X)
        PRCOMBO = ttk.Combobox(pt, width=35)
        print_list = []
        printers = list(win32print.EnumPrinters(2))
        for i in printers:
            print_list.append(i[2])
        print(print_list)
        # Put printers in combobox
        PRCOMBO['values'] = print_list
        defprinter= win32print.GetDefaultPrinter()
        print('Default selected Printer:',defprinter)
        PRCOMBO.set(defprinter)
        PRCOMBO.pack(padx=5,pady=5)
            
        def select():
            global printerdef
            printerdef = PRCOMBO.get()
            printcommand()
            pt.destroy()
        BUTTON = ttk.Button(pt, text="Print",width=30,command=select).pack(pady=10)

        LAB = Canvas(self.GdataPointObj,self.canvas_draw_height,self.canvas_draw_width)
        LAB.pack()

   

        def printcommand():
            printPic = LAB.pack_configure()
            print(printPic)
            print(printerdef)
        
            win32print.SetDefaultPrinter(printerdef)
            filename = tempfile.mktemp(".txt")
            open(filename,"w").write(str(printPic))
            # Bellow is call to print text from T2 textbox
            win32api.ShellExecute(
                0,
                "printto",
                filename,
                '"%s"' % win32print.GetDefaultPrinter(),
                ".",
                0
            )
            showinfo(title='Success',message='Print Successful',detail='Printing is done . thank You!')

    



    def zoomin(self):
         
        self.scale = self.scale*2 
        self.canvas_draw_width = self.canvas_draw_width*2
        self.canvas_draw_height = self.canvas_draw_height * 2
        # self.newsheet()
        self.canvasMain.delete("all")
        self.canvasMain.config(scrollregion=(0,0,50*self.scale,50*self.scale))
        self.drawgrid()
        self.paintwithDataPoint()
        
        print(self.scale)
        print(self.canvas_draw_width, self.canvas_draw_height)
       
        
    def zoomout(self):   
        self.scale = self.scale//2 
        self.canvas_draw_width = self.canvas_draw_width// 2
        self.canvas_draw_height = self.canvas_draw_height//2
        # self.newsheet()
        self.canvasMain.delete("all")
        self.canvasMain.config(scrollregion=(0,0,50*self.scale,50*self.scale))
        self.drawgrid()
        self.paintwithDataPoint() 

        print(self.scale) 
       
        print(self.GdataPointObj.datapoint)
        

        
    def run(self):
        self.mainwindow.mainloop()
    

if __name__ == '__main__':
    app = GuiTestApp()
      
    app.run()
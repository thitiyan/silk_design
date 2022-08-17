from reportlab.platypus.flowables import PageBreak
import Datapoint as DP
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,letter, inch,landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.graphics import shapes
from reportlab.graphics.charts.axes import XCategoryAxis,YValueAxis
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.axes import XValueAxis
from tkinter import colorchooser,filedialog

import numpy as np
class Report():
    
    def __init__(self,DataPoint,height,width):
 
        # self.reportName = "sample.pdf"
        # self.maincanvas = csPdf.Canvas(self.reportName,pagesize="A4")
        # self.maincanvas.line(0, 0, 500, 500)
        # self.maincanvas.drawString(150,200,"dbfbbf")
        # self.maincanvas.save()
        self.height = height//10
        self.width = width//10
        self.GDatapoint = DataPoint
        self.filename = ""
        self.maxX = 100
        self.maxY = 120
        self.saveasData()
        self.drawTableWithText()
        
    def convertColor(self,colorCode):
        color1 = int(colorCode[1:3],16)
        color2 = int(colorCode[3:5],16)
        color3 = int(colorCode[5:],16)
        return (color1,color2,color3)

    def drawBigTable(self):
        parts = []
        doc = SimpleDocTemplate("simple_table_grid.pdf", pagesize=A4,leftMargin=0.75*cm, rightMargin=0.75*cm,
            topMargin=1.5*cm,bottomMargin=2.5*cm)
        bigData = np.zeros((self.height,self.width))
        bigData =bigData.astype(str)
        bigData[:,:] = ""
        ListofDatapoint = self.GDatapoint.datapoint.copy()
        ListofColorPoint = self.GDatapoint.colorpoint.copy()
        for grid_y in range(0,(self.height//self.maxY)+1):
            for grid_x in range(0,(self.width//self.maxX)+1):
                startX = grid_x*self.maxX
                endX = (grid_x+1)*self.maxX
                startY = grid_y * self.maxY
                endY = (grid_y+1)*self.maxY
                if endX > self.width:
                    endX = self.width
                if endY > self.height:
                    endY = self.height


                subBigdata = bigData[startY:endY,startX:endX]  
                height,width = subBigdata.shape
                if height == 0 or width == 0:       ## continue if modulor has 0
                    continue
                subBigdata = subBigdata.tolist()
                t=Table(subBigdata,colWidths=width*[0.19*cm], rowHeights=height*[0.19*cm],hAlign='LEFT')
                t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),\
                ('VALIGN',(0,0),(0,-1),'TOP'),\
                ('ALIGN',(0,-1),(-1,-1),'CENTER'),\
                ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),\
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),\
                ('BOX', (0,0), (-1,-1), 0.25, colors.black)\
                ]))
                
                remainListDatapoint = ListofDatapoint.copy()
                remainListColorpoint = ListofColorPoint.copy()
                for index,color in zip(remainListDatapoint,remainListColorpoint) :
                    R,G,B = self.convertColor(color)
                    x,y = index
                    x,y = x//10,y//10
                    if x < endX and y < endY:
                        print(x-startX)
                        t.setStyle(TableStyle([('BACKGROUND', \
                            (x-startX, y-startY), (x-startX, y-startY), \
                                colors.Color(red=R/255.0,\
                                    green=G/255.0,\
                                        blue=B/255.0))]))    
                        if [x*10,y*10] in ListofDatapoint:  #remove if can set color
                            ## 
                            indexofList = ListofDatapoint.index([x*10,y*10])
                            del ListofDatapoint[indexofList]
                            del ListofColorPoint[indexofList]
                t.wrap(0, 0)
                parts.append(t)
                parts.append(Paragraph("This is a Heading"))

                parts.append(PageBreak())
        doc.build(parts)

    def getTableObject(self):
        parts = []
        bigData = np.zeros((self.height,self.width))
        bigData =bigData.astype(str)
        bigData[:,:] = ""
        ListofDatapoint = self.GDatapoint.datapoint.copy()
        ListofColorPoint = self.GDatapoint.colorpoint.copy()
        for grid_y in range(0,(self.height//self.maxY)+1):
            for grid_x in range(0,(self.width//self.maxX)+1):
                startX = grid_x*self.maxX
                endX = (grid_x+1)*self.maxX
                startY = grid_y * self.maxY
                endY = (grid_y+1)*self.maxY
                if endX > self.width:
                    endX = self.width
                if endY > self.height:
                    endY = self.height


                subBigdata = bigData[startY:endY,startX:endX]  
                height,width = subBigdata.shape
                if height == 0 or width == 0:       ## continue if modulor has 0
                    continue
                subBigdata = subBigdata.tolist()
                t=Table(subBigdata,colWidths=width*[0.19*cm], rowHeights=height*[0.19*cm],hAlign='LEFT')
                t.setStyle(TableStyle([('FONTSIZE', (0,0), (-1, -1), 5),\
                ('ALIGN',(0,0),(-1,-1),'LEFT'),\
                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),\
                ('INNERGRID', (0,0), (-1,-1), 0.1, colors.black),\
                ('BOX', (0,0), (-1,-1), 0.1, colors.black)\
                ]))
                
                remainListDatapoint = ListofDatapoint.copy()
                remainListColorpoint = ListofColorPoint.copy()
                for index,color in zip(remainListDatapoint,remainListColorpoint) :
                    R,G,B = self.convertColor(color)
                    x,y = index
                    x,y = x//10,y//10
                    if x < endX and y < endY:
                        print(x-startX)
                        t.setStyle(TableStyle([('BACKGROUND', \
                            (x-startX, y-startY), (x-startX, y-startY), \
                                colors.Color(red=R/255.0,\
                                    green=G/255.0,\
                                        blue=B/255.0))]))    
                        if [x*10,y*10] in ListofDatapoint:  #remove if can set color
                            ## 
                            indexofList = ListofDatapoint.index([x*10,y*10])
                            del ListofDatapoint[indexofList]
                            del ListofColorPoint[indexofList]
                t.wrap(0, 0)
                parts.append(t)
        return parts

    def drawTable(self):
        parts = []
        doc = SimpleDocTemplate("simple_table_grid.pdf", pagesize=A4,leftMargin=2.2*cm, rightMargin=2.2*cm,
            topMargin=1.5*cm,bottomMargin=2.5*cm)
        bigData = np.zeros((self.height,self.width))
        bigData =bigData.astype(str)
        bigData[:,:] = ""
        bigData = bigData.tolist()

        t=Table(bigData,self.width*[0.2*cm], self.height*[0.2*cm])
        t.setStyle(TableStyle([('ALIGN',(1,1),(-2,-2),'RIGHT'),
        ('VALIGN',(0,0),(0,-1),'TOP'),
        ('ALIGN',(0,-1),(-1,-1),'CENTER'),
        ('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black)
        ]))
        for index,color in zip(self.GDatapoint.datapoint,self.GDatapoint.colorpoint) :
            R,G,B = self.convertColor(color)
            x,y = index
            x,y = x//10,y//10
            t.setStyle(TableStyle([('BACKGROUND', \
                (x, y), (x, y), \
                    colors.Color(red=R/255.0,\
                        green=G/255.0,\
                            blue=B/255.0))]))

        t.wrap(0, 0)
        parts.append(t)
        parts.append(PageBreak())
        parts.append(t)
        doc.build(parts)

    def drawTableWithText(self):
        cc = canvas.Canvas(self.filename, pagesize=A4)
        width, height = A4
        totalh = 28*cm

        parts = self.getTableObject()
        for i in parts:

            print(totalh)
            A4width, A4height = A4
            print(A4width)
            # cc.setFontSize(6)
            # str_out = "{:02d}".format(number)
            # cc.drawString(1*cm+((number+1)*4.8), totalh, str_out)

            i.canv = cc
            #
            wight,height = i.wrap(0, 0)
            print(wight,height)
            #
            i.drawOn(cc, 1*cm, totalh-height)
            cc.showPage()
        cc.save()

    def saveasData(self): 
            data = [('pdf', '*.pdf')]
            filesave = filedialog.asksaveasfile(filetypes=data,defaultextension='pkl',initialfile ='untitle')
            print(filesave)
            if (filesave != None): 
                self.filename = filesave.name

if __name__ == "__main__":
    ireport = Report(DP.Datapoint(),800,1200)
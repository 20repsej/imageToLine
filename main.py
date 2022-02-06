from tkinter import Image
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.interpolate import make_interp_spline, BSpline


#img = Image.open("lapporten.jpeg").convert("L")
#print(img.size[1])
#img2 = Image.open("lapporten.jpeg")
#img3 = img2.crop((0, 0, 100, 100))
#img3.save("test2.jpeg")

#paletted = img.convert("L", palette=Image.ADAPTIVE)
#palette = paletted.getpalette()
#color_counts = sorted(paletted.getcolors(), reverse=True)
#print(color_counts)
#print(color_counts[0][1])

def dominantColor(img):
    paletted = img.convert("L", palette=Image.ADAPTIVE)
    colorCounts = sorted(paletted.getcolors(), reverse=True)
    return colorCounts[0][1]

def imageAreas(OrigImage, widthDiv, heightDiv, hPos):
    img = Image.open(OrigImage).convert("L")
    imgSquareHeight = int(img.height / heightDiv)
    imgSquareWidth = int(img.width / widthDiv)
    colorList = []

    for i in range(0, widthDiv):
        tempImg = img.copy()
        cropTempImg = tempImg.crop((imgSquareWidth*i, hPos*imgSquareHeight, imgSquareWidth*i + imgSquareWidth, hPos*imgSquareHeight + imgSquareHeight))
        domColor = dominantColor(cropTempImg)
        colorList.append(domColor)

    return colorList

#def colorListToCord(colorList):
#    colorWithCord = []
#    for i in colorList:
#        colorWithCord.append(())

def makeColorRow(OrigImage, widthDiv, heightDiv):
    colorListList = []
    for i in range(0, heightDiv):
        rowColorList = imageAreas(OrigImage, widthDiv, heightDiv, i)
        rowColorList = convert255ToPercentage(rowColorList)
        rowColorList = separeateLines(rowColorList, heightDiv-i)
        colorListList.append(rowColorList)
    
    return colorListList

def convert255ToPercentage(list):
    newList = []
    for i in list:
        newVal = 1/255 * i
        newList.append(newVal)
    
    return newList

def separeateLines(list, linePos):
    newList = []
    for i in list:
        newList.append(i + 0.7*linePos)
    return newList


def makeGraph(colorListList):
#    X = np.linspace(0, len(colorList), 10)
    X = []
    for i in range(0, len(colorListList[0])):
        X.append(i)
    xnew = np.linspace(0, 30, 3000)


    for colorList in colorListList:
        spl = make_interp_spline(X, colorList, k=3)
        y_smooth = spl(xnew)
        plt.plot(xnew, y_smooth, color='black')

    plt.show()

def main(image, widthDiv, heightDiv):
    colorListList = makeColorRow(image, widthDiv, heightDiv)
    makeGraph(colorListList)


main("linecoln.jpeg", 30, 50)




#X = np.linspace(0, 4 * np.pi, 50)
 
#Ya = np.sin(X)/2
#Yb = np.cos(X)
#Yc = np.log2(X)
#Yd = np.log10(X)
#print(Yb) 
#Yb[5] = 2
 
#plt.plot(X, Ya)
#plt.plot(X, Yb)
#plt.plot(X, Yc)
#plt.plot(X, Yd)
#plt.show()
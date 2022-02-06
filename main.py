from tkinter import Image
from turtle import color
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.interpolate import make_interp_spline, BSpline


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
        cropTempImg = tempImg.crop((imgSquareWidth*i, hPos*imgSquareHeight,
                                   imgSquareWidth*i + imgSquareWidth, hPos*imgSquareHeight + imgSquareHeight))
        domColor = dominantColor(cropTempImg)
        colorList.append(domColor)

    return colorList


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
        newVal = 1/255 * (255-i)
        newList.append(newVal)

    return newList


def separeateLines(list, linePos):
    newList = []
    for i in list:
        newList.append(i + 0.7*linePos)
    return newList


def makeGraph(colorListList, widthDiv):
    X = []
    for i in range(0, len(colorListList[0])):
        X.append(i)
    xnew = np.linspace(0, widthDiv, 3000)

    for colorList in colorListList:
        spl = make_interp_spline(X, colorList, k=3)
        y_smooth = spl(xnew)
        plt.plot(xnew, y_smooth, color='black')

    plt.show()


def main(image, widthDiv, heightDiv):
    colorListList = makeColorRow(image, widthDiv, heightDiv)
    makeGraph(colorListList, widthDiv)


numLines = 50
numWidth = 30
if(sys.argv[1] == None):
    print("Not enough arguments")
    exit()

if(sys.argv[1] == "help"):
    print("--------- HELP ---------")
    print("")
    print("Arg1: image file")
    print("Arg2: Width of squares (optional)")
    print("Arg3: Number of lines (optional)")
    print("")
    print("------------------------")
    exit()

if(len(sys.argv) >= 3):
    numWidth = sys.argv[2]

if(len(sys.argv) >= 4):
    numLines = sys.argv[3]

main(sys.argv[1], int(numWidth), int(numLines))

#from tkinter import Frame
from reportlab.pdfgen import canvas
from reportlab.lib import colors, styles
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Frame

# Create a PDF document with ReportLab
#pdf = SimpleDocTemplate("tuorial55.pdf", pagesize=letter)
pdf = canvas.Canvas("tuorial55.pdf")
# Get the pre-defined styles
s = styles.getSampleStyleSheet()

#### MATRIX CREATION
import random

# Size of the matrix
rows = 6
cols = 26

# Create an empty matrix
def matrix():
    matrix = [['' for j in range(cols)] for i in range(rows)]
    
    # Fill the matrix with random letters
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return matrix

# Create a list of flowables to be added to the document
flowables = []
flowables4 = []
flowables7 = []
flowables10 = []
flowables13 = []

# Add some text as a flowable
#text = "This is some example text."
#flowables.append(Paragraph(text, style=s["Normal"]))

# Create a table with some data
empty=['']
empty_table=Table(empty)
table_style=TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1),0),
                ('BACKGROUND', (0, -1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)])
alphabet= [['A', 'B', 'C', 'D', 'E','F', 'G', 'H', 'I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'],]

#CREATE SIDE BOXES
alphabet_part1 = ['A', 'B', 'C', 'D', 'E','F']
alphabet_part2 = ['G', 'H', 'I','J','K','L']
alphabet_part3 = ['M','N','O','P','Q','R']
alphabet_part4 = ['S','T','U','V','W','X','Y']

#CREATE SIDE BOX TABLES
alphabet_part1_table = Table(alphabet_part1,colWidths=[15,15])
flowables4.append(alphabet_part1_table)
#CREATE NEW FLOWABLE FOR VERTICAL ALPHABET PIECES and DISCOVER REST

alphabet_table=Table(alphabet,colWidths=[15,15])
alphabet_table.setStyle(table_style)
flowables.append(alphabet_table)

flowables.append(empty_table)

data = matrix()
for x in range(0, 4):
    data[x]=matrix()
    table = Table(data[x],colWidths=[15,15])
    table.setStyle(table_style)
    flowables.append(table)
    flowables.append(empty_table)


frame1=Frame(60,210,400,500,showBoundary=0)
frame1.addFromList(flowables,pdf)

frame2=Frame(35,580,10,90,showBoundary=1)
frame2.addFromList(flowables4,pdf)

pdf.save()

# Build the PDF document with the flowables
#pdf.build(flowables,flowables4)
#                #('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
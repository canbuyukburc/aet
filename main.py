from reportlab.pdfgen import canvas
from reportlab.lib import colors, styles
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Frame
from datetime import datetime
from io import BytesIO
from flask import Flask, render_template, request, send_file, make_response
import random

# Create an empty matrix
def matrix(cols,rows ):
    matrix = [['' for j in range(cols)] for i in range(rows)]
    
    # Fill the matrix with random letters
    for i in range(rows):
        for j in range(cols):
            matrix[i][j] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    return matrix
def generate_pdf (Exerceise_Name, Wing_Name,Extra_Notes):
    buffer = BytesIO()
    
    #pdf = canvas.Canvas("aet_v1.pdf")
    pdf = canvas.Canvas(buffer)
    # Get the pre-defined styles
    s = styles.getSampleStyleSheet()

    #### MATRIX CREATION
    # Size of the matrix
    #rows = 6
    #cols = 26
    # Create a list of flowables to be added to the document
    flowables = []
    flowables4 = []


    # Add some text as a flowable
    #text = "This is some example text."
    #flowables.append(Paragraph(text, style=s["Normal"]))

    # Create a table with some data
    empty=['']
    empty_table=Table(empty,colWidths=[15,15])
    table_style=TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1),0),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.white)])
    alphabet= ['A', 'B', 'C', 'D', 'E','F', 'G', 'H', 'I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    #CREATE SIDE BOXES

    alphabet_part1 = ['A', 'B', 'C', 'D', 'E','F']
    alphabet_part2 = ['G', 'H', 'I','J','K','L']
    alphabet_part3 = ['M','N','O','P','Q','R']
    alphabet_part4 = ['S','T','U','V','W','X','Y']

    flowables.append(empty_table)
    flowables.append(empty_table)
    data = matrix(26,6)
    for x in range(0, 4):
        data[x]=matrix(26,6)
        table = Table(data[x],colWidths=[15,15])
        table.setStyle(table_style)
        flowables.append(table)
        if x !=3:
            flowables.append(empty_table)

    #Single_line = data(26,1)
    Single_line_Table = Table(matrix(26,1),colWidths=[15,15])
    flowables.append(Single_line_Table)


    frame1=Frame(80,210,420,500,showBoundary=0)
    frame1.addFromList(flowables,pdf)

    #frame2=Frame(35,656,15,15,showBoundary=1)
    #frame3=Frame(35,641,15,15,showBoundary=1)
    #frame2.addFromList(flowables4,pdf)

    pdf.setFont('Helvetica-Bold', 11)
    # LEFT HEADER COLUMN
    Leftmargin = 80
    FirstGrBottomMargin =656
    for k in alphabet_part1:
        pdf.drawString(Leftmargin,FirstGrBottomMargin,k)
        FirstGrBottomMargin=FirstGrBottomMargin-15


    SecondGrBottomMargin =548    
    for k in alphabet_part2:
        pdf.drawString(Leftmargin,SecondGrBottomMargin,k)
        SecondGrBottomMargin=SecondGrBottomMargin-15
        
    ThirdGrBottomMargin = 441
    for k in alphabet_part3:
        pdf.drawString(Leftmargin,ThirdGrBottomMargin,k)
        ThirdGrBottomMargin=ThirdGrBottomMargin-15
        
    FourthGrBottomMargin = 330
    for k in alphabet_part4:
        pdf.drawString(Leftmargin,FourthGrBottomMargin,k)
        FourthGrBottomMargin=FourthGrBottomMargin-15
        

    # MID NUMBERS
    mid_string = "              0          1        2         3         4         5         6           7          8           9"
    pdf.drawString(80,567,mid_string)
    pdf.drawString(80,458,mid_string)
    pdf.drawString(80,351,mid_string)
    pdf.drawString(80,220,mid_string)

    #TOP HEADER ROW
    BottomMargin = 670
    LeftStart = 98
    for i in alphabet:
        pdf.drawString(LeftStart,BottomMargin,i)
        LeftStart=LeftStart+15

    #PLACE TITLE    
    pdf.setFont('Helvetica-Bold', 18)
    pdf.setFillColorRGB(1,0,0)
    pdf.drawString(250,690,"AET-100")

    #PLACE DCS Disclaimer
    pdf.setFont('Helvetica',11)
    Wing_String = f'Property of {Wing_Name}'
    pdf.drawString(68,708,Wing_String)

    #PLACE EXERCISE OR Virtual Squadron info
    Exercise_String = f'Exercise {Exerceise_Name}'
    pdf.drawString(250,190,Exercise_String)
    #PLACE VERSION DATA
    #version is day and hour DDHHMMLMM
    now = datetime.now()
    timeString = now.strftime("%d%H%M %Y") #/%m/%Y %H:%M:%S"
    pdf.setFont('Helvetica-Bold', 11)
    pdf.setFillColorRGB(0,0,0)
    version_string = f'Version : {timeString}'
    pdf.drawString(370,690,version_string)

    #
    uplx = 62
    uply = 720
    uprx = 500
    upry =uply
    dwnlx = uplx
    dwnly = 180
    dwnrx = uprx
    dwnry = dwnly

    pdf.line(uprx,upry,dwnrx,dwnry) #left
    pdf.line(uplx,uply,uprx,upry) #top
    pdf.line(uplx,uply,dwnlx,dwnly) #right
    pdf.line(dwnlx,dwnly,dwnrx,dwnry) #bottom
    
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    # Set the content type of the response to application/pdf
    response.headers.set('Content-Type', 'application/pdf')
    # Set the Content-Disposition header to attachment, which will prompt the user to download the file
    response.headers.set('Content-Disposition', 'attachment', filename='aet_v1.pdf')
    
    #return buffer.read()
    return response

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'], endpoint='generate_pdf')
def index():
    if request.method == 'POST':
        # Get the form data
        Exercise_Name = request.form['Exercise_Name']
        Wing_Name = request.form['Wing_Name']
        Extra_Notes = request.form['Extra_Notes']
        
        # Generate the PDF and return it as a response object
        return generate_pdf(Exercise_Name, Wing_Name, Extra_Notes)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
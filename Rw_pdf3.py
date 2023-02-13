from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm,inch,mm

from pdfrw import PdfReader

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib import utils
from datetime import datetime
import locale


from reportlab.lib import colors
from reportlab.lib.colors import Color, CMYKColor, getAllNamedColors, toColor, \
    HexColor

import qrcode



I=1

def creat_qrcode(fichier,data):
    global I
    img = qrcode.make(data)
    g='codes/' + fichier + str(I) + ".png"
    # img = qrcode.make_image(fill_color = 'red',back_color = 'white')
    img.save(g)
    I +=1
    return g

def add_image2(image_path,my_canvas,x=150,y=10,w=100,h=100,rot=False,ongle=45):
    img = utils.ImageReader(image_path)
    img_width, img_height = img.getSize()
    aspect = img_height / float(img_width)

    my_canvas.saveState()
    if rot:
        my_canvas.rotate(ongle)

    my_canvas.drawImage(image_path, x, y,
                        width=w, height=(h * aspect))
    my_canvas.restoreState()


def writeExistPDF(soket,existFile,destFile):
	"""
	from PyPDF2 import PdfFileWriter, PdfFileReader
	
	soket : type (io.BytesIO) write canvas --> reportlab.pdfgen
	existFile : path existe file pdf
	destFile : path existe file pdf
	"""
	#~ ====== Socket vers le nouveau PDF
	soket.seek(0)
	new_pdf = PdfFileReader(soket)
	
	#~ ====== fichier existant
	existing_pdf = PdfFileReader(open(existFile, "rb"))
	output = PdfFileWriter()
	
	#~ ====== Fusion New page et socket
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)
	
	#~ ====== Génération doc destination
	outputStream = open(destFile, "wb")
	output.write(outputStream)
	outputStream.close()
	
	






file_pdf="exist_pdf/Facture_10.pdf"

pdf = PdfReader(file_pdf)
w=pdf.pages[0].MediaBox[2]
h=pdf.pages[0].MediaBox[3]
#~ print("Taille :",)

#~ ====== Ecriture sur le socket t
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
#~ can.setFillColorRGB(1, 0, 0)
can.setFont("Times-Roman", 12)
can.translate(cm,cm)

can.setPageSize((w,h))

can.drawString(105, 530, "Brel ASSEH")

can.drawString(105, 512, "242 06 846 34 99")

can.drawString(105, 495, "brel.asseh@gmail.com")


can.setFont("Times-Roman", 15)
can.drawString(422, 535, "F_0000012456")

#~ date
can.drawString(385, 495, "10 décembre 2022")

pdfmetrics.registerFont(TTFont('helvetica', 'Helvetica.ttf'))
can.setFont("helvetica", 11)
can.setFillColorRGB(0, 0,0)


can.drawString(115, 400, "Autotorisation de transfansport  pour voyageur 2022")
can.drawString(60, 400, "01")
can.drawString(408, 400, "20 000")
can.drawString(458, 400, "20 000")

#~ can.drawString(250, 310, "0000000123456")
can.setFont("Times-Roman", 16)
can.drawString(450, 212, "20 000 XAF")

#~ can.setFont("Times-Roman", 22)

#~ can.drawString(438,394, "2023")


#~ =================== QR
da ="http//dgrp.cg/valid_atp/ixnnfkndkf1"
file = creat_qrcode("QRcode", da)
add_image2(file, can, x=70, y=30, w=90, h=90)
add_image2(file, can, x=90, y=50, w=90, h=90)

can.save() 

writeExistPDF(soket=packet,existFile=file_pdf,destFile="exist_pdf/destination.pdf")






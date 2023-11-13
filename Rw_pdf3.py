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

def creat_qrcode2(fichier,data,color=["black","white"]):
	global I
	if color:
		qr = qrcode.QRCode(version = 1,
			box_size = 10,
			border = 3)

		# Adding data to the instance 'qr'
		qr.add_data(data)
		qr.make(fit = True)
		img = qr.make_image(fill_color =color[0],
			back_color = color[1])
	else:
		img = qrcode.make(data)

	g='codes/' + fichier + str(I) + ".png"
	img.save(g)
	I +=1
	return g

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
	
	






file_pdf="exist_pdf/000001.pdf"

pdf = PdfReader(file_pdf)
w=pdf.pages[0].MediaBox[2]
h=pdf.pages[0].MediaBox[3]
#~ print("Taille :",)

#~ ====== Ecriture sur le socket t
packet = io.BytesIO()
can = canvas.Canvas(packet, pagesize=letter)
#~ can.setFillColorRGB(1, 0, 0)
pdfmetrics.registerFont(TTFont('hegelmotokoua', 'CenturyGothic.ttf'))
can.setFont("hegelmotokoua", 14)
can.translate(cm,cm)

can.setPageSize((w,h))

can.drawString(182, 426, "GARAGE DORDY")

can.drawString(125, 405, "175, Rue KITOKO, Plateau de 15 Ans Bvlle")

can.drawString(148, 380, "242067363636")

can.drawString(140, 362, "brel.asseh@gmail.com")

can.drawString(95, 336, "P2025110003038274")

can.drawString(108, 313, "CG-BZV-01-2019-B12-10047")

can.drawString(175, 289, "AG-XXXX-XXX")

can.drawString(135, 262, "A /MTACMM-DGTT-DTUR")

can.drawString(205, 230, "PETITE")

can.drawString(175, 211, "GARAGE AUTOMOBILE")

can.drawString(218, 183, "05 / 03 / 2023")

can.drawString(204, 150, "05 / 03 / 2023")


pdfmetrics.registerFont(TTFont('asseh', 'Helvetica.ttf'))
can.setFont("asseh", 13)

file = "codes\Signature.png"
add_image2(file, can, x=360, y=96, w=170, h=170)


can.drawString(364, 80, "Lionel MESSI")

# can.setFont("Times-Roman", 15)
# can.drawString(422, 535, "F_0000012456")

#~ date
# can.drawString(385, 495, "10 décembre 2022")

# pdfmetrics.registerFont(TTFont('helvetica', 'Helvetica.ttf'))
# can.setFont("helvetica", 11)
# can.setFillColorRGB(0, 0,0)


# can.drawString(115, 400, "Autotorisation de transfansport  pour voyageur 2022")
# can.drawString(60, 400, "01")
# can.drawString(408, 400, "20 000")
# can.drawString(458, 400, "20 000")

#~ can.drawString(250, 310, "0000000123456")
can.setFont("Times-Roman", 16)
# can.drawString(450, 212, "20 000 XAF")

#~ can.setFont("Times-Roman", 22)

#~ can.drawString(438,394, "2023")


#~ =================== QR
da ="http//dgrp.cg/valid_atp/ixnnfkndkf1"
file = creat_qrcode("QRcode", da)
add_image2(file, can, x=484, y=664, w=85, h=85)

file = creat_qrcode2("QRcode", da, color=["green","white"])
add_image2(file, can, x=24, y=36, w=50, h=50)

can.save() 

writeExistPDF(soket=packet,existFile=file_pdf,destFile="exist_pdf/destination.pdf")







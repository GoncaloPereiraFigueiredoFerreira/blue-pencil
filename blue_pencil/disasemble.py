from pdf2image import convert_from_path
from pypdf import PdfReader
import re

def latinCompability(text):
    text = re.sub(r"¸ *c","ç",text)
    text = re.sub(r"` *a","à",text)
    text = re.sub(r"´ *a","á",text)
    text = re.sub(r"´ *A","Á",text)
    text = re.sub(r"´ *E","É",text)
    text = re.sub(r"˜ *a","ã",text)
    text = re.sub(r"ˆ *a","â",text)
    text = re.sub(r"´ *e","é",text)
    text = re.sub(r"ˆ *e","ê",text)
    text = re.sub(r"´ *i","í",text)
    text = re.sub(r"´ *ı","í",text)
    text = re.sub(r"´ *o","ó",text)
    text = re.sub(r"˜ *o","õ",text)
    text = re.sub(r"´ *u","ú",text)
    return text


def pdf_to_text(pdf_path, text_path):
    reader = PdfReader(pdf_path)
    text = ""
    i=0
    res =[]
    for page in reader.pages:
        pageTxt = open(text_path+str(i)+".txt","w")
        res.append(text_path+str(i)+".txt")
        i+=1
        text = page.extract_text()
        text = latinCompability(text)
        pageTxt.write(text)
        pageTxt.close()
       
    return res

#Could have used pdftocairo
def pdf_to_image(pdf_path, image_path):
    # Convert the PDF to a list of PIL images
    images = convert_from_path(pdf_path)
    paths=[]
    # Loop through each image
    for i, image in enumerate(images):
        # Save the image
        image.save(image_path + str(i) + '.png')
        paths.append(image_path + str(i) + '.png')
    return paths
 

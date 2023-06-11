# Import required packages
import cv2
import pytesseract
import re

ents = {}

def blue_markerText(private,text,replace):
    global ents
    if replace:
        for i in private:
            if (i[2] in ents):
                if i[0] not in ents[i[2]]:ents[i[2]].append(i[0])
                index=ents[i[2]].index(i[0])
            else: 
                ents[i[2]]=[i[0]]
                index=0
            if (i[2]!="PER"):
                text=re.sub(re.escape(i[0]).replace("\ "," "),"#"+i[2]+str(index),text,count=1)
            else:
                match = re.search(r"([A-Z])\w+( ([A-Z])\w+)*",i[0])
                replace=""
                for x in range(len(match.groups())+1):
                    if x%2==1 and match.group(x)!=None: replace+=match.group(x)+". "
                replace=replace.removesuffix(" ")+"#"
                text=re.sub(re.escape(i[0]).replace("\ "," "),"#"+replace,text,count=1)

    else:
        for i in private:         
            censor=["*" for n in range(0,len(i[0]))]
            text=re.sub(re.escape(i[0]).replace("\ "," "),"".join(censor),text,count=1)
    return text



def blue_markerPDF(private,image,replace):

    # Mention the installed location of Tesseract-OCR in your system
    #pytesseract.pytesseract.tesseract_cmd = 'System_path_to_tesseract.exe'

    # Read image from which text needs to be extracted
    img = cv2.imread(image)

    # Preprocessing the image starts

    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    #Should be changed to configure by argument passing
    results = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT,config="-l Latin")
    
    for i in private: 
        match =re.escape(i[0]).replace("\ "," ")
        words =re.split(r"\s",match)

        boxes=[]
        for j in range(0, len(results["text"])):
            token=results["text"][j]
            if re.search(words[len(boxes)],token):
                boxes.append({"left":results["left"][j],"top":results["top"][j],"width":results["width"][j],"height":results["height"][j]})
            else:
                boxes = []
            if len(boxes)==len(words):
                break
        if boxes!=[]:
            w= 0
            x= boxes[0]["left"]
            y= boxes[0]["top"]
            h= boxes[0]["height"]
            for box in boxes[1:]:
                x = box["left"] if x > box["left"] else x
                y = box["top"]  if y > box["top"] else y
                w += box["width"] + 10
                h = box["height"] if h > box["height"] else h

            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0,0),-1)


    # show the output image
    cv2.imwrite(image,img)


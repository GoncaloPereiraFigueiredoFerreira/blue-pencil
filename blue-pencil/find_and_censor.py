# Import required packages
import cv2
import pytesseract
import re

def blue_marker(private,image,lang):

    # Mention the installed location of Tesseract-OCR in your system
    #pytesseract.pytesseract.tesseract_cmd = 'System_path_to_tesseract.exe'

    # Read image from which text needs to be extracted
    img = cv2.imread(image)

    # Preprocessing the image starts

    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    #Should be changed to configure by argument passing
    results = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT,config="-l Latin")


    for i in range(0, len(results["text"])):
        # extract the bounding box coordinates of the text region from
        # the current result
        x = results["left"][i]
        y = results["top"][i]
        w = results["width"][i]
        h = results["height"][i]
        # extract the OCR text itself along with the confidence of the
        # text localization

        # TODO: localize more than one word and aggregate rectangles
        text = results["text"][i]
        if re.search("projeto",text,re.I,) :
            conf = int(results["conf"][i])
            print("Confidence: {}".format(conf))
            print("Text: {}".format(text))
            text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0,0),-1)


    # show the output image
    cv2.imwrite(image,img)

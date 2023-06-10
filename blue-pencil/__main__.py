import argparse
import disasemble
import finder
import os
import find_and_censor
import img2pdf


def main():
    parser = argparse.ArgumentParser(
                prog='Blue Pencil',
                description='Python tool capable of censoring files. Works on any text based file and PDFs')

    parser.add_argument("filename", help="Name of the file to be annonimized")    # positional argument
    parser.add_argument("-o", "--outputFile", help="Name of the output file (without extension)", default="output")
    parser.add_argument("-p", "--patterns", help="Name of a file containing patterns to be detected (without extension)")
    parser.add_argument("-p2t","--pdf2text", help="Flag that indicates if pdf should be turned into .txt", action='store_true')
    parser.add_argument("-r", "--replace",help= "Flag that indicates that the program should replace entities found",default=False ,action='store_true')
    
    args = parser.parse_args()
    if args.patterns:
        extra_patterns = parse_extraPatterns(args.patterns)
    
    if (args.filename.endswith(".pdf") and args.pdf2text):
        processPDF2Text(args.filename,args.replace)

    elif (args.filename.endswith(".pdf")):
        processPDF(args.filename,args.replace)

    elif args.filename.endswith(".html") or args.filename.endswith(".txt") or args.filename.endswith(".xml") or args.filename.endswith(".md"):
        processTextF(args.filename,args.replace)
    
    else:
        print("File extension not supported!")



def processTextF(filename,replace):
    text =  open(filename).read()
    ents=finder.find_entities(text)
    output = find_and_censor.blue_markerText(ents,text,replace)
    open("output.txt","w").write(output)


def processPDF2Text(filename,replace):
    txtfiles = disasemble.pdf_to_text(filename,"pdfText/text")
    output=""
    counter=0
    for txt in txtfiles:
        text =  open(txt).read()
        result=finder.find_entities(text)
        output+= find_and_censor.blue_markerText(result,text,replace)
        counter+=1
    open("output.txt","w").write(output)

def processPDF(filename,replace):
    imgfiles =disasemble.pdf_to_image(filename,"pdfImages/image")
    txtfiles = disasemble.pdf_to_text(filename,"pdfText/text")
    counter=0
    for txt in txtfiles:
        print(txt)
        result=finder.find_entities(txt)
        find_and_censor.blue_markerPDF(result,"pdfImages/image"+str(counter)+".png",replace)
        counter+=1

    from fpdf import FPDF
    pdf = FPDF()
    # imagelist is the list with all image filenames
    for image in imgfiles:
        pdf.add_page()
        pdf.image(image,0,0, 210,297)
    pdf.output("yourfile.pdf", "F")

def parse_extraPatterns(filename):
    text = open(filename, 'r').read()
    lines = text.split('\n')
    print(lines)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()

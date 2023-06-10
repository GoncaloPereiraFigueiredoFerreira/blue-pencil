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
    args = parser.parse_args()

    if args.patterns:
        extra_patterns = parse_extraPatterns(args.patterns)
    
    if (args.filename.endswith(".pdf")):
        processPDF(args.filename)

    elif args.filename.endswith(".html") or args.filename.endswith(".txt") or args.filename.endswith(".xml") or args.filename.endswith(".md"):
        processTextF(args.filename)
    
    else:
        print("File extension not supported!")



def processTextF(filename):
    text =  open(filename).read()
    return finder.find_entities(text)
    

def processPDF(filename):
    disasemble.pdf_to_image(filename,"pdfImages/image")
    txtfiles = disasemble.pdf_to_text(filename,"pdfText/text")
    counter=0
    for txt in txtfiles:
        print(txt)
        result=processTextF(txt)
        find_and_censor.blue_marker(result,"pdfImages/image"+str(counter)+".png")
        counter+=1

    from fpdf import FPDF
    pdf = FPDF()
    # imagelist is the list with all image filenames
    for image in sorted([f for f in os.listdir("pdfImages")]):
        pdf.add_page()
        pdf.image("pdfImages/"+image,0,0, 210,297)
    pdf.output("yourfile.pdf", "F")

def parse_extraPatterns(filename):
    text = open(filename, 'r').read()
    lines = text.split('\n')
    print(lines)

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()

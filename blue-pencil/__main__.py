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
    parser.add_argument("-m", "--moreRestrictive", help="Extends entity recognition to include entities that are highly restrictive", action='store_true' )
    args = parser.parse_args()

    extra_patterns = []
    if args.patterns:
        extra_patterns = parse_extraPatterns(args.patterns)
    
    if (args.filename.endswith(".pdf")):
        processPDF(args.filename, extra_patterns)

    elif args.filename.endswith(".html") or args.filename.endswith(".txt") or args.filename.endswith(".xml") or args.filename.endswith(".md"):
        res = processTextF(args.filename, extra_patterns)
    
    else:
        print("File extension not supported!")



def processTextF(filename, extra_patterns):
    text = open(filename).read()
    res = finder.find_entities(text, extra_patterns)
    #for r in res:
    #    print(r)
    return res
    

def processPDF(filename, extra_patterns):
    imgfiles =disasemble.pdf_to_image(filename,"pdfImages/image")
    txtfiles = disasemble.pdf_to_text(filename,"pdfText/text")
    counter=0
    for txt in txtfiles:
        print(txt)
        result=processTextF(txt, extra_patterns)
        find_and_censor.blue_marker(result,"pdfImages/image"+str(counter)+".png")
        counter+=1

    from fpdf import FPDF
    pdf = FPDF()
    # imagelist is the list with all image filenames
    for image in imgfiles:
        pdf.add_page()
        pdf.image(image,0,0, 210,297)
    pdf.output("yourfile.pdf", "F")

def parse_extraPatterns(filename):
    res = []
    text = open(filename, 'r').read()
    lines = text.split('\n')
    for line in lines:
        if line != '': 
            line = line.split(' | ')
            elem = (r'' + line[0], r'' + line[1])
            res.append(elem)
    return res

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()

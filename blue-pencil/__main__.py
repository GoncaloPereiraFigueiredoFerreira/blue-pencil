import argparse
import disasemble

def main():
    parser = argparse.ArgumentParser(
                prog='Blue Pencil',
                description='Python tool capable of censoring pdf files')

    parser.add_argument("filename",help="Name .pss file, that describes the slideshow to be created")    # positional argument
    parser.add_argument("-o","--outputFile",help="Name of the output file, without extension",default="output")
    args = parser.parse_args()
    disasemble.pdf_to_image(args.filename,"pdfImages/image")
    disasemble.pdf_to_text(args.filename,"pdfText/text")



if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()

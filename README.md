# blue-pencil
A python anonymizer tool, capable of censoring names, adresses and other sensitive info.
```
usage: Blue Pencil [-h] [-o OUTPUTFILE] [-p PATTERNS] [-org] [-m] [-p2t] [-r] [-l LANGUAGE] filename

Python tool capable of censoring files. Works on any text based file and PDFs

positional arguments:
  filename              Name of the file to be annonimized

options:
  -h, --help            show this help message and exit
  -o OUTPUTFILE, --outputFile OUTPUTFILE
                        Name of the output file (without extension)
  -p PATTERNS, --patterns PATTERNS
                        Name of a file containing patterns to be detected (without extension)
  -org, --organizations
                        Extends entity recognition to include organizations
  -m, --moreRestrictive
                        Extends entity recognition to include entities that are highly restrictive
  -p2t, --pdf2text      Flag that indicates if pdf should be turned into .txt
  -r, --replace         Flag that indicates that the program should replace entities found
  -l LANGUAGE, --language LANGUAGE
                        Language of the input file: en or pt
```

Total development report in portguese in the SPLN-Ferramenta_de_Anonimização.pdf file.
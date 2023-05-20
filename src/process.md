1. Tornar pdf em serie de imagens
2. Transformar PDF em texto e dividir em páginas
3. Correr spacy por todas as páginas e localizar páginas e nomes
4. Correr opencv e pytesseract para encontrar e substituir por censored
5. Criar paginas pdf a partir das imagens mudadas
6. Merge de pdfs num unico

Vai perder qualidade e a possibilidade de copy/paste (vão ser read only)



Dependencias:

pip install opencv-python
pip install pytesseract
pip install spacy (com português nlp)
pip install pypdf
pip install pdf2image

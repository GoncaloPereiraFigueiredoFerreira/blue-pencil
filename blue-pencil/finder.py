#!/usr/bin/python3

import spacy
nlp = spacy.load("pt_core_news_lg")

import re
# TODO: encontrar morada
exps = [('email...', r'[a-zA-Z](\w)*@[a-zA-Z](\w)*\.[a-zA-Z](\w)*'), 
        ('código postal...', r'\d{4}-\d{3}'), 
        ('NSS...', r'\d{12}'), ('BI...', r'\d{8}'), 
        ('carta de condução...', r'[A-Z]{1,2}\-\d{6}'), 
        ('data...', r'\d\d?(-|\/|\.)\d\d?(-|\/|\.)\d\d{1,3}'),
        ('twitter...', r'@\w*'),
        ('www...', r'(http(s)?:\/\/)?(www\.)?[a-zA-z0-9]+\.[a-zA-z0-9]+')]
# TODO: extensão do website, p.ex., www.youtube.com/ (watch?asdsadasdasdas)
# telemóvel, NIF e NUS têm o mesmo número de dígitos

def find_entities(text):
    res = []
    doc = nlp(text)
    length = 0
    for w in doc:
        matched = False
        exp = -1
        for i in range(0, len(exps)):
            match = re.fullmatch(exps[i][1], w.text)
            if match:
                exp = i
                matched = True
                break
        if matched:
            res.append((w.text, (length, length + len(w.text), exps[exp][0])))

        # TODO: identificar números de acordo com o contexto
        # TODO: add more labels
        elif w.ent_type_ != '':
            res.append((w.text, (length, length + len(w.text), w.ent_type_)))
        length += len(w.text)
        length += len(w.whitespace_)
    #print(res)
    return res

rfile = open('test', 'r')
text = rfile.read()
find_entities(text)

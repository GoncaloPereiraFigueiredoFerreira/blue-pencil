#!/usr/bin/python3

import spacy
nlp = spacy.load("pt_core_news_lg")

import re
morada = ('morada...', r'(Avenida|Rua|Tv\.|Trv\.|Travessa)(\s(d[eao]s?\s)?([A-Z]\w+(\.)?))*(\s[nN](º)?\d+)?')
exps = [('email...', r'[a-zA-Z](\w)*@[a-zA-Z](\w)*\.[a-zA-Z](\w)*'), 
        ('código postal...', r'\d{4}-\d{3}'), 
        ('NSS...', r'\d{11}'), 
        ('número...', r'\d{9}'), 
        ('BI...', r'\d{8}'), 
        ('carta de condução...', r'[A-Z]{1,2}\-\d{6}'), 
        ('data...', r'\d\d?(-|\/|\.)\d\d?(-|\/|\.)\d\d{1,3}'),
        ('twitter...', r'@\w*'),
        ('www...', r'(http(s)?:\/\/)?(www\.)?[a-zA-z0-9]+\.[a-z]{2,3}(\/[a-zA-z0-9]+)?(\/)?')]
# telemóvel, NIF e NUS têm o mesmo número de dígitos


def find_entities(text, extra_patterns):
    res = []
    length = 0
    lines = text.split('\n')

    for line in lines:
        exp = -1
        for i in range(0, len(extra_patterns)):
            match = re.search(extra_patterns[i][0], line)
            if match:
                res = add_detection(res, (match.group(0), (length + match.span()[0], length + match.span()[1]), extra_patterns[i][1]))
                break

        match = re.search(morada[1], line)
        if match:
            res = add_detection(res, (match.group(0), (length + match.span()[0], length + match.span()[1]), morada[0]))

        words = line.split()
        for w in words:
            for i in range(0, len(exps)):
                match = re.match(exps[i][1], w)
                if match:
                    res = add_detection(res, (match.group(0), (length + match.span()[0], length + match.span()[1]), exps[i][0]))
                    break

        doc = nlp(line)
        for w in doc.ents:           
            if w.label_ in ['PER','GPE']:
                res = add_detection(res, (w.text, (length, length + len(w.text)), w.label_))
            length += len(w.text)

        length += 1

    for r in res:
        print(r)

    return res


def add_detection(l, elem):
    if doesntIntersect(l, elem[1]):
        l.append(elem)
    return l

def doesntIntersect(array,element): 
    elementRange=set([*range(element[0],element[1])])
    for i in array:
        irange = set([*range(i[1][0],i[1][1])])
        if (len(elementRange.intersection(irange))!=0 ):
            return False

    return True

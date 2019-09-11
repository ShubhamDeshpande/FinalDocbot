import re
import spacy
import os
import pandas as pd
nlp=spacy.load('en')

def checkBMIVariables(query):
    doc=nlp(query)
    types=[token.pos_ for token in doc if token.pos_=='NUM']
    if types.count('NUM')==2:
        return True,types.count('NUM')
    else:
        if 'weight' in query:
            return False,'height'
        if 'height' in query:
            return False,'weight'
        else:
            return False,''

def parseBMIQuery(query):
    print(query)
    parsed_info={}
    parsed_numbers=[int(num) for num in re.findall(r'\d+',query)]
    ht_wt=re.findall(r'(weight|height)',query)
    parsed_units=re.findall(r'\d+\s*(cm|m|kg)',query)
    print(ht_wt)
    print(parsed_numbers)
    occurences=[i for i,unit in enumerate(parsed_units) if unit=="cm"]
    for i in occurences:
        parsed_numbers[i]/=100
        parsed_units[i]="m"
    parsed_info[ht_wt.pop()]=parsed_numbers.pop()
    parsed_info[ht_wt.pop()]=parsed_numbers.pop()
    return parsed_info

def parseBAIQuery(query):
    parsed_info={}
    parsed_numbers=[int(num) for num in re.findall(r'\d+',query)]
    ht_hip=re.findall(r'(hip circumference|height)',query)
    parsed_units=re.findall(r'\d+\s*(cm|m)',query)    
    occurences=[i for i,unit in enumerate(parsed_units) if unit=="cm"]
    for i in occurences:
        parsed_numbers[i]/=100
        parsed_units[i]="m"
    print(parsed_numbers)
    print(ht_hip)
    parsed_info[ht_hip.pop()]=parsed_numbers.pop()
    parsed_info[ht_hip.pop()]=parsed_numbers.pop()
    return parsed_info

def parseName(query):
    doc=nlp(query)
    name=""
    for token in doc:
        if token.pos_ in ['NOUN','ADJ','PROPN']:
            if len([child for child in token.children])==0:
                name=str(token)
    return name.capitalize()

def ExtractDisease(query):
    pattern=re.compile('\w+ symptoms of (?P<disease>\w+)')
    temp=pattern.search(query)
    return temp.groupdict()['disease']

def ExtractSymptoms(ROOT_DIR,query):
#    doc=nlp(query)
#    tokens=[]
#    for chunk in doc.noun_chunks:
#        tokens.append(chunk.text)
#    for token in doc:
#        if not (token.is_stop or token.is_punct):
#            if token.pos_=='NOUN':
#                continue
#            elif token.text in tokens:
#                tokens.remove(token.text)
#    return tokens
    symptoms=[]
    df=pd.read_csv(os.path.join(ROOT_DIR,'datasets/preprocessed/df_pivoted.csv'))
    diseases=list(df.columns[1:])
    diseases.sort(reverse=True)
    for i in range(len(diseases)):
        if diseases[i] in query:
            symptoms.append(diseases[i])
            query=' '.join(query.rsplit(diseases[i]))
    return symptoms


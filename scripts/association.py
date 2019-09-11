import pandas as pd
import pyfpgrowth
import pickle
import codecs
import json

class SymptomsAssociation:
    def __init__(self,mode):
        if mode=='train':
            self.load_data()
            self.create_association_rules()
        else:
            self.asked=[]
            self.load_rules()
    def create_association_rules(self):
        symptoms_transactions=self.df.loc['symptoms']
        patterns=pyfpgrowth.find_frequent_patterns(symptoms_transactions,3)
        self.rules=pyfpgrowth.generate_association_rules(patterns,0.95)
        self.store_rules()   
    def load_data(self):
        self.df=pd.DataFrame(json.load(codecs.open('/home/shubham/Desktop/Docbot/datasets/preprocessed/diseases.json','r','utf-8-sig')))
    def store_rules(self):
        pickle.dump(self.rules,open('/home/shubham/Desktop/Docbot/models/custom/rules.b','wb'))
    def load_rules(self):
        self.rules=pickle.load(open('/home/shubham/Desktop/Docbot/models/custom/rules.b','rb'))
    def filter_rules(self,symptoms):
        required_rules={}
        self.asked=[symptom for symptom in symptoms]
        for rule in self.rules.keys():
            if set(symptoms).issubset(rule):
                required_rules[rule]=self.rules[rule]
        self.filtered_rules=required_rules
    def get_next_symptom(self,symptoms):
        if self.filtered_rules.get(tuple(symptoms)) is not None:
            symptom=self.filtered_rules.get(tuple(symptoms))[0][0]
            if symptom not in self.asked:
                self.asked.append(symptom)
                return symptom
            else:
                return self.generate_symptom(symptoms)
        else:
            return self.generate_symptom(symptoms)
        
        
    def generate_symptom(self,symptoms):
        self.temp=sorted(self.filtered_rules.items(),key=lambda key:len(key[0]))
        i=0
        symptom=set(self.temp[0][0]).difference(symptoms)
        if len(symptom)!=0:
            symptom=symptom.pop()
        while True:
            if i>=len(self.temp):
                break
            symptom=set(self.temp[i][0]).difference(symptoms)
            if len(symptom)!=0:
                symptom=symptom.pop()
            if len(symptom)==0:
                i+=1
                continue
            if symptom not in self.asked:
                break
            i+=1
        if symptom in self.asked:
            symptom="None"
        else:
            self.asked.append(symptom)
        return symptom
            

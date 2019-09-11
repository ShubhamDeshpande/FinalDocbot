import pandas as pd
import numpy as np
import pickle
import os
from joblib import dump,load
from scripts.disease_to_symptoms import D2S
from sklearn.ensemble import RandomForestClassifier

class S2D:
    def __init__(self,ROOT_DIR,mode="train"):
        self.ROOT_DIR=ROOT_DIR
        if mode=="train":
            self.load_data()
            self.model=RandomForestClassifier(300,n_jobs=-1)
        else:
            self.model=load(os.path.join(self.ROOT_DIR,'models/custom/S2D.joblib'))
            self.diseases,self.symptoms_list=pickle.load(open(os.path.join(self.ROOT_DIR,'models/custom/S2D.b'),'rb'))
    def load_data(self):
        self.data=pd.read_csv(os.path.join(self.ROOT_DIR,'datasets/preprocessed/df_pivoted.csv'))
    def train(self):
        self.symptoms_list=self.data.columns[2:]
        self.diseases=self.data['Source']
        symptoms=self.data.iloc[:,2:]
        self.model.fit(symptoms,self.diseases)
        self.store_params()
    def predict(self,symptoms):
        self.symptoms=symptoms
        symptom_vector=np.zeros(self.symptoms_list.size)
        for s in symptoms:
            symptom_vector[self.symptoms_list.get_loc(s)]=1
        probabilities=self.model.predict_proba([symptom_vector])
        predictions=sorted(zip(probabilities[0],self.diseases),reverse=True)
        predicted_diseases=[]
        i=0
        while len(predicted_diseases)!=3 and i<len(predictions):
            disease=predictions[i][1].replace('\xa0',' ')
            self.t=disease
            self.validity_string=D2S(self.ROOT_DIR,disease.lower())
            if self.check_prediction():
                predicted_diseases.append(disease)
            i+=1
        if len(predicted_diseases)!=0:
            return predicted_diseases
        else:
            return [d[1] for d in predictions[:3]]
    def check_prediction(self):
        for symptom in self.symptoms:
            if symptom not in self.validity_string:
                return False
        return True
    def store_params(self):
        dump(self.model,os.path.join(self.ROOT_DIR,'models/S2D.joblib'))
        pickle.dump((self.diseases,self.symptoms_list),open(os.path.join(self.ROOT_DIR,'models/S2D.b'),'wb'))
        
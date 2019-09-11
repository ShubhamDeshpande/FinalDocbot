import os
from scripts import symptoms_to_disease
from scripts import association
from scripts.sentence_generation import TextGenerator

class Ontology:
    def __init__(self,ROOT_DIR):
        self.classifier=symptoms_to_disease.S2D(ROOT_DIR,mode='test')
        self.question_asker=association.SymptomsAssociation(mode='test')
        self.question_asker.load_rules()
        self.ROOT_DIR=ROOT_DIR
        self.iterator=0
    
    def record_initial_symptoms(self,initial_symptoms):
        """
        initial_symptoms must be list of symptoms
        """
        self.question_asker.filter_rules(initial_symptoms)
        self.initial_symptoms=initial_symptoms
        self.possible_symptoms={}
        while True:
            next_symptom=self.question_asker.get_next_symptom(self.initial_symptoms)
            if next_symptom!="None":
                self.possible_symptoms[next_symptom]=True
            else:
                break
        self.symptoms_list=list(self.possible_symptoms.keys())
    
    def ask_question(self):
        if self.iterator==len(self.symptoms_list):
            return "END"
        self.current_symptom=self.symptoms_list[self.iterator]
        question="Are you suffering from "+self.current_symptom+"?"
        self.iterator+=1
        return question
    
    def record_response(self,answer):
        if answer=='n':
            self.possible_symptoms[self.current_symptom]=False
        
    def predict_disease(self):
        self.classifier=symptoms_to_disease.S2D(self.ROOT_DIR,mode='test')
        self.symptoms_list=[k for k,v in self.possible_symptoms.items() if v==True]
        self.symptoms_list+=self.initial_symptoms
        predicted_disease=self.classifier.predict(self.symptoms_list)
        generator=TextGenerator()
        return generator.generate_S2D_response(predicted_disease)
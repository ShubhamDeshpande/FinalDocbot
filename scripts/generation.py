import os
from settings import ROOT_DIR
from scripts import utilities
from scripts.disease_to_symptoms import D2S
from scripts.ontology import Ontology
from scripts.medical_conversation_query import MedicalQuery
from scripts.generalquery import general
import random
import spacy
nlp = spacy.load('en')

class Generation:
    def __init__(self,root):
        self.root=root
    
    def generateReply(self,analysis_wrapper,context_wrapper):
        self.analysis_info=analysis_wrapper.percept
        self.context=context_wrapper.context
        if self.analysis_info.get("None")==True:
            #self.analysis_info.pop("None",None)
            #self.context.pop("None",None)
            self.analysis_info.clear()
            self.context.clear()
            return None
        if self.context.get('conversation')==True:
            gen=MedicalQuery(ROOT_DIR)
            self.context.pop('conversation',None)
            response,confidence=gen.generate_response(self.analysis_info['conversation'])
            if confidence<0.25:
                response=general.search(self.analysis_info['conversation'])[0].description
                docs= nlp(response)
                list1 = [token.text for token in docs]
                months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                list2 = []
                if list1[0] in months:
                    for i in range(5,len(list1)): 
                        list2.append(list1[i])
                        response1 = " ".join(list2)
                else:
                    response1=response
                response=response1
            self.analysis_info.pop('conversation',None)
            print(response)
            return response

        if self.analysis_info.get('opener') is not None:
            if self.context.get('name') is None:
                reply=open(os.path.join(self.root,'datasets/raw/conversation_opener_queries')).readlines()[1].rstrip('\n').split('\t')
                return random.choice(reply)
            if self.context.get('greet') == False:
                self.context['greet']=True
                self.analysis_info.pop('opener',None)
                greetings=open(os.path.join(self.root,'datasets/raw/conversation_opener_queries')).readlines()[2].rstrip('\n').split('\t')
                return utilities.GreetUser(self.context['name'],greetings)
        elif self.analysis_info.get('close') is not None:
            reply=open(os.path.join(self.root,'datasets/raw/conversation_end_queries')).readlines()[1].rstrip('\n').split('\t')
            return random.choice(reply)
        elif self.context.get('bmi') is not None:
            self.context.pop('bmi',None)
            bmi=utilities.CalculateBMI(self.analysis_info['bmi']['height'],self.analysis_info['bmi']['weight'])
            self.analysis_info.pop('bmi',None)
            return bmi
        elif self.analysis_info.get('bai') is not None:
            self.context.pop('bai',None)
            ht=self.analysis_info['bai']['height']
            cir=self.analysis_info['bai']['hip circumference']
            self.analysis_info.pop("bai",None)
            return utilities.CalculateBAI(self.analysis_info['bai']['height'],self.analysis_info['bai']['hip circumference'])
        elif self.context.get('d2s') is not None:
            self.context.pop('d2s')
            buffer=self.analysis_info['d2s']
            self.analysis_info.pop('d2s',None)
            result=D2S(self.root,buffer)
            if result is None:
                gen=MedicalQuery(ROOT_DIR)
                results,confidence=gen.generate_response("What are the symptoms of "+buffer)
                if confidence<0.25:
                    result=general.search(self.analysis_info['conversation'])[0].description 
                    docs= nlp(result)
                    list1 = [token.text for token in docs]
                    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
                    list2 = []
                    if list1[0] in months:
                        for i in range(5,len(list1)): 
                            list2.append(list1[i])
                            result = " ".join(list2)
                    else:
                        result=response
            self.analysis_info.pop('conversation',None)
            print(result)
            return result
        elif self.context.get('s2d') is not None:
            if self.context['s2d']==True:
                self.context['s2d']=Ontology(self.root)
                self.context['s2d'].record_initial_symptoms(self.analysis_info['s2d'])
            ontology=self.context['s2d']
            question=ontology.ask_question()
            if  question=="END":
                disease=ontology.predict_disease()
                self.context.pop('s2d',None)
                self.analysis_info.pop('s2d',None)
                return disease
            return question

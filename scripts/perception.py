from scripts import parse_query
import os
from scripts import wrappers
import re


class Perception:
    def __init__(self,root):
        self.root=root
        self.context={}
        self.analysis={}
        self.buffered_queries=[]
    def analyzeQuery(self,query):
        try:
            print(query)
            self.query=query
            conversation=True
            #(Calculate|Tell|Provide)
            regex_dict={'bmi':re.compile(r'.*my.*bmi.*'),'bai':re.compile(r'.*.*bai.*'),'d2s':re.compile(r'\w+ symptoms of \w+'),'s2d':re.compile(r'\w+ (suffering from|feeling) \w+')}
            if self.analysis.get('opener')==True:
                self.context['name']=parse_query.parseName(query)
                self.context['greet']=False
                conversation=False
            file=open(os.path.join(self.root,'datasets/raw/conversation_opener_queries')).readlines()[0].rstrip('\n').split('\t')
            if self.query in file:
                self.analysis['opener']=True
                conversation=False
            file=open(os.path.join(self.root,'datasets/raw/conversation_end_queries')).readlines()[0].rstrip('\n').split('\t')
            if self.query in file:
                self.analysis['close']=True
                conversation=False
            if self.context.get('bmi') is not None:
                print("Inside")
                temp=re.findall('(\d+\s*cm)|(\d+\s*kg)',self.query)
                temp=[''.join(temp[i]) for i in range(len(temp))]
                self.buffer.append(self.query)
                #self.buffer=self.buffer+temp
                print(self.buffer)
                if parse_query.checkBMIVariables(' '.join(temp))[0]==True:
                    self.analysis['bmi']=parse_query.parseBMIQuery(' '.join(self.buffer))
                    self.buffer=[]
                conversation=False
            elif regex_dict['bmi'].match(query):
                bmi_query_analysis=parse_query.checkBMIVariables(query)
                if bmi_query_analysis[0]:
                    print("First")
                    self.analysis['bmi']=parse_query.parseBMIQuery(self.query)
                else:
                    if bmi_query_analysis[1]=='':
                        self.buffered_queries=['Can you please tell me your height and weight? eg. my height is 180 cm and weight is 70kg']
                    else:
                        self.buffered_queries=['Can you please tell me your '+bmi_query_analysis[1]]
                    self.buffer=[self.query,bmi_query_analysis[1]]
                self.context['bmi']=True
                conversation=False
            if self.context.get('bai') is not None:
                self.analysis['bai']=parse_query.parseBAIQuery(self.query)
                conversation=False
            elif regex_dict['bai'].match(query):
                self.buffered_queries=['Can you please tell me your height and hip circumference?']
                conversation=False
                self.context['bai']=True
            if regex_dict['d2s'].search(query):
                self.context['d2s']=True
                self.analysis['d2s']=parse_query.ExtractDisease(query)
                conversation=False
            if self.context.get('s2d') is not None:
                if query.lower() in ['yes','yup','yep','y','right','yeah']:
                    query='y'
                else:
                    query='n'
                self.context['s2d'].record_response(query)
                conversation=False
            if regex_dict['s2d'].search(query):
                self.context['s2d']=True
                self.analysis['s2d']=parse_query.ExtractSymptoms(self.root,query)
                conversation=False
            if conversation==True:
                self.context['conversation']=True
                self.analysis['conversation']=query
            return wrappers.AnalysisWrapper(self.analysis),wrappers.ContextWrapper(self.context)
        except:
            print("Caught error")
            self.analysis["None"]=True
            self.context["None"]=True
            return wrappers.AnalysisWrapper(self.analysis),wrappers.ContextWrapper(self.context)

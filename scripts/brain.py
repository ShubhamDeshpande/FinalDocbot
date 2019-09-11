import spacy
from scripts import perception
from scripts import generation
nlp=spacy.load('en')
class Brain:
    def __init__(self,root_dir):
        self.root=root_dir
        self.percept=perception.Perception(self.root) 
        self.generate=generation.Generation(self.root)
    
    def predict(self,query):
        self.query=query.lower()
        understanding,context=self.percept.analyzeQuery(self.query)
        if len(self.percept.buffered_queries)!=0:
            print(understanding.percept)
            print(context.context)
            return "buffered_queries",self.percept.buffered_queries
        print(understanding.percept)
        print(context.context)
        return "response",self.generate.generateReply(understanding,context)
    
    def print(self):
        print(self.percept.analysis)
        print(self.generate.context)
    
    def process_buffered_queries(self,buffered_ans):
        if len(buffered_ans)>1:
            for i in range(len(buffered_ans)-1):
                self.percept.analyzeQuery(buffered_ans[i].lower())
        self.percept.buffered_queries=[]
        return self.predict(buffered_ans[0])[1]
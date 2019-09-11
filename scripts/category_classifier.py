import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import gc
from sklearn.preprocessing import LabelEncoder
import spacy
import joblib
import pickle
import os
nlp=spacy.load('en')
class CategoryClassifier:
    def __init__(self,ROOT_DIR,mode):
        if mode=="train":
            self.df=pd.read_csv(os.path.join(ROOT_DIR,'question_category.csv'))
            print("Dataset loaded.......")
            self.encoder=LabelEncoder()
            self.vectorizer=TfidfVectorizer()
            #self.questions=self.vectorizer.fit_transform(self.df['question'].values.astype(str))
            self.category=self.encoder.fit_transform(self.df['main_category'].values)
            print("Labels encoded.......")
            self.preprocess()
            print("Processed......")
            gc.collect()
        else:
            self.vectorizer,self.encoder=pickle.load(open(os.path.join(ROOT_DIR,"models/custom/helpers.b"),"rb"))
            #self.vectorizer=buffer[0]
            #self.encoder=buffer[1]
            self.model=joblib.load(os.path.join(ROOT_DIR,"models/custom/CatClf.b"))
    def preprocess(self):
        self.processed_docs=[]
        for i in range(len(self.df)):
            line=self.df.loc[i,'question']
            line=self.process_line(line)
            self.processed_docs.append(line)
            if i%10000==0:
                print(str(i)," lines processed.")
        self.df=pd.DataFrame({"questions":self.processed_docs,"main_category":self.category})

    def process_line(self,line):
        doc=nlp(line)
        doc=[token for token in doc if not token.is_punct]
        doc=[token for token in doc if not token.is_digit]
        doc=[token for token in doc if not token.is_stop]
        doc=[token.lemma_.lower().strip() for token in doc if token.lemma_!='-PRON-']
        return " ".join(doc)
    def train(self):
        self.questions=self.vectorizer.fit_transform(self.df.loc[:,"questions"].values)
        self.model=MultinomialNB()
        self.model.fit(self.questions,self.category)
        joblib.dump(self.model,'CatClf.b')
        pickle.dump((self.vectorizer,self.encoder),open("helpers.b","wb"))
    def predict(self,query):
        query=self.process_line(query)
        query=self.vectorizer.transform([query])
        category=self.model.predict(query)
        return self.encoder.inverse_transform(category)[0]

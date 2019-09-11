from nltk.chat.util import Chat
import ast
class NLTKChatbot:
    def __init__(self,filename):
        self.d={}
        data=open(filename).read().split('\n')
        questions,answers=[],[]
        for obj in data:
            temp=obj.split("#")
            questions.append(temp[0])
            answers.append(temp[1])
        self.paired_data=[]
        for i in range(len(questions)):
            temp=answers[i].split('$')
            temp=[ans+'$'+temp[1] for ans in temp[0].split('\t')]
            self.paired_data.append([questions[i],temp])
    def opener(self):
        self.d['opener']=True
    def start_chatbot(self):    
        self.engine=Chat(self.paired_data)
    def execute_method(self,method_name):
        exec(compile(ast.parse('self.'+method_name+'()'),filename="",mode="exec"))
    def generate_response(self,question):
        response=self.engine.respond(question).split('$')
        method_name=response[1]
        response=response[0]
        self.execute_method(method_name)
        return response
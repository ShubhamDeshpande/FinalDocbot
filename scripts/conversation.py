from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from os import listdir 
from os.path import isfile,join
from chatterbot.comparisons import jaccard_similarity
from chatterbot.response_selection import get_first_response
import os

class ConversationModel:
	def train(self):
		q_path =r"/home/mayur/Desktop/Giri/Question/"
		q_files = [f for f in listdir(q_path) if isfile(join(q_path, f))]
		q_files.sort()
		print(q_files)
		a_path =r"/home/mayur/Desktop/Giri/Answer/"
		a_files = [f for f in listdir(a_path) if isfile(join(a_path, f))]
		a_files.sort()
		print(a_files)
		
		db_name = a_files.copy()
		db_name = [x[2:-4] for x in db_name] 

		print(db_name)

		for k in range(len(db_name)):
			url="sqlite:///"+db_name[k]+".sqlite3"
			print(url)
			chatbot = ChatBot('Bot',
			storage_adapter='chatterbot.storage.SQLStorageAdapter',
			trainer='chatterbot.trainers.ListTrainer',
			database_uri=url)

			print("Training "+q_files[k]+" with "+a_files[k])
			q_filepath='/home/mayur/Desktop/Giri/Question/'+q_files[k]
			a_filepath='/home/mayur/Desktop/Giri/Answer/'+a_files[k]
			question_file=open(q_filepath,'r').read().split('\n')[1:]
			answer_file=open(a_filepath,'r').read().split('\n')
			trainer=ListTrainer(chatbot)
			for i in range(len(question_file)):
				try:
					trainer.train([question_file[i],answer_file[i]])
				except IndexError:
				    pass
				continue
			print("Training completed")
			

	def predict(self,ROOT_DIR,query,category):
		temp=os.getcwd()
		os.chdir(os.path.join(ROOT_DIR,'models/custom/chatterbot_models'))
		chatbot=ChatBot('DocBot',
		storage_adapter='chatterbot.storage.SQLStorageAdapter',logic_adapters=[{"import_path": "chatterbot.logic.BestMatch","statement_comparison_function": jaccard_similarity,"response_selection_method":get_first_response}],database_uri=('sqlite:///'+category+'.sqlite3'),read_only=True)
		response=chatbot.get_response(query)
		print("Confidence:",response.confidence)
		print(response)
		os.chdir(temp)
		return str(response),response.confidence


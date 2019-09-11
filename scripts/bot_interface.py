from scripts import brain as b
class BotInterface:
    def __init__(self,ROOT_DIR):
        self.brain=b.Brain(ROOT_DIR)
        self.buffered_questions=[]
        self.buffered_answers=[]
        self._mode="response"
        self.i=0
    def ask_question(self,query):
        if self._mode=='buffered_queries':
            self.buffered_answers.append(query)
            question=self.ask_buffered_question()
            if question=="END":
                buffer=self.buffered_answers
                self.buffered_answers=[]
                return self.brain.process_buffered_queries(buffer)
            return question
        intermediate_response=self.brain.predict(query)
        self._mode=intermediate_response[0]
        if self._mode=='buffered_queries':
            self.buffered_questions=intermediate_response[1]
            return self.ask_buffered_question()
        else:
            if intermediate_response[1] is not None:
                return intermediate_response[1]
            else:
                return "Sorry, I don't recognize that"
    def get_mode(self):
        return self._mode
    def ask_buffered_question(self):
        if self.i==len(self.buffered_questions):
            self.i=0
            self.buffered_questions=[]
            self._mode="response"
            return "END"
        temp=self.buffered_questions[self.i]
        self.i+=1
        return temp

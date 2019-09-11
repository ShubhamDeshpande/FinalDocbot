from scripts.category_classifier import CategoryClassifier
from scripts.conversation import ConversationModel

class MedicalQuery:
    def __init__(self,ROOT_DIR):
        self.ROOT_DIR=ROOT_DIR
        self.classifier=CategoryClassifier(ROOT_DIR,mode="test")
        self.response_generator=ConversationModel()
    def generate_response(self,query):
        query_class=self.classifier.predict(query)
        return self.response_generator.predict(self.ROOT_DIR,query,query_class)
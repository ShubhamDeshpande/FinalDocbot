import markovify
import random
from random import sample


class TextGenerator:
    def __init__(self):
#        self.disease_text_generator=markovify.NewlineText(open('response_templates.txt').read().split('\n'),state_size=2)
#    def generate_response(self,disease):
#        line=self.disease_text_generator.make_sentence()
#        return re.sub('\w*__DISEASE__',disease,line)
        pass
    def generate_S2D_response(self,possible_diseases):
        foods = ["Tomatoes", "Spinach", "Brocoli", "Wheat", "Sweet Potato","Apples , Pears", "Oranges , Lemons","Peaches , Plums","Grapes","Melons","Cabbages","Avocado","Asparagus","Green Beans","Fish","Canned Beans","Low Sodium Salsa","Eggs","Greek Yoghurt","Milk","Cheese","Butter","Tea","Coffee","100% Orange Juice","Honey","Ginger","Olive oil","Sea Salt","Clove","Mustard"]
        food = sample(foods, 5)
        temp='\n'.join(possible_diseases[:-1])
        temp+=("\n"+possible_diseases[-1])
        sentence="You might be suffering from : \n"+temp+". \n---------------------\n Food Tip : \n"+food[0]+"\n"+ food[1]+"\n"+food[2]+"\n"+food[3]+"\n"+food[4]+""
        return sentence
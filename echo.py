import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import ROOT_DIR
from scripts.bot_interface import BotInterface
import emoji

updater_=None
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
#bot=BotInterface(ROOT_DIR)
user_object_dict=dict()
server_start_time=None

def start(update, context):
    #context.message.reply_text('Hi! I am your medical consultant \n I can perform following functions :\n 1. Calculate BMI \n 2. Calculate BAI \n 3. Predict Disease from your symptoms \n 4. Give you symptoms about particular disease \n What can i do for you?')
    context.message.reply_text('Hi! I am DocBot, your medical consultant '+emoji.emojize(':beaming_face_with_smiling_eyes:')+'\n I can perform functions :\n 1. Calculate BMI \n 2. Calculate BAI \n 3. Predict Disease from your symptoms \n 4. Give you symptoms about particular disease \n5. What can also ask me medical queries \n\n What can I do you ?')
    user_object_dict[context.message.from_user.id]=BotInterface(ROOT_DIR)

def help(update, context):
    update.message.reply_text("I'm your medical chatbot")


def sendmsgtouser(update, context,response):
    """Echo the user message."""
    ### generated response
    ### 
    if response is None:
        response = "I did not understand what you said, please try again ..."+emoji.emojize(':worried_face:')
    else:
        print(response)
    #bot.ask_question(msg)    
    context.message.reply_text(response)
    
def getmsgfromuser(update, context):
    """Echo the user message."""
    global server_start_date
    if server_start_time<=context.message.date:
        msg = context.message.text  #user's msg
        print("Msg from user : ",msg)
        id_=context.message.from_user.id
        if id_ not in user_object_dict.keys():
    	    user_object_dict[id_]=BotInterface(ROOT_DIR)
        bot=user_object_dict[id_]
        response = bot.ask_question(msg)
        print("Working on Response ... ")
        sendmsgtouser(update,context,response)

def main():
    updater = Updater("584947439:AAHIRNK56e2octIOY7FL8KTQMmlqJgCirqw")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, getmsgfromuser))
    #dp.add_handler(MessageHandler(Filters.text, sendmsgtouser))
    #dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()
    global updater_
    updater_=updater

def set_server_start_time(time):
    global server_start_time
    server_start_time=time

def stop():
    user_object_dict={}

if __name__ == '__main__':
    main()

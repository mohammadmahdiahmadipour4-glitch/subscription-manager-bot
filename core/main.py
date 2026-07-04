import telebot
import os 
import pprint
import json 
import random 
import logging 
from PIL import Image
API_TOKEN = os.getenv("Telegram_API_token")

logger = telebot.logger
telebot.logger.setLevel(logging.INFO) 

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start' , 'setname'])
def send_welcome(message):
    if message.text != "/setname":
        bot.send_message(message.chat.id , f"Hi {message.chat.first_name} , how can i help you ?")
        logger.info(f"User {message.chat.first_name} started the bot.") 
    else : 
        send_msg = bot.send_message(message.chat.id , "Please send me your name!")
        bot.register_next_step_handler(send_msg,set_name) 
        


def set_name(message):
    if (message.content_type!="text"):
            bot.reply_to(message, "Please send a valid name.")
            bot.register_next_step_handler(message,set_name)
            return
    if not message.text.replace(" ", "").isalpha() : 
        bot.reply_to(message, "wow! there is a number in your name? tell me the truth!!!")
        bot.register_next_step_handler(message,set_name)
        return
    
    user_name = message.text    
    send_msg = bot.send_message(message.chat.id , f"welcom {user_name} . please send your age .")
    bot.register_next_step_handler(send_msg, set_age , user_name)

def set_age(message , user_name):
    if (message.content_type!="text"):
            bot.reply_to(message, "Please send a valid age.")
            bot.register_next_step_handler(message,set_age , user_name)
            return 
    if not message.text.isdigit() :
        bot.reply_to(message, "wow there is a letter in your age? tell me the truth!!!")
        bot.register_next_step_handler(message,set_age , user_name)
        return
    
    user_age = message.text    
    send_msg = bot.send_message(message.chat.id , f" your name and age has been set successfully.{user_name} you are {user_age} years old\nif their correct confirm it by sending 'yes' or send 'no' to change them.")
    logger.info(f"User {message.chat.first_name} set their name to '{user_name}' and age to '{user_age}'.")
    bot.register_next_step_handler(send_msg, confirm_details , user_name , user_age)

def confirm_details(message , user_name , user_age ):
    if message.text.lower() == "yes":
        bot.send_message(message.chat.id, "Great! Your details have been confirmed.\n" + get_user_info(message ,  user_name , user_age))
        logger.info(f"User {message.chat.first_name} confirmed their details.")
        
    elif message.text.lower() == "no":
        send_msg = bot.send_message(message.chat.id , "Please send me your name again!")
        bot.register_next_step_handler(send_msg,set_name)
    else: 
        bot.reply_to(message, "Please respond with 'yes' or 'no'.")
        bot.register_next_step_handler(message, confirm_details , user_name , user_age)


def get_user_info( message  , user_name , user_age): 
    user_info = f"your name: {user_name}\nyour age: {user_age} \n your acocunt name: {message.chat.first_name} \n your acoourn id : @{message.chat.username} \n your name in telegram : {message.chat.first_name}. "
    return user_info









@bot.message_handler(regexp="^zahra$")
def handle_zahra(message):
    bot.reply_to(message, 'did you just say my girl name?')
    logger.info(f"User {message.chat.first_name} mentioned 'zahra'.")

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: "dios" in message.text or "تاس" in message.text)
def hendle_dios_random(message):
    random_number = random.randint(1, 6)
    if random_number == 6:
        bot.reply_to(message, f"عدد تاس : {random_number} \n خیلی خوش شانسی")
    elif random_number == 1:
        bot.reply_to(message, f"عدد تاس : {random_number} \n  خیلی بد شانسی")
    else:
        bot.reply_to(message, f"عدد تاس : {random_number}")

    logger.info(f"User {message.chat.first_name} rolled a dice and got {random_number}.") 





@bot.message_handler(func= lambda message : message.text in ["salam" , "hello" , "bonjour"] )
def hello_handler(message) : 
    bot.reply_to(message , f"Hello there {message.chat.first_name} ! ")

    logger.info(f"User {message.chat.first_name} greeted the bot with '{message.text}'.")   
    





bot.infinity_polling()


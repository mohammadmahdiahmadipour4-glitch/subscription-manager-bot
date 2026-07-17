import telebot
import os 
import random 
import logging 
from PIL import Image
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardButton , InlineKeyboardMarkup
from marzban import create_vpn_user  
import sqlite3
from datetime import datetime
API_TOKEN = os.getenv("Telegram_API_token")

logger = telebot.logger
telebot.logger.setLevel(logging.INFO) 

bot = telebot.TeleBot(API_TOKEN)



suppoert_id = 8760766967 
owner_id = 714678394





# تابع ساخت و اتصال به دیتابیس
def init_db():
    conn = sqlite3.connect("shop_database.db", check_same_thread=False)
    cursor = conn.cursor()
    # ساخت جدول برای ذخیره اطلاعات مشتریان
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            username TEXT,
            plan TEXT,
            status TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

# روشن کردن دیتابیس در شروع کار
db_conn, db_cursor = init_db()

# تابع برای ثبت یک سفارش جدید در دیتابیس
def save_order_to_db(user_id, username, plan, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    db_cursor.execute("INSERT INTO orders (user_id, username, plan, status, date) VALUES (?, ?, ?, ?, ?)",
                      (str(user_id), username, str(plan), status, now))
    db_conn.commit()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # if message.text != "/setname":
    #     # bot.send_message(message.chat.id , f"Hi {message.chat.first_name} , how can i help you ?")
    #     # logger.info(f"User {message.chat.first_name} started the bot.")  
    #     pass 
    # else : 
    #     send_msg = bot.send_message(message.chat.id , "Please send me your name!")
    #     bot.register_next_step_handler(send_msg,set_name) 
    markup = ReplyKeyboardMarkup(resize_keyboard=True , row_width=2,  input_field_placeholder="Choose an option")
    btn_shop = KeyboardButton("خرید اشتراک")
    btn_test = KeyboardButton("اکانت تست")
    btn_support = KeyboardButton("پشتیبانی")
    btn_teach = KeyboardButton("اموزش استفاده")
    btn_price = KeyboardButton("تعرفه و قیمت")
    markup.add(btn_shop)
    markup.add(btn_price , btn_test)
    markup.add(btn_support , btn_teach)
    logger.info(f"user {message.chat.first_name} pushed a button")

# display this markup:
    bot.send_message(message.chat.id, 'یک گزینه را انتخاب کنید : ', reply_markup=markup)
        
@bot.message_handler(func= lambda message : message.text in ["تعرفه و قیمت" , "خرید اشتراک" ])
def price_handler(message) :  

    markup = InlineKeyboardMarkup( row_width = 1 ) 
    btn_5g = InlineKeyboardButton(text="5 gigabyte --------> 65T" , callback_data="5gig")
    btn_10g = InlineKeyboardButton(text="10 gigabyte --------> 80T", callback_data="10gig")
    btn_20g = InlineKeyboardButton(text="20 gigabyte --------> 160T" , callback_data="20gig")
    btn_50g = InlineKeyboardButton(text="50 gigabyte --------> 400T" , callback_data="50gig")

    markup.add(btn_5g,btn_10g,btn_20g , btn_50g)

    bot.send_message(message.chat.id , text = "choose one of our services" , reply_markup=markup)


@bot.callback_query_handler(func=lambda call : True)
def reply_shopping_call(call) :
    user_id = call.message.chat.id 
    if call.data == "5gig" : 
        reply_text = "شما  بسته 5 گیگابایت بدون محدودیت زمان و کاربر را انتخاب کردید \n  لطفا بعد از واریز خرید را تایید کنید \n مبلغ : 65 هزار تومان \n شکاره کارت : 5041721121221111"
        markup = InlineKeyboardMarkup()
        btn_confirm = InlineKeyboardButton(text= "تایید واریز" , callback_data="confirmed_5")
        markup.add(btn_confirm) 
        bot.edit_message_text(chat_id=call.message.chat.id  , message_id =call.message.id , text  = reply_text , reply_markup=markup) 

    elif call.data == "10gig" : 
        reply_text = "شما  بسته 10 گیگابایت بدون محدودیت زمان و کاربر را انتخاب کردید \n  لطفا بعد از واریز خرید را تایید کنید \n مبلغ : 80 هزار تومان \n شکاره کارت : 5041721121221111"
        markup = InlineKeyboardMarkup()
        btn_confirm = InlineKeyboardButton(text= "تایید واریز" , callback_data="confirmed_10")
        markup.add(btn_confirm) 
        bot.edit_message_text(chat_id=call.message.chat.id  , message_id =call.message.id , text  = reply_text , reply_markup=markup)  

    elif call.data == "20gig" : 
        reply_text = "شما  بسته 5 گیگابایت بدون محدودیت زمان و کاربر را انتخاب کردید \n  لطفا بعد از واریز خرید را تایید کنید \n مبلغ : 160 هزار تومان \n شکاره کارت : 5041721121221111"
        markup = InlineKeyboardMarkup()
        btn_confirm = InlineKeyboardButton(text= "تایید واریز" , callback_data="confirmed_20")
        markup.add(btn_confirm) 
        bot.edit_message_text(chat_id=call.message.chat.id  , message_id =call.message.id , text  = reply_text , reply_markup=markup)  


    elif call.data == "50gig" : 
        reply_text = "شما  بسته 5 گیگابایت بدون محدودیت زمان و کاربر را انتخاب کردید \n  لطفا بعد از واریز خرید را تایید کنید \n مبلغ : 350 هزار تومان \n شکاره کارت : 5041721121221111"
        markup = InlineKeyboardMarkup()
        btn_confirm = InlineKeyboardButton(text= "تایید واریز" , callback_data="confirmed_50")
        markup.add(btn_confirm) 
        bot.edit_message_text(chat_id=call.message.chat.id  , message_id =call.message.id , text  = reply_text , reply_markup=markup)  
        



    elif call.data.startswith("confirmed_") :
        data_limit = call.data.split("_")[1] 
        first_name = call.message.chat.first_name
        username = call.message.chat.username 
        username_text = f"@{username}" if username else "ندارد"
        admin_text = f"🛒 یک درخواست خرید جدید!\n\n" \
                     f"👤 نام مشتری: {first_name}\n" \
                     f"🌐 آیدی تلگرام: {username_text}\n" \
                     f"🔢 آیدی سیستمی: {user_id}\n" \
                     f"📦 حجم درخواستی: {data_limit} گیگ"
        

        bot.answer_callback_query(call.id , text="your vpn will be sent after we confirm your payment  " , show_alert=True)
        bot.delete_message(chat_id=call.message.chat.id  , message_id =call.message.id , timeout=10  ) 
        markup = InlineKeyboardMarkup(row_width=1)
        btn_confirm_supp = InlineKeyboardButton(text="YES"  , callback_data=f"YES_{user_id}_{data_limit}") 
        btn_denided_supp = InlineKeyboardButton(text="NO" , callback_data=f"NO_{user_id}") 
        markup.add(btn_confirm_supp , btn_denided_supp) 
        bot.send_message(suppoert_id , text= admin_text  , reply_markup=markup)
    elif call.data.startswith("YES_") : 

        customer_id = call.data.split("_")[1]
        data_limit = int(call.data.split("_")[2])
        marzban_result = create_vpn_user(username=customer_id , data_limit_gb= data_limit) 
        success_text = f"خرید شما تایید شد \n لینک ساب شما : {marzban_result}" 
        bot.send_message (chat_id=customer_id , text= success_text) 
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="✅ تایید شد و به کاربر اطلاع داده شد.")
    elif call.data.startswith("NO_") : 
        customer_id = call.data.split("_")[1]

        bot.send_message(customer_id , text="خرید شما لغو شد !  ")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="❌ رد شد و به کاربر اطلاع داده شد.")


@bot.message_handler(func=lambda message : message.text == "اموزش استفاده")
def how_to_use(message) : 
    move_to_channel_text = "برای اموزش استفاده به چنل زیر مراجعه کنید \n  @fastvpn6"
    bot.send_message(chat_id=message.chat.id  , text=move_to_channel_text )

@bot.message_handler(func=lambda message : message.text =="پشتیبانی" )
def connest_supp(message) : 
    text =  "برای ارتباط با پشتیبانی به اکانت زیر پیام دهید \n @Sup_fastvpn"
    bot.send_message(chat_id=message.chat.id , text= text)



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


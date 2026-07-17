import telebot
import os 
import random 
import logging 
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.types import InlineKeyboardButton , InlineKeyboardMarkup
from marzban import create_vpn_user  
import sqlite3
from datetime import datetime
import re
import csv
from flask import Flask
import threading
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
    user_id = message.chat.username
    logger.info(f"New user started the bot | UserID: {user_id}")
    markup = ReplyKeyboardMarkup(resize_keyboard=True , row_width=2,  input_field_placeholder="Choose an option")
    btn_shop = KeyboardButton("خرید اشتراک")
    btn_test = KeyboardButton("اکانت تست")
    btn_support = KeyboardButton("پشتیبانی")
    btn_teach = KeyboardButton("اموزش استفاده")
    btn_price = KeyboardButton("تعرفه و قیمت")
    markup.add(btn_shop)
    markup.add(btn_price , btn_test)
    markup.add(btn_support , btn_teach)
    

    bot.send_message(message.chat.id, 'یک گزینه را انتخاب کنید : ', reply_markup=markup)
        
@bot.message_handler(func= lambda message : message.text in ["تعرفه و قیمت" , "خرید اشتراک" ])
def price_handler(message):  
    markup = InlineKeyboardMarkup( row_width = 1 ) 
    btn_5g = InlineKeyboardButton(text="5 gigabyte --------> 65T" , callback_data="5gig")
    btn_10g = InlineKeyboardButton(text="10 gigabyte --------> 80T", callback_data="10gig")
    btn_20g = InlineKeyboardButton(text="20 gigabyte --------> 160T" , callback_data="20gig")
    btn_50g = InlineKeyboardButton(text="50 gigabyte --------> 400T" , callback_data="50gig")

    markup.add(btn_5g,btn_10g,btn_20g , btn_50g)
    bot.send_message(message.chat.id , text = "choose one of our services" , reply_markup=markup)


@bot.callback_query_handler(func=lambda call : True)
def reply_shopping_call(call):
    user_id = call.message.chat.id 
    
    if call.data == "5gig": 
        reply_text = "شما  بسته 5 گیگابایت بدون محدودیت زمان و کاربر را انتخاب کردید \n لطفا بعد از واریز خرید را تایید کنید \n مبلغ : 65 هزار تومان \n شماره کارت : 5041721121221111"
        markup = InlineKeyboardMarkup()
        btn_confirm = InlineKeyboardButton(text= "تایید واریز" , callback_data="confirmed_5")
        markup.add(btn_confirm) 
        bot.edit_message_text(chat_id=call.message.chat.id  , message_id=call.message.message_id , text=reply_text , reply_markup=markup) 

    elif call.data == "10gig": 
        reply_text = "شما  بسته 10 گیگابایت بدون محدودیت زمان و کاربر را انتخاب کردید \n لطفا بعد از واریز خرید را تایید کنید \n مبلغ : 80 هزار تومان \n شماره کارت : 5041721121221111"
        markup = InlineKeyboardMarkup()
        btn_confirm = InlineKeyboardButton(text= "تایید واریز" , callback_data="confirmed_10")
        markup.add(btn_confirm) 
        bot.edit_message_text(chat_id=call.message.chat.id  , message_id=call.message.message_id , text=reply_text , reply_markup=markup)  

    elif call.data == "20gig": 
        reply_text = "شما  بسته 20 گیگابایت بدون محدودیت زمان و کاربر را انتخاب کردید \n لطفا بعد از واریز خرید را تایید کنید \n مبلغ : 160 هزار تومان \n شماره کارت : 5041721121221111"
        markup = InlineKeyboardMarkup()
        btn_confirm = InlineKeyboardButton(text= "تایید واریز" , callback_data="confirmed_20")
        markup.add(btn_confirm) 
        bot.edit_message_text(chat_id=call.message.chat.id  , message_id=call.message.message_id , text=reply_text , reply_markup=markup)  

    elif call.data == "50gig": 
        reply_text = "شما  بسته 50 گیگابایت بدون محدودیت زمان و کاربر را انتخاب کردید \n لطفا بعد از واریز خرید را تایید کنید \n مبلغ : 350 هزار تومان \n شماره کارت : 5041721121221111"
        markup = InlineKeyboardMarkup()
        btn_confirm = InlineKeyboardButton(text= "تایید واریز" , callback_data="confirmed_50")
        markup.add(btn_confirm) 
        bot.edit_message_text(chat_id=call.message.chat.id  , message_id=call.message.message_id , text=reply_text , reply_markup=markup)  

    elif call.data.startswith("confirmed_"):
        data_limit = call.data.split("_")[1] 
        
        # پیام قبلی را پاک می‌کنیم
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id) 
        
        # از کاربر می‌خواهیم عکس رسید را بفرستد
        msg = bot.send_message(call.message.chat.id, "📸 لطفاً عکس رسید واریز خود را ارسال کنید:")
        
        # ربات را منتظر می‌گذاریم تا پیام بعدی کاربر (که باید عکس باشد) را بگیرد و به تابع جدید بفرستد
        bot.register_next_step_handler(msg, process_receipt_photo, data_limit)


    elif call.data.startswith("YES_"): 
        customer_id = call.data.split("_")[1]
        data_limit = int(call.data.split("_")[2])
        logger.info(f"Admin APPROVED payment | UserID: {customer_id} | Plan: {data_limit}GB")
        # 🔴 کلمه text به caption تغییر کرد
        username_match = re.search(r"آیدی تلگرام:\s*(.+)", call.message.caption)
        extracted_username = username_match.group(1).strip() if username_match else "نامشخص"

        marzban_result = create_vpn_user(username=customer_id , data_limit_gb=data_limit) 
        success_text = f"خرید شما تایید شد \n لینک ساب شما :\n{marzban_result}" 
        bot.send_message(chat_id=customer_id , text=success_text) 
        
        # 🔴 ویرایش کپشن عکس و حذف دکمه‌ها
        new_caption = call.message.caption + "\n\n✅ وضعیت: تایید شد و لینک ارسال گردید."
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=new_caption, reply_markup=None)
        logger.info(f"Premium account created SUCCESSFULLY | UserID: {customer_id} | Plan: {data_limit}GB")
        save_order_to_db(customer_id, extracted_username, f"{data_limit} گیگ", "تایید شده")

    elif call.data.startswith("NO_"): 
        customer_id = call.data.split("_")[1]
        data_limit = call.data.split("_")[2]
        logger.error(f"Premium account creation FAILED | UserID: {customer_id} | Reason: admin deniyed ! ")
        # 🔴 کلمه text به caption تغییر کرد
        username_match = re.search(r"آیدی تلگرام:\s*(.+)", call.message.caption)
        extracted_username = username_match.group(1).strip() if username_match else "نامشخص"

        bot.send_message(customer_id , text="خرید شما لغو شد !  ")
        
        # 🔴 ویرایش کپشن عکس و حذف دکمه‌ها
        new_caption = call.message.caption + "\n\n❌ وضعیت: درخواست توسط ادمین رد شد."
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=new_caption, reply_markup=None)
        
        save_order_to_db(customer_id, extracted_username, f"{data_limit} گیگ", "رد شده")

def process_receipt_photo(message, data_limit):
    # بررسی می‌کنیم که کاربر حتماً عکس فرستاده باشد، نه متن
    if not message.photo:
        msg = bot.send_message(message.chat.id, "❌ لطفاً فقط عکس رسید را ارسال کنید. دوباره تلاش کنید:")
        bot.register_next_step_handler(msg, process_receipt_photo, data_limit)
        return

    # استخراج باکیفیت‌ترین سایزِ عکسی که کاربر فرستاده
    photo_id = message.photo[-1].file_id
    
    user_id = message.chat.id
    first_name = message.from_user.first_name
    username = message.from_user.username 
    username_text = f"@{username}" if username else "ندارد"
    
    # این متن حالا تبدیل می‌شود به کپشنِ زیرِ عکس
    admin_caption = f"🛒 یک درخواست خرید جدید!\n\n" \
                    f"👤 نام مشتری: {first_name}\n" \
                    f"🌐 آیدی تلگرام: {username_text}\n" \
                    f"🔢 آیدی سیستمی: {user_id}\n" \
                    f"📦 حجم درخواستی: {data_limit} گیگ"
    
    # ساخت دکمه‌های تایید و رد برای ادمین
    markup = InlineKeyboardMarkup(row_width=1)
    btn_confirm_supp = InlineKeyboardButton(text="YES", callback_data=f"YES_{user_id}_{data_limit}") 
    btn_denided_supp = InlineKeyboardButton(text="NO", callback_data=f"NO_{user_id}_{data_limit}") 
    markup.add(btn_confirm_supp, btn_denided_supp) 
    
    # 🔴 ارسال عکس + کپشن + دکمه‌ها برای پشتیبانی
    bot.send_photo(chat_id=suppoert_id, photo=photo_id, caption=admin_caption, reply_markup=markup)

    # پیام اطمینان‌بخش به مشتری
    bot.send_message(message.chat.id, "✅ رسید شما دریافت شد و برای ادمین ارسال گردید. لطفاً منتظر تایید باشید.")


@bot.message_handler(func=lambda message: message.text == "اکانت تست")
def test_account(message):
    user_id = message.chat.id 
    test_user = str(user_id) + "test"
    logger.info(f"Test account requested | UserID: {user_id}")
    # پیام انتظار برای کاربر
    bot.send_message(chat_id=message.chat.id, text="⏳ چند لحظه صبر کنید...")
    
    # ساخت اکانت (حالا 0.1 به درستی کار می‌کند)
    new_test_account = create_vpn_user(username=test_user, data_limit_gb=1)
    
    # بررسی اینکه آیا اروری (مثل تکراری بودن) رخ داده یا لینک با موفقیت ساخته شده
    if "❌" in new_test_account:
        logger.error(f"Test account creation FAILED | UserID: {user_id} | Reason: {new_test_account}")
        bot.send_message(chat_id=message.chat.id, text=new_test_account)
    else:
        logger.info(f"Test account created SUCCESSFULLY | UserID: {user_id}")
        sending_test = f"🎁 اکانت تست شما با حجم ۱۰۰ مگابایت:\n\n{new_test_account}" 
        bot.send_message(chat_id=message.chat.id, text=sending_test)













@bot.message_handler(func=lambda message : message.text == "اموزش استفاده")
def how_to_use(message): 
    move_to_channel_text = "برای اموزش استفاده به چنل زیر مراجعه کنید \n  @fastvpn6"
    bot.send_message(chat_id=message.chat.id  , text=move_to_channel_text )

@bot.message_handler(func=lambda message : message.text =="پشتیبانی" )
def connest_supp(message): 
    text =  "برای ارتباط با پشتیبانی به اکانت زیر پیام دهید \n @Sup_fastvpn"
    bot.send_message(chat_id=message.chat.id , text=text)

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



@bot.message_handler(commands=['report'])
def export_database(message):
    # بررسی اینکه فقط ادمین (پشتیبان) بتواند این دستور را اجرا کند
    # متغیر suppoert_id در کدهای شما وجود دارد، آن را اینجا چک می‌کنیم
    if str(message.chat.id) != str(suppoert_id):
        bot.send_message(message.chat.id, "⛔️ شما دسترسی به این بخش را ندارید.")
        return

    # خواندن تمام اطلاعات از دیتابیس
    db_cursor.execute("SELECT * FROM orders")
    records = db_cursor.fetchall()

    if not records:
        bot.send_message(message.chat.id, "📭 دیتابیس هنوز خالی است و هیچ سفارشی ثبت نشده.")
        return

    # ساخت یک فایل CSV (اکسل)
    filename = "customers_report.csv"
    
    # استفاده از utf-8-sig باعث می‌شود زبان فارسی در اکسل به هم نریزد
    with open(filename, mode='w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        # نوشتن ردیف اول (تیتر ستون‌ها)
        writer.writerow(["شناسه خرید", "آیدی عددی تلگرام", "یوزرنیم", "حجم درخواستی", "وضعیت تراکنش", "تاریخ و ساعت"])
        # نوشتن تمام رکوردهای دیتابیس
        writer.writerows(records)

    # ارسال فایل برای ادمین در تلگرام
    with open(filename, 'rb') as doc:
        bot.send_document(
            chat_id=message.chat.id, 
            document=doc, 
            caption=f"📊 گزارش کامل فروش شما آماده است.\nتعداد کل تراکنش‌های ثبت شده: {len(records)}"
        )

    # پاک کردن فایل از روی سرور بعد از ارسال (برای اشغال نشدن فضا)
    if os.path.exists(filename):
        os.remove(filename)

# ترفند ساخت سرور وب برای Render
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running online!"

def run_http_server():
    app.run(host="0.0.0.0", port=8080)

threading.Thread(target=run_http_server).start()





bot.infinity_polling()


import telebot
import subprocess
import sys
from requests import post, Session
import time
import datetime
import psutil
import random
import string
import os
import requests
import sqlite3
from telebot import types
from time import strftime
from keep_alive import keep_alive
admin_diggory = "thanngheo2002" # ví dụ : để user name admin là @diggory347 bỏ dấu @ đi là đc
name_bot = "𝘽𝙊𝙏 𝙎𝙋𝘼𝙈 𝙎𝙈𝙎 - 𝘾𝘼𝙇𝙇"
zalo = "coconcak"
web = "newupdate"
facebook = "https://www.facebook.com/profile.php?id=100068655524402&mibextid=ZbWKwL"
allowed_group_id = -1002179925488
bot=telebot.TeleBot("6748031892:AAFYLvQPnPcL3cOfh-BCzMcfDQF25Bzz1QE") #token bot
print("Bot đã được khởi động thành công")
users_keys = {}
key = ""
auto_spam_active = False
last_sms_time = {}
allowed_users = []
processes = []
ADMIN_ID =  5968619607 # id admin
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()
last_command_time = {}


def check_command_cooldown(user_id, command, cooldown):
    current_time = time.time()
    
    if user_id in last_command_time and current_time - last_command_time[user_id].get(command, 0) < cooldown:
        remaining_time = int(cooldown - (current_time - last_command_time[user_id].get(command, 0)))
        return remaining_time
    else:
        last_command_time.setdefault(user_id, {})[command] = current_time
        return None


# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()

def TimeStamp():
  now = str(datetime.date.today())
  return now


def load_users_from_database():
  cursor.execute('SELECT user_id, expiration_time FROM users')
  rows = cursor.fetchall()
  for row in rows:
    user_id = row[0]
    expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
    if expiration_time > datetime.datetime.now():
      allowed_users.append(user_id)


def save_user_to_database(connection, user_id, expiration_time):
  cursor = connection.cursor()
  cursor.execute(
    '''
        INSERT OR REPLACE INTO users (user_id, expiration_time)
        VALUES (?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S')))
  connection.commit()

@bot.message_handler(commands=['add', 'adduser'])
def add_user(message):
   
  admin_id = message.from_user.id
  if admin_id != ADMIN_ID:
    bot.reply_to(message, 'BẠN KHÔNG CÓ QUYỀN SỬ DỤNG LỆNH NÀY')
    return

  if len(message.text.split()) == 1:
    bot.reply_to(message, 'VUI LÒNG NHẬP ID NGƯỜI DÙNG')
    return

  user_id = int(message.text.split()[1])
  allowed_users.append(user_id)
  expiration_time = datetime.datetime.now() + datetime.timedelta(days=30)
  connection = sqlite3.connect('user_data.db')
  save_user_to_database(connection, user_id, expiration_time)
  connection.close()

  bot.reply_to(
    message,
    f'NGƯỜI DÙNG CÓ ID {user_id} ĐÃ ĐƯỢC THÊM VÀO DANH SÁCH ĐƯỢC PHÉP SỬ DỤNG LỆNH /spamvipspamvip'
  )


load_users_from_database()






def is_key_approved(chat_id, key):
    if chat_id in users_keys:
        user_key, timestamp = users_keys[chat_id]
        if user_key == key:
            current_time = datetime.datetime.now()
            if current_time - timestamp <= datetime.timedelta(hours=2):
                return True
            else:
                del users_keys[chat_id]
    return False

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
   
   
    username = message.from_user.username
    bot.reply_to(message, f'''
┌───⭓ {name_bot}
│» Xin chào @{username}
│» /help : Lệnh trợ giúp
│» /admin : Thông tin admin
│» /spam : Spam SMS.
│» /spamvip : Spam SMS kế hoạch VIP
│» /start : Lệnh khởi đầu
│» Lệnh Cho ADMIN
│» /cpu : Kiểm tra CPU và BỘ NHỚ
│» /add : Thêm người dùng sử dụng spamvip
└───────────⧕
    ''')

@bot.message_handler(commands=['admin'])
def diggory(message):
     
    username = message.from_user.username
    diggory_chat = f'''
┌───⭓ {name_bot}
│» Xin chào @{username}
│» Zalo: {zalo}
│» Website: {web}
│» Telegram: @{admin_diggory}
└──────────────
    '''
    bot.send_message(message.chat.id, diggory_chat)

@bot.message_handler(commands=['cpu'])
def check_system_info(message):
     
    username = message.from_user.username
    diggory_chat = f'''
    ┌───⭓ {name_bot}
    │» Thông Báo Tới : @{username}
    │» Nội Dung: Bạn không có quyền thực hiện lệnh này
    └────────
    '''
    if str(message.from_user.username) != admin_diggory:
        bot.reply_to(message, diggory_chat)
        return

    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent

    message_text = f"🖥 Thông tin hệ thống 🖥\n\n" \
                   f"📊 CPU: {cpu_percent}%\n" \
                   f"🧠 Bộ nhớ: {memory_percent}%"
    bot.reply_to(message, message_text)

@bot.message_handler(commands=['restart'])
def restart(message):
     
    if str(message.from_user.username) != admin_diggory:
        bot.reply_to(message, '🚀 Bạn không có quyền sử dụng lệnh này. 🚀')
        return

    bot.reply_to(message, '🚀 Bot sẽ được khởi động lại trong giây lát... 🚀')
    time.sleep(10)
    python = sys.executable
    os.execl(python, python, *sys.argv)

@bot.message_handler(commands=['stop'])
def stop(message):
     
    if str(message.from_user.username) != admin_diggory:
        bot.reply_to(message, '🚀 Bạn không có quyền sử dụng lệnh này. 🚀')
        return

    bot.reply_to(message, '🚀 Bot sẽ dừng lại trong giây lát... 🚀')
    time.sleep(1)
    bot.stop_polling()

@bot.message_handler(commands=['spam'])
def spam(message):
    if message.chat.id != allowed_group_id:
        bot.send_message(chat_id=message.chat.id, text='Bot chỉ hoạt động trong nhóm này https://t.me/trumspamsms.')
        return
     
    params = message.text.split()
    username = message.from_user.username
    diggory_chat = f'''
┌───⭓ {name_bot}
│» Thông Báo Tới : @{username}
│» Nội Dung: Vui lòng nhập đầy đủ thông tin
└───────
    '''
    
    if len(params) < 2:
        bot.reply_to(message, diggory_chat)
        return

    sdt = params[1]
    chat_id = message.chat.id
    username = message.from_user.username
    diggory_chat3 = f'''
┌───⭓ {name_bot}
│» Thông Báo Tới : @{username}
│» Nội Dung: Spam Thành Công
│» Số Luồng Cho Gói Free Là : [30]
│» Plan : [FREE]
│» Số điện thoại:{sdt}
└─────────────
    '''
    file_path = os.path.join(os.getcwd(), "smsv2.py")
    process = subprocess.Popen(["python", file_path, sdt, "30"])
    processes.append(process)
    bot.send_message(chat_id, diggory_chat3)

@bot.message_handler(commands=['spamvip'])
def supersms(message):
    user_id = message.from_user.id
    if user_id not in allowed_users:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này.')
        return

    if len(message.text.split()) == 1:
        bot.send_message(chat_id=message.chat.id, text="Vui lòng nhập số điện thoại cần spam.")
        return

    phone_number = message.text.split()[1]

    username = message.from_user.username
    diggory_chat4 = f'''
┌───⭓ {name_bot}
│» Thông Báo Tới : @{username}
│» Nội Dung: Spam Thành Công
│» Số Lần Cho Gói VIP Là : [50]
│» Plan : [VIP]
│» Số điện thoại:{phone_number}
└─────────────
    '''
    bot.send_message(message.chat.id, diggory_chat4)
    file_path = os.path.join(os.getcwd(), "1.py")
    process = subprocess.Popen(["python", file_path, phone_number, "120"])
    processes.append(process)

keep_alive()
bot.polling()

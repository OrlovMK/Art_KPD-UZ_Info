import imaplib
import email
import json
import DBInteraction
import email.utils
import time
from aiogram import Bot, Dispatcher, executor, types
import asyncio

Settings = ""

# Зчитуємо файл з налаштуваннями
with open('Settings.json', 'r') as f:
    text = f.read()
    Settings = json.loads(text)
    f.close()

bot = Bot(token=Settings["BOT_TOKEN"], parse_mode=types.ParseMode.HTML)

async def send_message(channel_id: int, text: str):
    await bot.send_message(channel_id, text)

async def bot_alert():

    users = DBInteraction.db_get_all_users(Settings)
    letters = DBInteraction.db_get_all_not_processed_letters(Settings)

    for letter in letters:

        text = "Тема: " + letter[5] + "\n\n" + letter[1]
        text = text.replace('<mailto:support@kpd-uz.com>','')

        for user in users:
            
            if user[3] == True and letter[6] == False:
                await send_message(user[1], text)
            elif letter[6] == True:
                await send_message(user[1], text)  

        DBInteraction.db_letter_processed(letter[0],Settings)

              

def mail_analysis():

    # Встановлюємо з'єднання з сервером пошти та отримуємо вхідні
    mail = imaplib.IMAP4_SSL(Settings["EMAIL_SERVER"])
    mail.login(Settings["Email"], Settings["EMAIL_PASSWORD"])
    mail.select('inbox')

    # Отримуємо список ідентифікаторів повідомлень
    typ, data = mail.search(None, 'ALL')

    # Перебираємо кожне повідомлення за його ідентифікатором
    for num in data[0].split():

        typ, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]

        # Конвертуємо повідомлення в об'єкт email
        email_message = email.message_from_bytes(raw_email)

        '''
        print('Subject:', email_message['Subject'])
        print('From:', email_message['From'])
        print('Body:', email_message.get_payload())
        '''

        tmsoft_letter = False

        from_list = email_message['From'].split()
        for list_elem in from_list: 
            elemFind = list_elem.find("@tmsoft.com.ua")
            if elemFind > 0:
                tmsoft_letter = True
                break


        sent_dateTime = email.utils.parsedate_to_datetime(email_message['Date'])
        sent_date = sent_dateTime.date()
        sent_time = sent_dateTime.time()

        header_letter, encoding = email.header.decode_header(
            email_message['Subject'])[0]
        header_letter = header_letter.decode('utf-8')

        text_letter = str(email_message.get_payload()[0]._payload).encode('utf8', 'surrogateescape').decode('utf8')

        letter = {'date': sent_date,'time': sent_time,'header': header_letter, 'text': text_letter, 'tmsoft_letter':tmsoft_letter}

        # Записуємо в базу лист
        res = DBInteraction.db_interactionin_letter(2, letter, Settings)

        if res == None:
            print(1)

    # Відключаємо з'єднання з сервером пошти
    mail.close()
    mail.logout()
    
async def main():
    while True:
        #mail_analysis()
        await bot_alert()
        time.sleep(600)

if __name__ == '__main__':
    asyncio.run(main())

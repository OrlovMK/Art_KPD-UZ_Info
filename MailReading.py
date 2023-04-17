import imaplib
import email

# Встановлюємо з'єднання з сервером пошти та отримуємо вхідні
mail = imaplib.IMAP4_SSL('mail.artsoft.mk.ua')
mail.login('KPDUZUpdates@artport.pro', 'o9InY7KJA1rw')
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
    # виводимо тему та відправника повідомлення
    print('Subject:', email_message['Subject'])
    print('From:', email_message['From'])
    print('Body:', email_message.get_payload())
    '''
    
    textMail = str(email_message.get_payload()[0]._payload).encode('utf8', 'surrogateescape').decode('utf8')
    print(textMail)
    
    text, encoding = email.header.decode_header(email_message['Subject'])[0]
    text = text.decode('utf-8')
    print(text)
    
    
# Відключаємо з'єднання з сервером пошти
mail.close()
mail.logout()
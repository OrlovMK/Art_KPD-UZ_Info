import psycopg2

''' type: 1 - find; 2 - add; 3 - update; 4 - delete '''
def bot_interactionin_db(type, userID, Settings, userName=""):

    db_connect_params = "dbname='%s' user='%s' host='%s' password='%s'" % (Settings["dbname"], Settings["user"], Settings["host"], Settings["password"])

    result = None

    if type != 1:
        result = bot_interactionin_db(1, userID, Settings)

    if result is not None and type == 2:
        return None

    connect = psycopg2.connect(db_connect_params)
    if type == 1:
        sql = """SELECT name FROM users WHERE telegram_id = %s;"""
    elif type == 2:
        sql = """INSERT INTO users(telegram_id)
         VALUES(%s) RETURNING telegram_id;"""
    elif type == 3:
        sql = """UPDATE users SET name = %s WHERE telegram_id = %s RETURNING name;"""
    elif type == 4:
        sql = """DELETE FROM users WHERE telegram_id = %s RETURNING name;"""
    else:
        return None

    try:
        cursor = connect.cursor()
        if type == 3:
            cursor.execute(sql, (userName, userID))
        else:
            cursor.execute(sql, (userID,))

        result = cursor.fetchone()
        connect.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        result = None
    finally:
        if connect is not None:
            connect.close()

    return result

def show_all_letters():

    result = None

    sql = """SELECT
            emails.id AS id,
            emails.letter_subject AS letter_subject,
            emails.content AS content,
            emails.date_of_receiving AS date_of_receiving,
            emails.sent AS sent,
        FROM
            emails WHERE sent = True """

    try:
        connect = psycopg2.connect(db_connect_params)
        cursor = connect.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        connect.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connect is not None:
            connect.close()

    return result

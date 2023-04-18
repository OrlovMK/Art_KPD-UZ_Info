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
        sql = """INSERT INTO users(name,super_user,telegram_id)
         VALUES(%s,FALSE,%s) RETURNING telegram_id;"""
    elif type == 3:
        sql = """UPDATE users SET name = %s WHERE telegram_id = %s RETURNING telegram_id;"""
    elif type == 4:
        sql = """DELETE FROM users WHERE telegram_id = %s RETURNING name;"""
    else:
        return None

    try:
        cursor = connect.cursor()
        if type == 3 or type == 2:
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

''' type: 1 - find; 2 - add; 3 - update; 4 - delete '''
def db_interactionin_letter(type, letter, Settings):

    db_connect_params = "dbname='%s' user='%s' host='%s' password='%s'" % (Settings["dbname"], Settings["user"], Settings["host"], Settings["password"])

    result = None

    if type != 1:
        result = db_interactionin_letter(1, letter, Settings)

    if result is not None and type == 2:
        return None

    connect = psycopg2.connect(db_connect_params)
    if type == 1:
        sql = """SELECT id FROM letters WHERE date = %s;"""
    elif type == 2:
        sql = """INSERT INTO letters(date,time,header,text,sent_status,tmsoft_letter)
         VALUES(%s,%s,%s,%s,FALSE,%s) RETURNING id;"""
    elif type == 3:
        '''sql = """UPDATE users SET name = %s WHERE telegram_id = %s RETURNING name;"""'''
    elif type == 4:
        '''sql = """DELETE FROM users WHERE telegram_id = %s RETURNING name;"""'''
    else:
        return None

    try:
        cursor = connect.cursor()
        if type == 2:
            cursor.execute(sql, (letter["date"],letter["time"],letter["header"],letter["text"],letter["tmsoft_letter"],))
        elif type == 3:
            '''cursor.execute(sql, (userName, userID))'''
        else:
            cursor.execute(sql, (letter["date"],))

        result = cursor.fetchone()
        connect.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        result = None
    finally:
        if connect is not None:
            connect.close()

    return result

def db_get_all_not_processed_letters(Settings):

    db_connect_params = "dbname='%s' user='%s' host='%s' password='%s'" % (Settings["dbname"], Settings["user"], Settings["host"], Settings["password"])

    result = None

    sql = """SELECT
            letters.id AS id,
            letters.text AS text,
            letters.date AS date,
            letters.time AS time,
            letters.sent_status AS sent_status,
            letters.header AS header,
            letters.tmsoft_letter AS tmsoft_letter
        FROM
            letters WHERE sent_status = FALSE """

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

def db_get_all_users(Settings):

    db_connect_params = "dbname='%s' user='%s' host='%s' password='%s'" % (Settings["dbname"], Settings["user"], Settings["host"], Settings["password"])

    result = None

    sql = """SELECT * From users"""

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

def db_letter_processed(id, Settings):

    db_connect_params = "dbname='%s' user='%s' host='%s' password='%s'" % (Settings["dbname"], Settings["user"], Settings["host"], Settings["password"])

    connect = psycopg2.connect(db_connect_params)

    sql = """UPDATE letters SET sent_status = True WHERE id = %s RETURNING id;"""

    try:
        cursor = connect.cursor()
        cursor.execute(sql, (id))
        connect.commit()
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        result = None
    finally:
        if connect is not None:
            connect.close()

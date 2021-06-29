from util.db.create_db_pool import db_pool


def execute(sql):
    conn = db_pool.get_connection()
    conn.start_transaction()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    return


def query(sql):
    conn = db_pool.get_connection()
    conn.start_transaction()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    return result


def insert(tb, dt):
    conn = db_pool.get_connection()
    conn.start_transaction()
    cursor = conn.cursor(dictionary=True)
    ls = [(k, dt[k]) for k in dt if dt[k] is not None]
    sql = 'INSERT INTO `%s` (' % tb + ','.join(i[0] for i in ls) + \
          ') VALUES (' + ','.join('%r' % i[1] for i in ls) + ');'
    try:
        cursor.execute(sql)
    except Exception as e:
        print(sql)
        print('DBErr:' + str(e))
    conn.commit()
    conn.close()
    return


def insert_many(tb, _field, _list):
    conn = db_pool.get_connection()
    conn.start_transaction()
    cursor = conn.cursor(dictionary=True)
    ls = [k for k in _field]
    sql = 'INSERT INTO `%s` (' % tb + ','.join(i for i in ls) + \
          ') VALUES (' + ','.join('%s' for i in ls) + ');'
    try:
        cursor.executemany(sql, _list)
    except Exception as e:
        print(sql)
        print('DBErr:' + str(e))
    conn.commit()
    conn.close()
    return


def update(table, dt_update, dt_condition):
    conn = db_pool.get_connection()
    conn.start_transaction()
    cursor = conn.cursor(dictionary=True)
    sql = 'UPDATE %s SET ' % table + ','.join('%s=%r' % (k, dt_update[k]) for k in dt_update) \
          + ' WHERE ' + ' AND '.join('%s=%r' % (k, dt_condition[k]) for k in dt_condition) + ';'
    try:
        cursor.execute(sql)
    except Exception as e:
        print(sql)
        print(str(e))
    conn.commit()
    conn.close()
    return

import pymysql


if __name__=="__main__":
    connection = pymysql.connect(host='localhost',
                                port=3306,
                                user='root',
                                password='ysy990821',
                                db='baidunews',
                                charset='utf8')
    cursor = connection.cursor()

    effect_row=cursor.execute('''
        CREATE TABLE news(
        title varchar(32),
        date_time varchar(32),
        platform varchar(32),
        body MEDIUMTEXT);
    ''')
    print("finish")
    cursor.close()
    connection.commit()
    connection.close()
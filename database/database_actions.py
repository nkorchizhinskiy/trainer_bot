from typing import Literal
import psycopg2


connection = psycopg2.connect(
        database="trainer_bot",
        user="korchizhinskiy",
        password="ltvbl2002",
        host="127.0.0.1",
        port="5433")

def add_user(connection, user_id: int, user_name: str) -> None | bool:
    """Add user info into database. If user in database - return True"""
    cursor = connection.cursor()
    in_database = check_user(cursor, user_id)
    if not in_database:
        cursor.execute(
                    f'''
                    INSERT INTO users (user_id, user_name)
                    VALUES ({user_id}, '{user_name}');
                    '''
                )
        connection.commit()  
    else:
        return True



def check_user(cursor, user_id: int) -> bool:
    """Check info about user in database"""
    cursor.execute(
            '''
            SELECT (user_id) from users;
            '''
            )
    users = cursor.fetchall()
    users_list = [user[0] for user in users]

    if user_id in users_list:
        return True
    else: 
        return False

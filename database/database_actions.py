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


def check_user(cursor, user_id: int) -> None | bool:
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


def add_exercise_in_list(connection, exercise_name: str, exercise_description: str) -> None:
    """Add exercise into database list"""
    cursor = connection.cursor()
    cursor.execute(
                f'''
                INSERT INTO exercises (exercise_name, exercise_description)
                VALUES ('{exercise_name}', '{exercise_description}')
                '''
            )
    connection.commit()  


def delete_exercise_from_list(connection, exercise_name: str):
    """Delete exercise info in database list"""
    cursor = connection.cursor()
    cursor.execute(
                f'''
                DELETE FROM exercises
                WHERE exercise_name = '{exercise_name}';
                '''
            )
    connection.commit()  


def change_exercise_info(connection, exercise_name: str, new_information: str, changeable_info: str) -> None:
    """Change exercise info in database."""
    cursor = connection.cursor()
    if changeable_info == "name":
        cursor.execute(
                    f'''
                    UPDATE exercises
                    SET exercise_name = '{new_information}'
                    WHERE exercise_name = '{exercise_name}';
                    '''
                )
    else:
        cursor.execute(
                    f'''
                    UPDATE exercises
                    SET exercise_description = '{new_information}'
                    WHERE exercise_name = '{exercise_name}'; 
                    '''
                )
    connection.commit()
    

def print_exercise_list(connection) -> list[str]:
    """Print all exercises in message."""
    cursor = connection.cursor()
    cursor.execute(
                f'''
                SELECT exercise_name, exercise_description
                FROM exercises
                ORDER BY id;
                '''
            )
    exercises = cursor.fetchall()
    exercise_names = [exercise[0] for exercise in exercises]
    connection.commit()
    return exercise_names


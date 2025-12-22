import os
import psycopg2
from psycopg2 import Error
from fastapi import FastAPI, Query, HTTPException
import uvicorn

app = FastAPI()

def execute_query_get(query, params=None):
    try:
        # Подключение
        connection = psycopg2.connect(user=os.getenv("DB_USER", "postgres"),
                                      password=os.getenv("DB_PASS"),
                                      host=os.getenv("DB_HOST", "db"),
                                      port=os.getenv("DB_PORT", "5432"),
                                      database=os.getenv("DB_NAME", "postgres"))

        cursor = connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        raise HTTPException(status_code=400, detail={"Ошибка при работе с PostgreSQL": str(error)})
    finally:
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def execute_query_post(query, params=None):
    try:
        # Подключение
        connection = psycopg2.connect(user=os.getenv("DB_USER", "postgres"),
                                      password=os.getenv("DB_PASS"),
                                      host=os.getenv("DB_HOST", "db"),
                                      port=os.getenv("DB_PORT", "5432"),
                                      database=os.getenv("DB_NAME", "postgres"))

        cursor = connection.cursor()
        cursor.execute(query, params)
        rowcount = cursor.rowcount
        return {"Success": True, "RowCount": rowcount}

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
        raise HTTPException(status_code=400, detail={"Ошибка при работе с PostgreSQL": str(error)})
    finally:
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


#=============================================================================================
#1. Создать студента
#=============================================================================================
@app.post('/create_student', tags=['Студенты'], summary='Создать студента')
def create_student(student_id: int = Query(None), fio: str = Query(), email: str = Query()):
    if student_id is None:
        return execute_query_post('''   
                            INSERT INTO students (fio, email)
                            VALUES (%s, %s)''',
        (fio, email))
    else:
        return execute_query_post('''   
                            INSERT INTO students (student_id, fio, email)
                            VALUES (%s, %s, %s)''',
        (student_id, fio, email))

#=============================================================================================
#2. Создать группу
#=============================================================================================
@app.post('/create_group',  tags=['Группы'], summary='Создать группу')
def create_group(group_id: int = Query(None), group_name: str = Query()):
    if group_id is None:
        return execute_query_post('''   
                            INSERT INTO groups (group_name)
                            VALUES (%s)''',
        (group_name,))
    else:
        return execute_query_post('''   
                            INSERT INTO groups (group_id, group_name)
                            VALUES (%s, %s)''',
        (group_id, group_name))

#=============================================================================================
#3. Получить информацию о студенте по его id
#=============================================================================================
@app.get('/student',  tags=['Студенты'], summary='Получить инфо студента по student_id')
def get_student_info(student_id: int = Query()):
    return execute_query_get('''   
                                SELECT * FROM students
                                WHERE student_id = %s''',
        (student_id,))

#=============================================================================================
#4. Получить информацию о группе по её id
#=============================================================================================
@app.get('/group', tags=['Группы'], summary='Получить инфо группы по group_id')
def get_group_info(group_id: int = Query()):
    return execute_query_get('''   
                                SELECT * FROM groups
                                WHERE group_id = %s''',
        (group_id,))

#=============================================================================================
#5. Удалить студента
#=============================================================================================
@app.post('/delete_student', tags=['Студенты'], summary='Удалить студента по student_id')
def delete_student(student_id: int = Query()):
    return execute_query_post('''   
                        DELETE FROM students
                        WHERE student_id = %s''',
    (student_id,))

#=============================================================================================
#6. Удалить группу
#=============================================================================================
@app.post('/delete_group', tags=['Группы'], summary='Удалить группу по group_id')
def delete_group(group_id: int = Query()):
    return execute_query_post('''   
                        DELETE FROM groups
                        WHERE group_id = %s''',
    (group_id,))

#=============================================================================================
#7. Получить cписок студентов
#=============================================================================================
@app.get('/student_list',  tags=['Студенты'], summary='Получить список студентов')
def get_student_list():
    return execute_query_get('''   
                                SELECT * FROM students''',
        )

#=============================================================================================
#8. Получить список групп
#=============================================================================================
@app.get('/group_list',  tags=['Группы'], summary='Получить список групп')
def get_group_list():
    return execute_query_get('''   
                                SELECT * FROM groups''',
        )

#=============================================================================================
#9. Добавить студента в группу
#=============================================================================================
@app.post('/set_student_group', tags=['Студенты'], summary='Добавить студента в группу')
def set_student_group(student_id: int = Query(), group_id: int = Query()):
    return execute_query_post('''   
                        INSERT INTO student_group (student_id, group_id)
                        VALUES (%s, %s)''',
    (student_id, group_id))

#=============================================================================================
#10. Удалить студента из группы
#=============================================================================================
@app.post('/delete_student_group', tags=['Студенты'], summary='Удалить студента из группы')
def delete_student_group(student_id: int = Query(), group_id: int = Query()):
    return execute_query_post('''   
                        DELETE FROM student_group
                        WHERE ((student_id = %s) AND (group_id = %s))''',
    (student_id, group_id))

#=============================================================================================
#11. Получить всех студентов в группе
#=============================================================================================
@app.get('/student_group_list', tags=['Студенты'], summary='Получить всех студентов в группе')
def student_group_list(group_id: int = Query()):
    return execute_query_get('''   
                        SELECT * FROM students
                        WHERE student_id IN (SELECT student_id FROM student_group
                                WHERE group_id = %s)''',
    (group_id,))

#=============================================================================================
#12. Перевести студента из группы A в группу B
#=============================================================================================
@app.post('/student_change_team', tags=['Студенты'], summary='Перевести студента из группы A в группу B ')
def student_change_team(student_id: int = Query(), group_id_A: int = Query(), group_id_B: int = Query()):
    return execute_query_post('''   
                        UPDATE student_group 
                        SET group_id = %s
                        WHERE student_id = %s AND group_id = %s''',
    (group_id_B, student_id, group_id_A))





if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
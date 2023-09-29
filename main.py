import psycopg2

# удаление таблиц
def drop_db(conn):
    cur = conn.cursor()
    cur.execute("""
        DROP TABLE Clients CASCADE;
    """)

# создание таблиц
def create_db(conn):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Clients(
            Clients_id INTEGER UNIQUE PRIMARY KEY,
            first_name VARCHAR(40),
            last_name VARCHAR(40),
            email VARCHAR(40)
    );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Phone_Clients(
            id SERIAL PRIMARY KEY,
            Clients_id INTEGER NOT NULL REFERENCES Clients(Clients_id),
            phone_number VARCHAR(12) UNIQUE
    );
    """)
    conn.commit()

# наполнение таблиц
def add_client(conn, Clients_id, first_name, last_name, email, phone_number=None):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Clients (Clients_id, first_name, last_name, email) VALUES (%s, %s, %s, %s);
        """, (Clients_id, first_name, last_name, email))
    conn.commit()
    cur.execute("""
        SELECT * FROM Clients;
        """)
    print(cur.fetchall())

    cur.execute("""
        INSERT INTO Phone_Clients (Clients_id, phone_number) VALUES (%s, %s);
        """, (Clients_id, phone_number))
    conn.commit()
    cur.execute("""
        SELECT * FROM Phone_Clients;
        """)
    print(cur.fetchall())

def add_phone(conn, Clients_id, phone_number):  # добавление телефона существующему клиенту
    cur = conn.cursor()
    cur.execute("""
        UPDATE Phone_Clients SET phone_number=%s WHERE Clients_id=%s;
        """, (phone_number, Clients_id))
    conn.commit()

# изменение данных
def change_client(conn, Clients_id, first_name=None, last_name=None, email=None, phone_number=None):
    cur = conn.cursor()
    if first_name != None:
        cur.execute("""
            UPDATE Clients SET first_name=%s WHERE Clients_id=%s;
            """, (first_name, Clients_id))
        cur.execute("""
            SELECT * FROM Clients;
            """)
    print(cur.fetchall())
    if last_name != None:
        cur.execute("""
            UPDATE Clients SET last_name=%s WHERE Clients_id=%s;
            """, (last_name, Clients_id))
        cur.execute("""
            SELECT * FROM Clients;
            """)
    print(cur.fetchall())
    if email != None:
        cur.execute("""
            UPDATE Clients SET email=%s WHERE Clients_id=%s;
            """, (email, Clients_id))
        cur.execute("""
            SELECT * FROM Clients;
            """)
    print(cur.fetchall())
    cur.execute("""
        UPDATE Phone_Clients SET phone_number=%s WHERE Clients_id=%s;
        """, (phone_number, Clients_id))
    cur.execute("""
            SELECT * FROM Phone_Clients;
            """)
    print(cur.fetchall())

# Удаление телефона у клиента
def delete_phone(conn, Clients_id):
    cur = conn.cursor()
    cur.execute("""
        UPDATE Phone_Clients SET phone_number=%s WHERE Clients_id=%s;
        """, ('Null', Clients_id))
    cur.execute("""
        SELECT * FROM Phone_Clients;
        """)
    print(cur.fetchall())

# удаление клиента
def delete_client(conn, Clients_id):
    # сначала удаляем клиента из таблицы с телефонами
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Phone_Clients WHERE Clients_id=%s;
        """, (Clients_id,))
    cur.execute("""
        SELECT * FROM Phone_Clients;
        """)
    print(cur.fetchall())

    # теперь удаляем самого клиента
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM Clients WHERE Clients_id=%s;
        """, (Clients_id,))
    cur.execute("""
        SELECT * FROM Clients;
        """)
    print(cur.fetchall())


# поиск клиента
def find_client(conn, first_name=None, last_name=None, email=None, phone_number=None):
    cur = conn.cursor()
    cur.execute("""
    SELECT c.Clients_id, first_name, last_name, email, phone_number FROM Clients c JOIN Phone_Clients p ON c.Clients_id = p.Clients_id
    WHERE (first_name = %(first_name)s OR %(first_name)s IS NULL)
        AND (last_name = %(last_name)s OR %(last_name)s IS NULL)
        AND (email = %(email)s OR %(email)s IS NULL)
        AND (phone_number = %(phone_number)s OR %(phone_number)s IS NULL);
    """, {"first_name": first_name, "last_name": last_name, "email": email, "phone_number": phone_number})
    print(cur.fetchall())

if __name__ == '__main__':
    with psycopg2.connect(database='post_f_pyth_db', user='postgres', password=open("password.md").read()) as conn:
        create_db(conn)
        add_client(conn, 1, 'Иван', 'Иванов', 'i.ivanov@i.ru', '+79031111111')
        add_client(conn, 2, 'Петр', 'Петров', 'p.petrov@i.ru', '+79032222222')
        add_client(conn, 3, 'Максим', 'Сидоров', 'm.sidorov@i.com')
        add_client(conn, 4, 'Яков', 'Яковлев', 'ya.yakovlev@i.ru')
        add_client(conn, 5, 'Степан', 'Степанов', 's.stepanov@i.ru', '+79033333333')
        add_phone(conn, 2, '+79034444444')
        add_phone(conn, 4, '+79035555555')
        change_client(conn, 1, 'Матвей')
        change_client(conn, 4, 'Костя', 'Костяков')
        change_client(conn, 1, '790399999')
        delete_phone(conn, 1)
        delete_client(conn, 4)
        find_client(conn, first_name='Петр')
        find_client(conn, last_name='Яковлев')
        find_client(conn, first_name='Степан', last_name='Степанов', email='s.stepanov@i.ru', phone_number='+79033333333')
        find_client(conn, phone_number='+79032222222')

conn.close()
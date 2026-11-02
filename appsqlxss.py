from flask import Flask, request
import sqlite3
app=Flask(__name__)
DATABASE="user.db"
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        count=conn.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0]
        if count==0:
            conn.executemany(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                [
                    ("alex", "alex@example.com"),
                    ("maria", "maria@example.com"),
                    ("ivan", "ivan@example.com"),
                ],
            )
@app.route("/")
def index():
    with sqlite3.connect(DATABASE) as conn:
        users=conn.execute(
            "SELECT id, username, email FROM users"
        ).fetchall()
    html="""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Учебная система пользователя</title>
    </head>
    <body>
        <h1>Список пользователей</h1>
        <p><a href="/add_user">Регистрация</a></p>
        <form action="/search" method="get">
            <label for="q">Имя пользователя:</label>
            <input id="q" name="q" type="text">
            <button type="submit">Найти</button>
        </form>
        <ul>
    """
    for user in users:
        html+=f"<li>{user[1]}-{user[2]}</li>"
    html+="""
        </ul>
    </body>
    </html>
    """
    return html
@app.route("/search")
def search():
    query=request.args.get("q","")
    sql=(
        "SELECT id, username, email FROM users "
        f"WHERE username='{query}'"
    )
    with sqlite3.connect(DATABASE) as conn:
        users=conn.execute(sql).fetchall()
    result="<h1>Результаты поиска</h1><ul>"
    for user in users:
        result+=f"<li>{user[1]}-{user[2]}</li>"
    result+="</ul><a href='/'>На главную</a>"
    return result
@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method=="POST":
        username=request.form.get("username","")
        email=request.form.get("email","")
        with sqlite3.connect(DATABASE) as conn:
            conn.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                (username, email)
            )
        return "<h1>Пользователь добавлен!</h1><a href='/'>На главную</a>"
    return """
    <h1>Добавление пользователя</h1>
    <form method="POST">
        <p>Имя: <input name="username"></p>
        <p>Email: <input name="email"></p>
        <button type="submit">Добавить</button>
    </form>
    <a href="/">На главную</a>
    """
if __name__=="__main__":
    init_db()
    app.run(debug=True)
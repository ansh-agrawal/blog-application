from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.config['SECRET_KEY'] = ""
app.config['MYSQL_DB'] = "ansh"
app.config['MYSQL_PASSWORD'] = "@nsh"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
mysql = MySQL(app)


@app.route('/')
def index():
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn.execute('SELECT * FROM posts ORDER BY id DESC')
    post = conn.fetchall()
    return render_template('index.html', post=post)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        title = request.form['title']
        message = request.form['message']
        conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        conn.execute('INSERT INTO posts VALUES(NULL, %s, %s)', (title, message))
        conn.connection.commit()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/<int:post_id>')
def post(post_id):
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn.execute("SELECT id, title, message FROM posts WHERE id = %s", (post_id,))
    detailed_post = conn.fetchone()
    return render_template("detailed_post.html", detailed_post=detailed_post)


@app.route('/<int:post_id>/edit', methods=['GET', 'POST'])
def edit(post_id):
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn.execute("SELECT title, message FROM posts WHERE id = %s", (post_id,))
    old_data = conn.fetchone()

    if request.method == "POST":
        title = request.form['title']
        message = request.form['message']
        conn.execute("UPDATE posts SET title = %s, message = %s", (title, message))
        conn.connection.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template("edit.html", old_data=old_data)


@app.route('/<int:post_id>/delete')
def delete(post_id):
    conn = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    conn.execute("DELETE FROM posts WHERE id = %s", (post_id,))
    conn.connection.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

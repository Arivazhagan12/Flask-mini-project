from flask import Flask, render_template, redirect, request, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
# mysql connection
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Arivu@1994"
app.config["MYSQL_DB"] = "crud"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


# Loding Home page
@app.route("/")
def home():
    con = mysql.connection.cursor()
    sql = "select * from users"
    con.execute(sql)
    res = con.fetchall()

    return render_template("index.html", datas=res)


# New user
@app.route("/addUsers", methods=['GET', 'POST'])
def addusers():
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        age = request.form['age']
        con = mysql.connection.cursor()
        sql = "insert into users(NAME,CITY,AGE) value (%s,%s,%s)"
        con.execute(sql, [name, city, age])
        mysql.connection.commit()
        con.close()
        flash('User details added')
        return redirect(url_for("home"))

    return render_template("addusers.html")


# Update users
@app.route("/edituser/<string:id>", methods=['GET', 'POST'])
def edituser(id):
    con = mysql.connection.cursor()

    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        age = request.form['age']
        sql = "Update users set NAME=%s,CITY=%s,AGE=%s where ID=%s"
        con.execute(sql, [name, city, age, id])
        mysql.connection.commit()
        con.close()
        flash('User details updated')
        return redirect(url_for("home"))

        con = mysql.connection.cursor()

    sql = "select * from users where ID=%s"
    con.execute(sql, [id])
    res = con.fetchone()
    return render_template("edituser.html", datas=res)


# Delete Users
@app.route("/deleteuser/<string:id>", methods=['GET', 'POST'])
def deleteuser(id):
    con = mysql.connection.cursor()
    sql = "delete from users where ID=%s"
    con.execute(sql,id)
    mysql.connection.commit()
    con.close()
    flash('User details deleted')

    return redirect(url_for("home"))


if __name__ == '__main__':
    app.secret_key = "abc123"
    app.run(debug=True)

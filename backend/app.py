from flask import Flask, render_template, request, redirect, flash
import MySQLdb
from contextlib import closing
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='../frontend/static',
                      template_folder='../frontend/templates')
app.secret_key = os.getenv("SECRET_KEY")

def get_db_connection():
    return MySQLdb.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        passwd=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME")
    )

def validar_email(email):
    email_formato = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_formato, email)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        if not validar_email(email):
            flash("Email inválido!", "error")
            return redirect("/login")

        with closing(get_db_connection()) as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha = %s",
            (email, senha))
            user = cursor.fetchone()

        if user:
            return redirect("/")
        else:
            flash("Login falhou! Verifique seu email e senha.", "error")
            return redirect("/login")
        
    return render_template("login.html")

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form("nome")
        email = request.form("email")
        senha = request.form("senha")

        if not validar_email(email):
            flash("Email inválido!", "error")
            return redirect("/cadastro")

        with closing(get_db_connection()) as db: 
            cursor = db.cursor()
            try:
                cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, senha))
                db.commit()
                flash("Cadastro realizado com sucesso! Faça login.", "sucesso")
            except MySQLdb.Error as e:
                flash("Erro ao cadastrar usuário: {}".format(e), "error")
                return redirect("/cadastro")
    

        return redirect("/login")
    
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
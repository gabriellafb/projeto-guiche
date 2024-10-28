from flask import Flask, render_template, request, redirect, flash, session
import pymysql
from contextlib import closing
import re
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__, static_folder='../frontend/static',
                      template_folder='../frontend/templates')
app.secret_key = os.getenv("SECRET_KEY")

def get_db_connection():
    return pymysql.connect(
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
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()

        if user and check_password_hash(user[3], senha):
            session['usuario'] = user[0]
            return redirect("/servicos")
        else:
            flash("Login falhou! Verifique seu email e senha.", "error")
            return redirect("/login")
        
    return render_template("login.html")

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        if not validar_email(email):
            flash("Email inválido!", "error")
            return redirect("/cadastro")

        if len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "error")
            return redirect("/cadastro")

        with closing(get_db_connection()) as db: 
            cursor = db.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            if cursor.fetchone():
                flash("Email já cadastrado!", "error")
                return redirect("/cadastro")

            hashed_password = generate_password_hash(senha)

            try:
                cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (nome, email, hashed_password))
                db.commit()
                flash("Cadastro realizado com sucesso! Faça login.", "sucesso")
            except pymysql.Error as e:
                flash("Erro ao cadastrar usuário: {}".format(e), "error")
                return redirect("/cadastro")
    
        return redirect("/login")
    
    return render_template('cadastro.html')

@app.route('/servicos')
def servicos():
    if 'usuario' not in session:
        flash("Você precisa estar logado para acessar esta página.", "error")
        return redirect("/login")
    
    return render_template('servicos.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash("Você foi desconectado com sucesso.", "sucesso")
    return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, url_for

app = Flask(__name__, static_folder='../frontend/static',
                      template_folder='../frontend/templates')

# Rota principal para renderizar o index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)
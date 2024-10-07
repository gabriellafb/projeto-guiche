from flask import Flask, render_template

app = Flask(__name__, static_folder='../frontend/static',
                      template_folder='../frontend/templates')

# Rota principal para renderizar o index.html
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
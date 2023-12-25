from flask import render_template
from app import create_app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html', context={})

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5001)

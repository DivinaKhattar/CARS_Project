from app import create_app
def create_app():
    app = Flask(__name__)
app = create_app()

@app.route('/')
def home():
    return "Hello, Flask on Vercel!"

if __name__ == '__main__':
    app.run(debug=True)

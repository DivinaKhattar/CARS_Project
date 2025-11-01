from app import create_app
app = create_app()

@app.route('/')
def home():
    return "Hello, Flask is running successfully on Render!"

if __name__ == "__main__":
    app.run()

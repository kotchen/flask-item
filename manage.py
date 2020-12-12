from flaskr import create_app

app = create_app()

if __name__ == '__main__':
    app.run("127.0.0.2",5000,debug=True)
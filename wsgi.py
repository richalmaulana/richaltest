from application import app

#app = create_app()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4567, debug=True)

from website import create_app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
    #debug=True  to enable debugging mode in flask

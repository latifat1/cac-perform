from src import create_app

_ = create_app()

app = _[0]
mode = _[1]

if __name__=='__main__':
    if mode == "prod":
        print('Server de production lancée')
        app.run()
    else:
        print('Server de développement lancée')
        app.run()
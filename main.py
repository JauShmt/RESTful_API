from sukurepa import create_app


app = create_app()
app.app_context().push()
app.config["DEBUG"] = True


if __name__ == '__main__': #prevents web server starting without running sukurepa.py (e.g: can't import it and run it from another file)
    app.run()
from TheHunt import create_app


def main():
    app = create_app()
    app.config.from_object('TheHunt.config.Debug')
    app.run()


if __name__ == '__main__':
    main()

from TheHunt import create_app
import click


@click.command()
@click.option("--config", help="Config path", default="Debug")
def main(config):
    app = create_app()
    app.config.from_object(f"TheHunt.config.{ config }")
    app.run()

if __name__ == '__main__':
    main()

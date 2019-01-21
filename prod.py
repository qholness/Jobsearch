import TheHunt
import waitress
import logging


app = TheHunt.create_app()
app.config.from_object('TheHunt.config.Production')


waitress.serve(app, host='192.168.1.110', port=8082)

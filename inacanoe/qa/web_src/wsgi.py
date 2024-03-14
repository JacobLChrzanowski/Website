# from docker.docker_flaskapp_prod.src.routes import app
from web_src.app import app

if __name__ == "__main__":
    app.run(debug=False)
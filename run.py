# run.py

import os

from app import create_app

env_config = os.getenv('FLASK_ENV')
app = create_app(env_config)


if __name__ == '__main__':
    app.run()
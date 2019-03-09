import os
import uuid

from flask import Flask
from flask_restplus import Api
from controllers.books import books as books
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, root_path=ROOT_DIR)
app.config['SECRET_KEY'] = str(uuid.uuid4())
api = Api(app, doc='/swagger/')
api.add_namespace(books)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

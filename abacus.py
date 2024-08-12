from app import app, db, connex_app
from app.models import Dimension

# app = create_app()
# app = app.app

# @app.shell_context_processor
# def make_shell_context():
#     return {'db': db, 'Dimension': Dimension}

if __name__ == '__main__':
    connex_app.run(port=5001, host='0.0.0.0')


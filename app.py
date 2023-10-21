import os
from src import init_app

# Configuranndo o app
app = init_app()


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5001))

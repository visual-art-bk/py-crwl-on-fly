import os
from core import create_app
from dotenv import load_dotenv

load_dotenv()

app = create_app()


if __name__ == "__main__":

    # DYNAMIC PORT
    # - Hero PORT   - 5000, THE DEFAULT
    # - Fly.io PORT - 8080, SEE ./fly.toml CHECK [env] - PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

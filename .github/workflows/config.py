import os

def load_config():
    return {
        "BOOKS_CSV_PATH": os.environ.get("BOOKS_CSV_PATH", "assets/books.csv"),
        "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
        "PORT": int(os.environ.get("PORT", 5000)),
        "HOST": os.environ.get("HOST", "0.0.0.0"),
    }

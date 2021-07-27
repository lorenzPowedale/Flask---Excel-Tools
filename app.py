import sys

from flask_thread import FlaskThread
import webview


# creates a Thread with the Flask Application running in the background
# in the main Thread it starts the Browser Window
if __name__ == "__main__":
    flask_thread = FlaskThread()
    flask_thread.start()

    webview.create_window('Excel Tools', "http://127.0.0.1:5000", width=1080, height=720)
    sys.exit(1)

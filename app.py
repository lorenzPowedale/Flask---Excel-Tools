from flask_thread import FlaskThread
import webview
from time import sleep

if __name__ == "__main__":
    flask_thread = FlaskThread()
    flask_thread.start()

    sleep(1)

    webview.create_window('New hunt', "http://127.0.0.1:5000", width=1080, height=720)
    done = webview.start()

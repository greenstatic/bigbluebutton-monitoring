from datetime import datetime

from flask import Flask, jsonify, send_from_directory
import settings
import views

app = Flask(__name__, static_url_path='')


@app.route('/about')
def about():
    return jsonify({"name": "bigbluebutton-monitoring",
                    "version": settings.VERSION,
                    "datetime": datetime.now().isoformat(),
                    "source": "https://gitlab.fri.uni-lj.si/greenstatic/bigbluebutton-monitoring"})


@app.route('/')
def root():
    return send_from_directory('frontend', "index.html")


@app.route('/frontend/<path:filename>')
def frontend_static_files(filename):
    return send_from_directory('frontend', filename)


@app.route('/api/server')
def api_server():
    return jsonify(views.get_server())


@app.route('/api/meetings')
def api_meetings():
    return jsonify(views.get_meetings())


if __name__ == '__main__':
    app.run(host="0.0.0.0")

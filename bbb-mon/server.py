from flask import Flask, jsonify, send_from_directory
import views

app = Flask(__name__, static_url_path='')


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

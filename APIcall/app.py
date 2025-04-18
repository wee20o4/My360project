from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/image')
def serve_image():
    return send_from_directory('.', 'image.png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template, request, jsonify
import subprocess
import os
import threading
from werkzeug.utils import secure_filename

app = Flask(__name__)

# دایرەکتۆری بۆتەکان
BOTS_DIR = os.path.join(os.path.dirname(__file__), 'bots')
os.makedirs(BOTS_DIR, exist_ok=True)

# بۆتە چالاکەکان
active_bots = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_bot():
    if 'bot_file' not in request.files:
        return jsonify({'error': 'هیچ فایلێک نەنێردراوە'}), 400
    
    bot_file = request.files['bot_file']
    bot_token = request.form.get('bot_token')
    
    if bot_file.filename == '':
        return jsonify({'error': 'هیچ فایلێک دیاری نەکراوە'}), 400
    
    if not bot_token:
        return jsonify({'error': 'تووکنی بۆت دیاری نەکراوە'}), 400
    
    # پاراستنی فایل
    filename = secure_filename(bot_file.filename)
    bot_path = os.path.join(BOTS_DIR, filename)
    bot_file.save(bot_path)
    
    # زیادکردنی تووکن بۆ فایل
    with open(bot_path, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(f"TOKEN = '{bot_token}'\n" + content)
    
    return jsonify({'message': 'بۆت بەسەرکەوتوویی بارکرا', 'filename': filename})

@app.route('/start', methods=['POST'])
def start_bot():
    data = request.json
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'ناوی فایل دیاری نەکراوە'}), 400
    
    bot_path = os.path.join(BOTS_DIR, filename)
    
    if not os.path.exists(bot_path):
        return jsonify({'error': 'فایلەکە بوونی نییە'}), 404
    
    if filename in active_bots:
        return jsonify({'error': 'بۆتێک بەم ناوە پێشتر چالاکە'}), 400
    
    try:
        # ڕاناندنی بۆت لە پاشەوە
        process = subprocess.Popen(['python', bot_path], 
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        
        active_bots[filename] = process
        return jsonify({'message': 'بۆت بەسەرکەوتوویی چالاککرا'})
    
    except Exception as e:
        return jsonify({'error': f'هەڵە لە ڕاناندنی بۆت: {str(e)}'}), 500

@app.route('/stop', methods=['POST'])
def stop_bot():
    data = request.json
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'ناوی فایل دیاری نەکراوە'}), 400
    
    if filename not in active_bots:
        return jsonify({'error': 'بۆتێک بەم ناوە چالاک نییە'}), 404
    
    try:
        process = active_bots[filename]
        process.terminate()
        del active_bots[filename]
        return jsonify({'message': 'بۆت بەسەرکەوتوویی کوژایەوە'})
    
    except Exception as e:
        return jsonify({'error': f'هەڵە لە کوژاندنەوەی بۆت: {str(e)}'}), 500

@app.route('/list', methods=['GET'])
def list_bots():
    bots = []
    for filename in os.listdir(BOTS_DIR):
        if filename.endswith('.py'):
            bots.append({
                'name': filename,
                'status': 'چالاکە' if filename in active_bots else 'نەچالاکە'
            })
    return jsonify({'bots': bots})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
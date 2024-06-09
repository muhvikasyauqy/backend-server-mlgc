from flask import Flask, request, jsonify
from uuid import uuid4
import datetime
from google.cloud import firestore

app = Flask(__name__)

db = firestore.Client()

def save_prediction(data):
    doc_ref = db.collection('predictions').document(data['id'])
    doc_ref.set(data)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"status": "fail", "message": "No file part"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"status": "fail", "message": "No selected file"}), 400

    file.seek(0, 2)
    file_length = file.tell()
    if file_length > 1000000:
        return jsonify({"status": "fail", "message": "Payload content length greater than maximum allowed: 1000000"}), 413

    file.seek(0)

    # Dummy model prediction logic
    result = "Cancer" if uuid4().int % 2 == 0 else "Non-cancer"
    suggestion = "Segera periksa ke dokter!" if result == "Cancer" else "Tetap jaga kesehatan!"

    response_data = {
        "id": str(uuid4()),
        "result": result,
        "suggestion": suggestion,
        "createdAt": f'{datetime.datetime.now(datetime.timezone.utc).isoformat()}Z',
    }

    save_prediction(response_data)

    return jsonify({"status": "success", "message": "Model is predicted successfully", "data": response_data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

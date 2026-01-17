import os, json, base64, pickle
from flask import Flask, request
from tensorflow.keras.models import load_model
import numpy as np

app = Flask(__name__)

# Load AI models once when the container starts
c_model = pickle.load(open('classical_model.pkl', 'rb'))
s_model = load_model('sequential_model.h5')

@app.route("/", methods=["POST"])
def process_telemetry():
    # Pub/Sub sends data as a POST request with a JSON body
    envelope = request.get_json()
    payload = base64.b64decode(envelope['message']['data']).decode('utf-8')
data = json.loads(payload)

    # Prepare features for prediction
    static_x = np.array(data['static']).reshape(1, -1)
    seq_x = np.array(data['seq']).reshape(1, 10, 3)

    # Hybrid Logic (The "Fusion")
    c_score = c_model.predict_proba(static_x)[0][1]
    s_score = s_model.predict(seq_x, verbose=0)[0][0]

    verdict = "NORMAL"
    if c_score > 0.8 or s_score > 0.7:
        verdict = "THREAT_DETECTED"

    print(f"Analysis Complete: {verdict} (Static: {c_score:.2f}, Seq: {s_score:.2f})")
    return ("Success", 200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

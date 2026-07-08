
import hashlib
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'usuarios.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False) # SHA-256 genera 64 caracteres hex

def calcular_sha256(texto):
    """Genera el hash SHA-256 de una cadena de texto."""
    return hashlib.sha256(texto.encode('utf-8')).hexdigest()

@app.route('/registrar', methods=['POST'])
def registrar():
    """Endpoint para almacenar usuarios y contraseñas en hash."""
    data = request.get_json()
    if not data or 'usuario' not in data or 'password' not in data:
        return jsonify({"error": "Datos incompletos en el JSON"}), 400
        
    user_hash = calcular_sha256(data['password'])
    nuevo_usuario = Usuario(nombre=data['usuario'].strip(), password_hash=user_hash)
    
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"mensaje": f"Usuario '{data['usuario']}' registrado con éxito en hash SHA-256."}), 201
    except:
        db.session.rollback()
        return jsonify({"error": "El usuario ya se encuentra registrado"}), 400

@app.route('/login', methods=['POST'])
def login():
    """Endpoint para validar usuarios (Comando/Ruta respectiva de validación)."""
    data = request.get_json()
    if not data or 'usuario' not in data or 'password' not in data:
        return jsonify({"error": "Datos incompletos"}), 400
        
    user_db = Usuario.query.filter_by(nombre=data['usuario'].strip()).first()
    incoming_hash = calcular_sha256(data['password'])
    
    if user_db and user_db.password_hash == incoming_hash:
        return jsonify({
            "status": "Autenticación Exitosa",
            "mensaje": f"Bienvenido al sistema del Examen, Marcelo Valdes."
        }), 200
    else:
        return jsonify({"status": "Error", "mensaje": "Credenciales inválidas"}), 401

if __name__ == '__main__':
    # Inicializar base de datos dentro del contexto de Flask
    with app.app_context():
        db.create_all()
        
        # Requerimiento: Almacenar de forma predeterminada al integrante (Marcelo Valdes)
        nombre_integrante = "marcelo_valdes"
        if not Usuario.query.filter_by(nombre=nombre_integrante).first():
            # Contraseña por defecto para tu defensa: Cisco5800!
            hash_inicial = calcular_sha256("Cisco5800!")
            integrante_default = Usuario(nombre=nombre_integrante, password_hash=hash_inicial)
            db.session.add(integrante_default)
            db.session.commit()
            print(f"[+] Usuario base del integrante '{nombre_integrante}' creado exitosamente.")

    print("\n[i] Iniciando la API Web del Examen en el puerto 5800...")
    # Escucha en todas las interfaces en el puerto 5800 según la pauta
    app.run(host='0.0.0.0', port=5800)

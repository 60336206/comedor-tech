from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = "comedor-tech-secret-2026"

# ------------------------------------------------------------------
# "Base de datos" en memoria (rama TEST inicializa estos usuarios)
# ------------------------------------------------------------------
USUARIOS = {
    "admin": {"password": "admin123", "rol": "Administrador"},
    "colaborador": {"password": "colab123", "rol": "Colaborador"},
}

# Tickets de comedor (coinciden con el diseño de la imagen)
TICKETS = {
    "221045": {
        "codigo_estudiante": "221045",
        "nombres": "Julio Cesar",
        "apellidos": "Lloclli",
        "turno": "Turno 1 (11:30 AM)",
        "codigo_ticket": "221045-2026",
        "estado": "VALIDO_SIN_SERVIR",  # VALIDO_SIN_SERVIR | ATENDIDO
    }
}


# ------------------------------------------------------------------
# Decorador de sesión
# ------------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ------------------------------------------------------------------
# LOGIN (rama TEST)
# ------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        user = USUARIOS.get(usuario)
        if user and user["password"] == password:
            session["usuario"] = usuario
            session["rol"] = user["rol"]
            return redirect(url_for("validar"))
        error = "Credenciales incorrectas"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ------------------------------------------------------------------
# MODULO QUE IDENTIFICA AL LECTOR / ESCANEO (rama MAIN)
# ------------------------------------------------------------------
@app.route("/validar")
@login_required
def validar():
    return render_template("validar.html", usuario=session.get("usuario"), rol=session.get("rol"))


@app.route("/api/validar/<codigo>")
@login_required
def api_validar(codigo):
    ticket = TICKETS.get(codigo)
    if not ticket:
        return jsonify({"ok": False, "mensaje": "Ticket no encontrado"}), 404
    return jsonify({"ok": True, "ticket": ticket})


@app.route("/api/atender/<codigo>", methods=["POST"])
@login_required
def api_atender(codigo):
    ticket = TICKETS.get(codigo)
    if not ticket:
        return jsonify({"ok": False, "mensaje": "Ticket no encontrado"}), 404
    ticket["estado"] = "ATENDIDO"
    return jsonify({"ok": True, "ticket": ticket})


if __name__ == "__main__":
    app.run(debug=True)

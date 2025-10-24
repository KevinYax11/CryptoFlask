import os
from flask import render_template, request, flash, redirect, url_for, current_app
from . import crypto
from .config import Config

@current_app.route("/")
def index():
    keys_list = []
    try:
        keys_list = [f for f in os.listdir(Config.KEYS_DIR) if f.endswith(".pem")]
    except:
        pass

    return render_template("index.html", keys=keys_list)

@current_app.route("/keys")
def keys():
    keys_list = []
    try:
        keys_list = [f for f in os.listdir(Config.KEYS_DIR) if f.endswith(".pem")]
    except:
        pass

    return render_template("keys.html", keys=keys_list)

@current_app.route("/encrypt")
def encrypt_page():
    keys_list = []
    try:
        keys_list = [f for f in os.listdir(Config.KEYS_DIR) if f.endswith(".pem")]
    except:
        pass

    encrypted_message = request.args.get('encrypted_message')
    return render_template("encrypt.html", keys=keys_list, encrypted_message=encrypted_message)

@current_app.route("/decrypt")
def decrypt_page():
    keys_list = []
    try:
        keys_list = [f for f in os.listdir(Config.KEYS_DIR) if f.endswith(".pem")]
    except:
        pass

    decrypted_message = request.args.get('decrypted_message')
    return render_template("decrypt.html", keys=keys_list, decrypted_message=decrypted_message)

@current_app.route("/sign")
def sign_page():
    keys_list = []
    try:
        keys_list = [f for f in os.listdir(Config.KEYS_DIR) if f.endswith(".pem")]
    except:
        pass

    signature = request.args.get('signature')
    return render_template("sign.html", keys=keys_list, signature=signature)

@current_app.route("/verify")
def verify_page():
    keys_list = []
    try:
        keys_list = [f for f in os.listdir(Config.KEYS_DIR) if f.endswith(".pem")]
    except:
        pass

    verification_result = request.args.get('verification_result')
    return render_template("verify.html", keys=keys_list, verification_result=verification_result)

@current_app.route("/generate", methods=["POST"])
def route_generate():
    key_name = request.form['key_name']
    if not key_name:
        flash("Debes proporcionar un nombre base.", "error")
        return redirect(url_for('keys'))
    
    try:
        crypto.generar_y_guardar_claves(key_name)
        flash(f"Claves '{key_name}' generadas exitosamente.", "success")
    except Exception as e:
        flash(f"Error al generar claves: {e}", "error")
        
    return redirect(url_for('keys'))

@current_app.route("/encrypt", methods=["POST"])
def route_encrypt():
    message_bytes = request.form['message'].encode('utf-8')
    key_name = request.form['key_name']
    
    try:
        encrypted_b64 = crypto.cifrar_mensaje(message_bytes, key_name)
        flash("Mensaje cifrado exitosamente.", "success")
        return redirect(url_for('encrypt_page', encrypted_message=encrypted_b64))
    except FileNotFoundError:
        flash(f"Error: No se encontró la clave pública '{key_name}'.", "error")
    except Exception as e:
        flash(f"Error al cifrar: {e}", "error")
        
    return redirect(url_for('encrypt_page'))

@current_app.route("/decrypt", methods=["POST"])
def route_decrypt():
    encrypted_b64 = request.form['message']
    key_name = request.form['key_name']
    
    try:
        decrypted_message = crypto.descifrar_mensaje(encrypted_b64, key_name)
        flash("Mensaje descifrado exitosamente.", "success")
        return redirect(url_for('decrypt_page', decrypted_message=decrypted_message))
    except FileNotFoundError:
        flash(f"Error: No se encontró la clave privada '{key_name}'.", "error")
    except Exception as e:
        flash(f"Error al descifrar: {e}", "error")
        
    return redirect(url_for('decrypt_page'))

@current_app.route("/sign", methods=["POST"])
def route_sign():
    message_bytes = request.form['message'].encode('utf-8')
    key_name = request.form['key_name']
    
    try:
        signature_b64 = crypto.firmar_mensaje(message_bytes, key_name)
        flash("Mensaje firmado exitosamente.", "success")
        return redirect(url_for('sign_page', signature=signature_b64))
    except FileNotFoundError:
        flash(f"Error: No se encontró la clave privada '{key_name}'.", "error")
    except Exception as e:
        flash(f"Error al firmar: {e}", "error")
        
    return redirect(url_for('sign_page'))

@current_app.route("/verify", methods=["POST"])
def route_verify():
    message_bytes = request.form['message'].encode('utf-8')
    signature_b64 = request.form['signature']
    key_name = request.form['key_name']
    
    try:
        es_valida = crypto.verificar_firma(message_bytes, signature_b64, key_name)
        
        if es_valida:
            flash("Verificación exitosa: La firma es válida.", "success")
            return redirect(url_for('verify_page', verification_result='True'))
        else:
            flash("Verificación fallida: La firma es inválida.", "error")
            return redirect(url_for('verify_page', verification_result='False'))
            
    except FileNotFoundError:
        flash(f"Error: No se encontró la clave pública '{key_name}'.", "error")
    except Exception as e:
        flash(f"Error al verificar: {e}", "error")
        
    return redirect(url_for('verify_page'))
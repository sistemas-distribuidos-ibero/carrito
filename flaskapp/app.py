from flask import Flask, request, jsonify, abort
import threading
import carrito as carrito
import redis
import carrito
import os
from dotenv import load_dotenv
from flask_cors import CORS


# -----------------------------------------------------------------------------

load_dotenv()
app = Flask(__name__)
CORS(app)
print(os.environ.get("DATABASE_URL"))
conn = redis.from_url(os.environ.get("DATABASE_URL"))
#conn =redis.Redis()
#redis_host = os.getenv('REDIS_HOST', '127.0.0.1')
#redis_port = os.getenv('REDIS_HOST', 6379)
#conn = redis.Redis(host=redis_host, port=redis_port)


# -----------------------------------------------------------------------------

##Metodo para cambiar el carrito de un usuario, recibe el id de usuario, el id de producto y la cantidad de este
##Si se recibe 0 o negativo commo cantidad se elimina el producto del carrito
@app.route('/cart', methods=['POST'])
def add_to_cart():
    item_id = request.json.get('item_id')
    quantity = request.json.get('quantity')
    user_id = request.json.get('user_id') 
     # Validate the received data
    if item_id is None or quantity is None or user_id is None:
        return jsonify({'error': 'Missing data'}), 400

    try:
        carrito.add_to_cart(conn, user_id, item_id, quantity)
        return jsonify({"message": f"Cart:{str(user_id)} changed successfully. item:{item_id} = {str(quantity)}"}), 200
    except Exception as e:
        return jsonify({'error': str(e), 'cart': "no cart"}), 500

##Devuelve el carrito, recibe el id de usuario
@app.route('/get-cart', methods=['POST'])
def get_cart():
    user_id = request.json["user_id"]
    if user_id is None:
        return jsonify({'error': 'Missing data'}), 400
    try:
        cart = carrito.fetch_cart(conn, user_id)
        decoded_cart = {key.decode('utf-8'): value.decode('utf-8') for key, value in cart.items()}
        return jsonify(decoded_cart), 200
    except Exception as e:
        return jsonify({'error': str(e), 'cart': "no cart"}), 500

##Borra el carrito, recibe el id de usuario
@app.route('/cart/<int:user_id>', methods=['DELETE'])
def del_cart(user_id):
    if user_id is None:
        return jsonify({'error': 'Missing data'}), 400
    try:
        carrito.delete_cart(conn,user_id)
        return jsonify({"message": f"Cart {user_id} deleted"})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    ##Función limpiadora de carritos, borra los carritos carritos mas viejos sin utilizar pasados los 10000
    thread = threading.Thread(target=carrito.clean_full_sessions, args=(conn,), daemon=True)
    thread.start()
    app.run(debug=os.environ.get("DEBUG"), port=os.getenv('FLASK_PORT'), host=os.getenv('HOST'))

import redis
import time

QUIT = False
LIMIT = 10000 ##Numero máximo de carritos

##Convierte a str
def to_str(x):
    return x.decode() if isinstance(x, bytes) else x

##Modificar carrito
def add_to_cart(conn, user, item, count):
    if count <= 0:
        conn.zadd('recent:', {user: time.time()})
        conn.hrem('cart:' + str(user), item)
    else:
        conn.zadd('recent:', {user: time.time()})
        conn.hset('cart:' + str(user), item, str(count))

##Regresa carrito
def fetch_cart(conn, user):
    return conn.hgetall('cart:'+ str(user))

#Regresa la lista de todos los carritos guardados
def fetch_recent(conn):
    return conn.zrange('recent:', 0, -1, withscores=True)

##Borra carrito
def delete_cart(conn,user):
    conn.delete('cart:'+str(user))
    conn.zrem('recent:',str(user))

##Limpia carritos más antiguos sin utilizar
def clean_full_sessions(conn):
    while not QUIT:
        size = conn.zcard('recent:')
        if size <= LIMIT:
            time.sleep(1)
            continue

        end_index = min(size - LIMIT, 100)
        sessions = conn.zrange('recent:', 0, end_index-1)

        session_keys = []
        for sess in sessions:
            sess = to_str(sess)
            session_keys.append('cart:' + sess)                    #A

        conn.delete(*session_keys)
        conn.zrem('recent:', *sessions)


if __name__ == '__main__':
    import threading
    conn = redis.Redis()
    LIMIT = 5
    t = threading.Thread(target=clean_full_sessions, args=(conn,), daemon=True)
    t.start()
    add_to_cart(conn, '234', 'item:1234', 1)
    add_to_cart(conn, '134', 'item:1234', 1)
    add_to_cart(conn, '334', 'item:1234', 1)
    add_to_cart(conn, '434', 'item:1234', 1)
    add_to_cart(conn, '534', 'item:1234', 1)
    add_to_cart(conn, '634', 'item:1234', 1)
    time.sleep(2)
    print(fetch_cart(conn, '234'))
    print(fetch_recent(conn))
    QUIT = True
    time.sleep(2)
    if t.is_alive():
        raise Exception("thread is still alive")
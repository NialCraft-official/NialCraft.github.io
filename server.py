import socket, select, sys, os
from datetime import datetime

# Настраиваем хост на 0.0.0.0 (чтобы сервер слушал весь мир, а не только локалку)
H = "0.0.0.0"
# Облачные хостинги передают выданный порт через переменную окружения PORT. Если её нет — ставим 25565
P = int(os.environ.get("PORT", 25565))
MAX_PLAYERS = 50

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((H, P))
server_socket.listen(MAX_PLAYERS)
server_socket.setblocking(False)

sockets_list = [server_socket]
clients = {} 
next_uid = 1000

def log(m, l, g):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f" [{ts}] [{m}/{l}] {g}"); sys.stdout.flush()

log("CORE", "READY", f"NialCraft Cloud Core powered for NASA supercomputers. Port: {P}")
print("-" * 80)

while True:
    try:
        read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list, 0.01)
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                if len(clients) >= MAX_PLAYERS:
                    client_socket.close()
                    continue
                client_socket.setblocking(False)
                sockets_list.append(client_socket)
                uid = next_uid; next_uid += 1
                clients[client_socket] = {"id": uid, "x": 4, "y": 4}
                log("NET", "CONN", f"Slots: {len(clients)}/{MAX_PLAYERS} | Target incoming client UID: {uid}")
                client_socket.sendall(bytes([1, uid >> 8, uid & 255]))
                spawn_pkt = bytes([2, uid >> 8, uid & 255, 4, 4])
                for sock in clients:
                    if sock != client_socket:
                        try: sock.sendall(spawn_pkt)
                        except: pass
                for sock, info in clients.items():
                    if sock != client_socket:
                        try: client_socket.sendall(bytes([2, info["id"] >> 8, info["id"] & 255, info["x"], info["y"]]))
                        except: pass
            else:
                try:
                    data = notified_socket.recv(5)
                    if not data: raise Exception()
                    if data[0] == 3 and len(data) == 5:
                        uid = (data[1] << 8) + data[2]
                        cx, cy = data[3], data[4]
                        if notified_socket in clients and clients[notified_socket]["id"] == uid:
                            clients[notified_socket]["x"], clients[notified_socket]["y"] = cx, cy
                            for sock in clients:
                                if sock != notified_socket:
                                    try: sock.sendall(data)
                                    except: pass
                except:
                    if notified_socket in clients:
                        info = clients[notified_socket]
                        log("NET", "DISC", f"Connection terminated for UID: {info['id']}")
                        quit_pkt = bytes([4, info["id"] >> 8, info["id"] & 255])
                        for sock in clients:
                            if sock != notified_socket:
                                try: sock.sendall(quit_pkt)
                                except: pass
                        del clients[notified_socket]
                    if notified_socket in sockets_list: sockets_list.remove(notified_socket)
                    try: notified_socket.close()
                    except: pass
        for notified_socket in exception_sockets:
            if notified_socket in sockets_list: sockets_list.remove(notified_socket)
            if notified_socket in clients: del clients[notified_socket]
            try: notified_socket.close()
            except: pass
    except KeyboardInterrupt: break
server_socket.close()
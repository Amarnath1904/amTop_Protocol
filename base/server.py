import socket
import json
import threading
from base.amtop import messagemaker, send, recive, compute



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = socket.gethostbyname(socket.gethostname())
PORT = 6969
FORMAT = "utf-8"
Disconect = "!DISCONNECT"
HEADER = 64




nodes = []




s.bind((IP, PORT))
s.listen(5)
print(f"server is listening on {IP}:{PORT}")


def clinthandling(socket, addr):
    connected = True
    while connected:


        send(socket, messagemaker("Connected"))
        data = recive(socket)
        if data["action"] == Disconect:
            connected = False
            socket.close()
            break
        elif data["action"] == "ConnectTOMotherServer":


            nodes.append(addr)
            DataTosend = {
                "ID": nodes.index(addr),
            }
            send(socket, messagemaker("ID", DataTosend))
            nodelist = nodes.copy()
            nodelist.pop(nodelist.index(addr))
            DataTosend = {
                "nodes": nodelist,
            }

            send(socket, messagemaker("ConnectTo", DataTosend))



        elif data["action"] == "Compute":
            a = compute(data["data"])
            send(socket, messagemaker("Result", a))


while True:
    socket, addr = s.accept()
    print(f"connected to {addr}")
    alpha = threading.Thread(target=clinthandling, args=(socket, addr))
    alpha.start()

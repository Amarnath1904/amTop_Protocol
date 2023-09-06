import threading
import socket
import json




ID = None
HEADER = 64
PORT = 6969
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
MOTHER_SERVER_IP = "192.168.1.5"




def messagemaker(action, data=None):

    """
    
    param action: str
    param data: dict
    return: bytes

    message maker is an object that takes an action and data and converts it to data that can be passed throw send() function
    """

    if data == None:
        data = {"action": action}
    else:
        data = {"action": action, "data": data}

    data = json.dumps(data)
    data = data.encode(FORMAT)
    return data


def send(conn, data):

    """
        param conn: socket object
        param data: bytes
        return: None

        send is an object that takes a socket object and data and sends it throw the network

    """




    SendingHEADER =  str(len(data)).encode(FORMAT)
    conn.send(SendingHEADER)
    conn.send(data)

def recive(conn):

    """
        param conn: socket object
        return: dict
        
    """


    data = conn.recv(HEADER).decode(FORMAT)
    data = conn.recv(int(data)).decode(FORMAT)
    data = json.loads(data)
    return data



def compute(data):
    d = json.loads(data)
    num1 = d["num1"]
    num2 = d["num2"]
    do = d["do"]
    print(num1, do,num2)
    if do== "+":
        return num1 + num2
    elif do == "-":
        return num1 - num2
    elif do == "*":
        return num1 * num2
    elif do == "/":
        return num1 / num2



def ClientHandling(clientsocket):

    Conected = True
    while Conected:
        send(clientsocket, messagemaker("Connected"))
        data = recive(clientsocket)
        if data["action"] == DISCONNECT_MESSAGE:
            Conected = False
            clientsocket.close()

            break
        elif data["action"] == "Compute":
            a = compute(data["data"])
            send(clientsocket, messagemaker("Result", a))





def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 6969
    ADDR = (IP, PORT)
    s.bind(ADDR)
    s.listen(5)
    print(f"[LISTENING] Server is listening on {IP}")
    while True:
        clientsocket, address = s.accept()
        print(f"[NEW CONNECTION] {address} connected.")
        thread = threading.Thread(target=ClientHandling, args=(clientsocket,))
        thread.start()





def clint(IP=None, action=None, data=None, expectingReturndata=True, SendingdataAction=None):
    if action == "ConnectTOMotherServer":
        try :
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            IP = MOTHER_SERVER_IP
            PORT = 6969
            s.connect((IP, PORT))
            data = { "action": "ConnectTOMotherServer"}
            send(s, data)
            data = recive(s)
            global ID
            ID = data["ID"]
            ConnectTo = recive(s)
            return "Success", ConnectTo

        except Exception as e:
            return e
    elif action=="Instance":
        if IP == None:
            return "No IP"
        else:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                PORT = 6969
                s.connect((IP, PORT))
                Connectionmsg = recive(s)
                if Connectionmsg["action"] == "Connected":
                    send(s, messagemaker("Compute", data))
                    data = recive(s)
                    return data
                
                if expectingReturndata:
                    data = recive(s)
                    return data["nodes"]
                else:
                    return "Success"
            except Exception as e:
                return e

        


def start():
    if ID == None:
        result = clint(action="ConnectTOMotherServer")
        if result != "Success":
            print(result)
            return None
        elif result[0] == "Success":
            return result[1] 
        
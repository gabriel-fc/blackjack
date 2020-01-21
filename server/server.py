import match
import socket
import _thread


groups = [list(), list(), list()]

menu_msg = "Seja bem-vindo(a) ao BlackJack On-line!!\n" + "Escolha o modo:\n" + \
    "2. 2 jogadores\n" + "3. 3 jogadores\n" + "4. 4 jogadores\n"

address = ("", 20000 )

class Player:
    def __init__(self, nickName, conn, address):
        self.status =  'playing'
        self.nickName = nickName
        self.conn = conn
        self.address = address
        self.score = 0






def create_socket():
    web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    web_socket.bind(address)
    web_socket.listen(32)
    return web_socket    


def set_group(response, client):
    client.conn.send("Formando grupos...\n".encode())
    index = response - 2
    groups[index].append(client)
    if len(groups[index]) == response:
        aux = groups[index]
        groups[index] = list()
        match.run(aux)



web_socket = create_socket()

def set_player(conn, address):
    print("client with address {} conected!".format(address))
    conn.send(menu_msg.encode())
    response = int(conn.recv(1024).decode())
    player = Player("Jogador " + str(len(groups[response-2]) + 1), conn, address)
    set_group(response, player)



print("IP do servidor: {}".format(socket.gethostbyname(socket.gethostname())))
while True:
    conn, address = web_socket.accept()
    _thread.start_new_thread(set_player, (conn, address))
   
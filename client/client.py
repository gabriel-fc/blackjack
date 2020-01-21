import socket

address = None




def create_socket(server = False):
    web_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    web_socket.connect(address)    
    return web_socket





def match():
    end = False
    while not end:
        response = web_socket.recv(1024).decode()
        if response == 'Calculando resultado final...\n':
            end = True
        print(response)
        if response == "É a sua vez!\n1. Mais uma carta\n2. Parar\n":
            web_socket.send(input_exception(1, 2).encode())
            response = web_socket.recv(1024).decode()
            print(response)

        response = web_socket.recv(1024).decode()
        print(response)

    return






def input_exception(lo, hi):
    try:
        user_input = int(input())
    except ValueError:
        print("O dado informado não é um número! Por favor forneça uma entrada válida.\n")
        return str(input_exception(lo, hi))

    if user_input < lo or user_input > hi:
        print("Este valor não corresponde a uma opção válida! Por favor tente novamente.\n")
        return str(input_exception(lo, hi))
    return str(user_input)




print("Por favor, informe o ip do servidor!\n")
ip = str(input())
address = (ip, 20000)
web_socket = create_socket()
response = web_socket.recv(1024).decode()
print(response)
web_socket.send(input_exception(2, 4).encode())
response = web_socket.recv(1024).decode()
print(response)
response = web_socket.recv(1024).decode()
print(response)
match()













    
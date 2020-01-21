import socket
from random import seed
from random import choice
import time

seed(time.time())


deck = [{'name': "ás de paus", 'value': 1}, {'name': "2 de paus", 'value': 2}, {'name': "3 de paus", 'value': 3}, {'name': "4 de paus", 'value': 4}, {
        'name': "5 de paus", 'value': 5}, {'name': "6 de paus", 'value': 6}, {'name': "7 de paus", 'value': 7}, {'name': "8 de paus", 'value': 8}, {'name': "9 de paus", 'value': 9}, {'name': "10 de paus", 'value': 10}, {'name': "valete de paus", 'value': 11}, {'name': "dama de paus", 'value': 12}, {'name': "rei de paus", 'value': 13}, {'name': "ás de espadas", 'value': 1}, {'name': "2 de espadas", 'value': 2}, {'name': "3 de espadas", 'value': 3}, {'name': "4 de espadas", 'value': 4}, {
        'name': "5 de espadas", 'value': 5}, {'name': "6 de espadas", 'value': 6}, {'name': "7 de espadas", 'value': 7}, {'name': "8 de espadas", 'value': 8}, {'name': "9 de espadas", 'value': 9}, {'name': "10 de espadas", 'value': 10}, {'name': "valete de espadas", 'value': 11}, {'name': "dama de espadas", 'value': 12}, {'name': "rei de espadas", 'value': 13}, {'name': "ás de ouros", 'value': 1}, {'name': "2 de ouros", 'value': 2}, {'name': "3 de ouros", 'value': 3}, {'name': "4 de ouros", 'value': 4}, {
        'name': "5 de ouros", 'value': 5}, {'name': "6 de ouros", 'value': 6}, {'name': "7 de ouros", 'value': 7}, {'name': "8 de ouros", 'value': 8}, {'name': "9 de ouros", 'value': 9}, {'name': "10 de ouros", 'value': 10}, {'name': "valete de ouros", 'value': 11}, {'name': "dama de ouros", 'value': 12}, {'name': "rei de ouros", 'value': 13}, {'name': "ás de copas", 'value': 1}, {'name': "2 de copas", 'value': 2}, {'name': "3 de copas", 'value': 3}, {'name': "4 de copas", 'value': 4}, {
        'name': "5 de copas", 'value': 5}, {'name': "6 de copas", 'value': 6}, {'name': "7 de copas", 'value': 7}, {'name': "8 de copas", 'value': 8}, {'name': "9 de copas", 'value': 9}, {'name': "10 de copas", 'value': 10}, {'name': "valete de copas", 'value': 11}, {'name': "dama de copas", 'value': 12}, {'name': "rei de copas", 'value': 13}]


def timer(secs):
    time.sleep(secs)


yt_msg = "É a sua vez!\n1. Mais uma carta\n2. Parar\n"


def set_score_list(size):
    score_list = list()
    for i in range(size):
        score_list.append(0)
    return score_list


def send_msg_single_client(client, msg):
    client.conn.send(msg.encode())


def transmission(ignore, clients, msg):

    for c in clients:
        if c != ignore:
            c.conn.send(msg.encode())


def gen_score_msg(clients, c, end):
    if not end:
        msg = "Tabela de pontuação atual:\n~~~~~~~~~~~~~~~~~~~~~~~~~\n"
    else:
        msg = "Resultado final:\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

    for aux in clients:
        if aux == c:
            msg += "Você: " + str(aux.score) + " pontos.\n"
        else:
            msg += aux.nickName + ": " + str(aux.score) + " pontos.\n"

    msg += "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
    if end:
        msg += "Partida finalizada!\n"
    send_msg_single_client(c, msg)


def show_score_msg(clients, end):
    for c in clients:
        gen_score_msg(clients, c, end)


def run(clients):

    timer(2)
    transmission(None, clients, "a partida começou!\n")

    players = len(clients)
    while players != 0:
        for c in clients:
            if c.status == 'playing':
                timer(1)
                transmission(
                    c, clients, ("Esperando o jogador " + c.nickName + "!\n"))
                send_msg_single_client(c, yt_msg)
                response = int(c.conn.recv(1024).decode())
                if response == 1:
                    card = get_card(deck)
                    timer(2)
                    send_msg_single_client(
                        c, ("sua carta foi: " + card['name'] + "!\n"))
                    c.score += card['value']
                    if c.score >= 21:
                        c.status = "finished"
                        players -= 1
                else:
                    send_msg_single_client(
                        c, ("Jogada finalizada! Aguarde o término da partida.\n"))
                    c.status = "finished"
                    players -= 1
                timer(2)
                show_score_msg(sort_score_table(list(clients)), False)
                timer(1)

    transmission(None, clients, "Calculando resultado final...\n")
    timer(3)
    show_score_msg(sort_score_table(list(clients)), True)


def sort_score_table(score_table):
    for i in range(len(score_table)):
        for j in range(i+1, len(score_table)):
            if score_table[i].score > 21:
                if score_table[i].score > score_table[j].score:
                    swap(i, j, score_table)
            else:
                if score_table[i].score < score_table[j].score and score_table[j].score <= 21:
                    swap(i, j, score_table)
    return score_table


def swap(i, j, _list):
    temp = _list[i]
    _list[i] = _list[j]
    _list[j] = temp


def get_card(deck):
    card = choice(deck)
    deck.remove(card)
    return card

import socket, threading


def determine_card_type(card_value):
    card_value = int(card_value)

    if card_value == 1:
        return 'A'
    elif card_value == 11:
        return "J"
    elif card_value == 12:
        return "Q"
    elif card_value == 13:
        return "K"
    else:
        return card_value


def retrieve_card_value(card_value):
    if card_value == 'A' or card_value == 'a':
        return 1
    elif card_value == 'J' or card_value == 'j':
        return 11
    elif card_value == 'Q' or card_value == 'q':
        return 12
    elif card_value == 'K' or card_value == 'k':
        return 13
    else:
        return int(card_value)


def send():
    while True:
        msg = input('\nSelect your card >> ')
        msg = retrieve_card_value(msg)

        if msg < 1 or 13 < msg:
            print("Invalid card Please choose valid card...")
            continue
        elif msg in CARD_LIST:
            print("You already used this card please choose another one....")
            continue
        else:
            CARD_LIST.append(msg)
            break

    cli_sock.send(str(msg).encode("utf-8"))


def receive():
    while True:
        try:
            data = cli_sock.recv(1024)
            if data:
                data = data.decode("utf-8")
                # print(data)
                data = eval(data)

                if len(data['used_cards']) != 0:
                    if len(data['used_cards']) ==13 :
                        print("game over")
                        break
                    print("You get ", data['score_this_round'], " in this round")
                    print("Your total score is ", data['total_score'])
                    
                    
                    

                #winnerstatement
                print("\n\n\n\nThe card choosen by server is ", determine_card_type(data['server_card']))
                send()
                
        except Exception as x:
            print(x.message)
            break


if __name__ == "__main__":
    CARD_LIST = []
    # socket
    cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect
    HOST = 'localhost'
    PORT = 5049
    cli_sock.connect((HOST, PORT))
    print('Connected to remote host...')
    uname = input('Enter your name to start a Game:')
    cli_sock.send(uname.encode("utf-8"))

    # thread_send = threading.Thread(target=send)
    # thread_send.start()

    thread_receive = threading.Thread(target=receive)
    thread_receive.start()

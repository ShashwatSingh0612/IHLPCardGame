import socket, threading, random, json


def receive_connection():
    while CLIENT_COUNT[0] != 3:
        cli_sock, cli_add = ser_sock.accept()
        uname = cli_sock.recv(1024)
        uname = uname.decode("utf-8")
        CONNECTION_LIST[CLIENT_COUNT[0]]['connection'] = cli_sock
        CONNECTION_LIST[CLIENT_COUNT[0]]['name'] = uname
        CLIENT_COUNT[0] = CLIENT_COUNT[0] + 1
        print('%s is now connected' % uname)

    if CLIENT_COUNT[0] == 3:
        deliver_response()
        print("Server card is ", SERVER_CARDS[SERVER_CARDS_COUNTER[0]])
        for i in range(len(CONNECTION_LIST)):
            thread_client = threading.Thread(target=distribute_message, args=str(i))
            thread_client.start()

def deliver_response():
    for client in CONNECTION_LIST:
        
        # if SERVER_CARDS_COUNTER[0] > 13 :
        #     final_list ={
        #     "name": client['name'],
        #     "used_cards": client['used_cards'],
        #     "score_round": client['score_round'],
        #     "total_score": client['total_score'],
        #     "score_this_round": client['score_round'][SERVER_CARDS_COUNTER[0] - 1]
        # }
        #     winner()

        if SERVER_CARDS_COUNTER[0] == 13 :
            lastround_list = {
            "name": client['name'],
            "used_cards": client['used_cards'],
            "score_round": client['score_round'],
            "total_score": client['total_score'],
            "score_this_round": client['score_round'][SERVER_CARDS_COUNTER[0] - 1]
        }
            y = str(json.dumps(lastround_list))              
            client['connection'].send(bytes(str(y), 'utf-8'))
            print(bytes(y, 'utf-8'))
            winner()
            
        else:
            temp_list = {
                "name": client['name'],
                "used_cards": client['used_cards'],
                "score_round": client['score_round'],
                "total_score": client['total_score'],
                "server_card": SERVER_CARDS[SERVER_CARDS_COUNTER[0]],
                "score_this_round": client['score_round'][SERVER_CARDS_COUNTER[0] - 1]
            }
            y = str(json.dumps(temp_list))              
            client['connection'].send(bytes(str(y), 'utf-8'))
            print(bytes(y, 'utf-8'))
            

def winner():

    print("Winner is someone!!!")  
    winner_name=[]

    if(CONNECTION_LIST[0]['total_score'] >= CONNECTION_LIST[1]['total_score'] and CONNECTION_LIST[0]['total_score'] >= CONNECTION_LIST[2]['total_score']):
        print(f"{CONNECTION_LIST[0]['name']} is winner")
        winner_name.add(CONNECTION_LIST[0]['name'])

    if(CONNECTION_LIST[1]['total_score'] >= CONNECTION_LIST[0]['total_score'] and CONNECTION_LIST[1]['total_score'] >= CONNECTION_LIST[2]['total_score']):
        print(f"{CONNECTION_LIST[1]['name']} is winner")
        winner_name.add(CONNECTION_LIST[1]['name'])

    if(CONNECTION_LIST[2]['total_score'] >= CONNECTION_LIST[0]['total_score'] and CONNECTION_LIST[2]['total_score'] >= CONNECTION_LIST[1]['total_score']):
        print(f"{CONNECTION_LIST[2]['name']} is winner")
        winner_name.add(CONNECTION_LIST[2]['name'])  
      

def evaluate_result():
    server_card = SERVER_CARDS[SERVER_CARDS_COUNTER[0]]
    client1_card = int(CONNECTION_LIST[0]['used_cards'][-1])
    client2_card = int(CONNECTION_LIST[1]['used_cards'][-1])
    client3_card = int(CONNECTION_LIST[2]['used_cards'][-1])

    if client1_card >= client2_card and client1_card >= client3_card:
        CONNECTION_LIST[0]['score_round'][SERVER_CARDS_COUNTER[0]] = server_card

    if client2_card >= client1_card and client2_card >= client3_card:
        CONNECTION_LIST[1]['score_round'][SERVER_CARDS_COUNTER[0]] = server_card

    if client3_card >= client1_card and client3_card >= client2_card:
        CONNECTION_LIST[2]['score_round'][SERVER_CARDS_COUNTER[0]] = server_card

    for i in range(len(CONNECTION_LIST)):
        CONNECTION_LIST[i]['total_score'] = sum(int(j) for j in CONNECTION_LIST[i]['score_round'])

    print(SERVER_CARDS[SERVER_CARDS_COUNTER[0]])

    SERVER_CARDS_COUNTER[0] = SERVER_CARDS_COUNTER[0] + 1

    deliver_response() #3error


def print_card_table():
    if CARD_ACCEPT_FLAG[0] == 3:
        CARD_ACCEPT_FLAG[0] = 1
        evaluate_result()               #error2
    else:
        CARD_ACCEPT_FLAG[0] = CARD_ACCEPT_FLAG[0] + 1


def distribute_message(i):
    i = int(i)
    while True:
        try:
            data = CONNECTION_LIST[i]['connection'].recv(1024)
            if data:
                card = data.decode("utf-8")
                print("{0} choose".format(CONNECTION_LIST[i]['name']), card)
                list = CONNECTION_LIST[i]['used_cards']
                list.append(int(card))
                CONNECTION_LIST[i]['used_cards'] = list
                print_card_table() #error1
        except Exception as x:
            #print(x.message) 
            break

if __name__ == "__main__":
    SERVER_CARDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    random.shuffle(SERVER_CARDS)

    CLIENT_COUNT = [0]
    SERVER_CARDS_COUNTER = [0]

    CONNECTION_LIST = [
        {
            "connection": None,
            "name": "",
            "used_cards": [],
            "score_round": [0 for element in range(13)],
            "total_score": []
        }, {
            "connection": None,
            "name": "",
            "used_cards": [],
            "score_round": [0 for element in range(13)],
            "total_score": []
        }, {
            "connection": None,
            "name": "",
            "used_cards": [],
            "score_round": [0 for element in range(13)],
            "total_score": []
        }
    ]
    CARD_TABLE = {}
    CARD_ACCEPT_FLAG = [1]

    # socket
    ser_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind
    HOST = 'localhost'
    PORT = 5049
    ser_sock.bind((HOST, PORT))

    # listen
    ser_sock.listen(1)
    print('Game server started on port : ' + str(PORT))

    thread_ac = threading.Thread(target=receive_connection)
    thread_ac.start()

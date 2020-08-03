import pickle
import socket
import sys

from _thread import start_new_thread
from settings import *
from game import RPSGame


server = socket.gethostbyname(socket.gethostname())
port = PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print("Waiting for connection, server started...")

games = dict()
players_count = 0


def threaded_client(conn, player_id, game_id):
    global players_count
    
    conn.send(str.encode(str(player_id)))
    
    while True:
        try:
            data = conn.recv(BYTE_SIZE * 2).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    break
                else:
                    if data == 'reset':
                        game.reset()
                    elif data == 'score1':
                        game.wins[0] += 1
                    elif data == 'score2':
                        game.wins[1] += 1
                    elif data != 'get':
                        game.update_move(player_id, data)
                    
                    conn.sendall(pickle.dumps(game))
            else:
                print('Game does not exist...')
                break

        except:
            break

    print('Lost connection..')

    try:
        del games[game_id]
        print('Closing Game', game_id)
    except:
        pass

    players_count -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print(f"Connected to {addr}")

    players_count += 1
    player_id = 0

    game_id = (players_count - 1) // 2

    if players_count % 2 == 1:
        games[game_id] = RPSGame(game_id)
        print('Creating a new game...')
    else:
        games[game_id].ready = True
        player_id = 1


    start_new_thread(threaded_client, (conn, player_id, game_id))

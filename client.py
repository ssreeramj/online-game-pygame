import pickle
import sys

import pygame as pg

from network import Network
from settings import *
from widgets.button import Button
from widgets.label import show_label

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(TITLE)
pg.font.init()
pg.mixer.init()

clock = pg.time.Clock()

rock_butt = Button(screen, 'rect', (WIDTH*0.1, HEIGHT*0.75), (150, 50), RED)
paper_butt = Button(screen, 'rect', (WIDTH*0.4, HEIGHT*0.75), (150, 50), GREEN)
scissor_butt = Button(screen, 'rect', (WIDTH*0.7, HEIGHT*0.75), (150, 50), YELLOW)

rock_butt.add_text('Rock', 15, BLACK)
paper_butt.add_text('Paper', 15, BLACK)
scissor_butt.add_text('Scissors', 15, BLACK)

buttons = [rock_butt, paper_butt, scissor_butt]

def redraw_window(window, game, player):
    window.fill(BLACK)

    if not game.is_connected():
        show_label(window, (WIDTH/2, HEIGHT/2), 60, BLUE, 'Waiting for Player...')
    else:
        show_label(window, (WIDTH*0.3, HEIGHT*0.3), 40, WHITE, 'Your Move')
        show_label(window, (WIDTH*0.7, HEIGHT*0.3), 40, WHITE, 'Opponents')

        if player == 0:
            show_label(window, (WIDTH*0.3, HEIGHT*0.36), 25, WHITE, f"{game.wins[0]}")
            show_label(window, (WIDTH*0.7, HEIGHT*0.36), 25, WHITE, f"{game.wins[1]}")
        else:
            show_label(window, (WIDTH*0.3, HEIGHT*0.36), 25, WHITE, f"{game.wins[1]}")
            show_label(window, (WIDTH*0.7, HEIGHT*0.36), 25, WHITE, f"{game.wins[0]}")

        move_1 = game.get_player_move(0)
        move_2 = game.get_player_move(1)

        if game.did_both_play():
            text_1, text_2 = move_1, move_2

        else:
            if game.did_p1_play:
                if player == 0:
                    text_1 = move_1
                else:
                    text_1 = 'Locked In'
            else:
                text_1 = 'Waiting...'

            if game.did_p2_play:
                if player == 1:
                    text_2 = move_2
                else:
                    text_2 = 'Locked In'
            else:
                text_2 = 'Waiting...'

        if player == 0:
            show_label(window, (WIDTH*0.3, HEIGHT*0.5), 40, BLUE, text_1)
            show_label(window, (WIDTH*0.7, HEIGHT*0.5), 40, BLUE, text_2)
        else:
            show_label(window, (WIDTH*0.3, HEIGHT*0.5), 40, BLUE, text_2)
            show_label(window, (WIDTH*0.7, HEIGHT*0.5), 40, BLUE, text_1)

    
        for btn in buttons:
            btn.draw()

    pg.display.update()

def main():
    is_running = True
    n = Network()
    player_id = int(n.get_player())

    while is_running:
        #Fill the screen with black
        screen.fill(BLACK)

        try:
            game = n.send('get')
        except:
            is_running = False
            print("Couldn't get game")
            break

        if game.did_both_play():
            screen.fill(BLACK)
            redraw_window(screen, game, player_id)

            pg.time.delay(500)

            try:
                game = n.send('reset')
            except:
                is_running = False
                print("Couldn't get game...")
                break
            
            # update score
            result = game.get_winner()
            
            if result == player_id:
                show_label(screen, (WIDTH*0.5, HEIGHT*0.6), 50, GREEN, 'You Won...')
                if player_id == 0:
                    n.send('score1')
                else:
                    n.send('score2')
            elif result == -1:
                show_label(screen, (WIDTH*0.5, HEIGHT*0.6), 50, WHITE, 'Game Tied...')
            else:
                show_label(screen, (WIDTH*0.5, HEIGHT*0.6), 50, RED, 'You Lost...')

            pg.display.update()
            pg.time.delay(2000)



        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
                pg.quit()
                sys.exit()

            #if the button is clicked, send info to server
            if event.type == pg.MOUSEBUTTONUP:
                for btn in buttons:
                    if btn.touching(pg.mouse.get_pos()) and game.is_connected():
                        if player_id == 0 and not game.did_p1_play:
                            n.send(btn.actual_text)
                        elif player_id == 1 and not game.did_p2_play:
                            n.send(btn.actual_text)
                         
                    
        redraw_window(screen, game, player_id)
        clock.tick(FPS)


def menu_screen():
    is_start = True
    clock = pg.time.Clock()

    while is_start:
        screen.fill(BLACK)
        show_label(screen, (WIDTH/2, HEIGHT/2), 50, WHITE, 'Click to join lobby')
        pg.display.update()
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                is_start = False

            if event.type == pg.MOUSEBUTTONUP:
                is_start = False

    main()


if __name__ == '__main__':
    while True:
        menu_screen()
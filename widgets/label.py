import pygame as pg

def show_label(surface, pos, size, color, text, font='comicsaans', anti_alias=1):
    font = pg.font.SysFont(font, size)
    text = font.render(text, anti_alias, color)
    text_pos = text.get_rect(center=(pos[0], pos[1]))
    surface.blit(text, text_pos)
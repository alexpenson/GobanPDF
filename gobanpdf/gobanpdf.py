# -*- coding: utf-8 -*-

"""Main module."""

from sgfmill import sgf
from sgfmill import sgf_moves
import pandas as pd
from plotnine import *
import sys
import click

def read_board(sgf_file, move_number):
    sgf_src = sgf_file.read()
    sgf_file.close()
    try:
        sgf_game = sgf.Sgf_game.from_bytes(sgf_src)
    except ValueError:
        raise Exception("bad sgf file")

    board_size = sgf_game.get_size()

    try:
        board, plays = sgf_moves.get_setup_and_moves(sgf_game)
    except ValueError as e:
        raise Exception(str(e))
    if move_number is not None:
        move_number = max(0, move_number-1)
        plays = plays[:move_number]


    for colour, move in plays:
        if move is None:
            continue
        row, col = move
        try:
            board.play(row, col, colour)
        except ValueError:
            raise Exception("illegal move in sgf file")
    return board, board_size





# n = 4
# text_annotations = pd.DataFrame({'x': np.arange(1, n),
#                                  'y': [2]*(n-1),
#                                  'label': np.arange(1, n)})
#
# print(text_annotations)


# In[188]:


def goban(board_size=19):
    hoshi = pd.DataFrame({'x0': [3,  3,  9,  3, 15, 15,  9, 15,  9],
                          'y0': [3,  9,  9, 15, 15,  9, 15,  3,  3]})
    hoshi = hoshi + 1

    grid_lines = pd.concat([
        pd.DataFrame({
            'x': [1]*board_size,
            'xend': [board_size]*board_size,
            'y': list(range(1, board_size+1)),
            'yend': list(range(1, board_size+1))}),
        pd.DataFrame({
            'x': list(range(1, board_size+1)),
            'xend': list(range(1, board_size+1)),
            'y': [1]*board_size,
            'yend': [board_size]*board_size
        })])

    return (ggplot() +
            geom_rect(aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax'),
                      data=pd.DataFrame({'xmin': [1], 'xmax': [board_size],
                                         'ymin': [1], 'ymax': [board_size]}),
                      color='black', fill='none') +
            geom_segment(aes(x='x', xend='xend', y='y', yend='yend'),
                         data=grid_lines,
                         color='black') +
            geom_point(aes('x0', 'y0'), data=hoshi, size=1.5))


def game_board_ggplot(board, board_size):
    stones = pd.DataFrame([[row + 1, col + 1, board.get(row, col)] for col in range(board_size) for row in range(board_size)],
                          columns=['x', 'y', 'color'])
    stones = stones.query("color == 'b' | color == 'w'")

    game = (goban(board_size) +
            geom_point(aes('x', 'y', col='color'), data=stones, size=8.9) +
            # geom_text(aes('x', 'y', label='label'), data=text_annotations, color='white', size=15, nudge_y=-0.05) +
            coord_fixed() +
            theme_void() +
            theme(
        text=element_text(family='Arial'),
        panel_grid_minor=element_blank(),
        panel_grid_major=element_blank(),
        panel_border=element_blank(),
        axis_ticks=element_blank(),
        axis_line=element_blank(),
        axis_title=element_blank(),
        axis_text=element_text(size=10),
    )
    )
    return game

@click.command()
@click.argument('sgf_file', nargs=1, type=click.File('rb'))
@click.argument('move_number', nargs=1)
@click.argument('pdf_filename', nargs=1)
def board_to_pdf(sgf_file, move_number, pdf_filename):
    move_number = int(move_number)
    board, board_size = read_board(sgf_file, move_number)
    p = game_board_ggplot(board, board_size)
    p.save(filename=pdf_filename, width = 6.4, height = 4.8, verbose = False)
    return 0

if __name__ == "__main__":
    sys.exit(board_to_pdf())  # pragma: no cover



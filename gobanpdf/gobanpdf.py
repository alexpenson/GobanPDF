# -*- coding: utf-8 -*-

"""Main module."""

from sgfmill import sgf
from sgfmill import sgf_moves
import pandas as pd
from plotnine import *
import numpy as np
import string
import sys
import click


def extract_board_table(sgf_file, move_number):
    sgf_src = sgf_file.read()
    sgf_file.close()
    try:
        sgf_game = sgf.Sgf_game.from_bytes(sgf_src)
    except ValueError:
        raise Exception("bad sgf file")

    board_size = sgf_game.get_size()

    # extract annotations/markings eg. A, B, square
    try:
        node = sgf_game.get_main_sequence()[move_number - 1]
    except ValueError as e:
        raise Exception(str(e))

    try:
        board, plays = sgf_moves.get_setup_and_moves(sgf_game)
    except ValueError as e:
        raise Exception(str(e))
    if move_number is not None:
        move_number = max(0, move_number - 1)
        plays = plays[:move_number]

    for colour, move in plays:
        if move is None:
            continue
        row, col = move
        try:
            board.play(row, col, colour)
        except ValueError:
            raise Exception("illegal move in sgf file")

    board_list = [[col + 1, row + 1, board.get(row, col)] for col in range(board_size) for row in range(board_size)]
    board_table = pd.DataFrame(board_list, columns=['x', 'y', 'stone'])

    # properties_with_a_value = ['LB']
    p = 'LB'
    text_list = list()
    if p in node.properties():
        text_list = [[i[0][1] + 1, i[0][0] + 1, 'text', i[1]] for i in node.get(p)]
    text_table = pd.DataFrame(text_list, columns=['x', 'y', 'annotation_type', 'value'])

    properties_without_a_value = ['SQ', 'MA']
    symbol_list = list()
    for p in properties_without_a_value:
        if p in node.properties():
            for i in node.get(p):
                row = i[0]
                col = i[1]
                symbol_list = symbol_list + [[col + 1, row + 1, 'symbol', p]]
    symbol_table = pd.DataFrame(symbol_list, columns=['x', 'y', 'annotation_type', 'value'])
    symbol_table

    # combine stones and annotations into a single table
    annotation_table = pd.concat([text_table, symbol_table])
    board_table = board_table.merge(annotation_table, on=['x', 'y'], how='outer')

    # set the color of the annotations
    board_table['annotation_color'] = np.where(
        (board_table['stone'].isnull()) | (board_table['stone'] == 'w'),
        'b',
        'w')

    return board_table, board_size


# n = 4
# text_annotations = pd.DataFrame({'x': np.arange(1, n),
#                                  'y': [2]*(n-1),
#                                  'label': np.arange(1, n)})
#
# print(text_annotations)


# In[188]:


def goban(board_size=19):
    hoshi = pd.DataFrame({'x0': [3, 3, 9, 3, 15, 15, 9, 15, 9],
                          'y0': [3, 9, 9, 15, 15, 9, 15, 3, 3]})
    hoshi = hoshi + 1

    grid_lines = pd.concat([
        pd.DataFrame({
            'x': [1] * board_size,
            'xend': [board_size] * board_size,
            'y': list(range(1, board_size + 1)),
            'yend': list(range(1, board_size + 1))}),
        pd.DataFrame({
            'x': list(range(1, board_size + 1)),
            'xend': list(range(1, board_size + 1)),
            'y': [1] * board_size,
            'yend': [board_size] * board_size
        })])

    letters = [string.ascii_uppercase[i]
               for i in list(range(0, len(string.ascii_uppercase)))]
    letters.remove('I')
    letter_labels = letters[0:board_size]

    kanji_labels = [u"\u4e00",
                    u"\u4e8c",
                    u"\u4e09",
                    u"\u56db",
                    u"\u4e94",
                    u"\u516d",
                    u"\u4e03",
                    u"\u516b",
                    u"\u4e5d",
                    u"\u5341",
                    u"\u5341\u4e00",
                    u"\u5341\u4e8c",
                    u"\u5341\u4e09",
                    u"\u5341\u56db",
                    u"\u5341\u4e94",
                    u"\u5341\u516d",
                    u"\u5341\u4e03",
                    u"\u5341\u516b",
                    u"\u5341\u4e5d"
                    ]
    kanji_labels.reverse()

    goban = (ggplot() +
             geom_rect(aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax'),
                       data=pd.DataFrame({'xmin': [1], 'xmax': [board_size],
                                          'ymin': [1], 'ymax': [board_size]}),
                       color='black', fill='none') +
             geom_segment(aes(x='x', xend='xend', y='y', yend='yend'),
                          data=grid_lines,
                          color='black') +
             geom_point(aes('x0', 'y0'), data=hoshi, size=1.5)
             )
    use_letter_labels = True
    if use_letter_labels:
        goban = (goban +
                 scale_x_continuous(labels=letter_labels, breaks=list(range(1, board_size + 1))) +
                 scale_y_continuous(breaks=list(range(1, board_size + 1)))
                 )
    else:
        goban = (goban +
                 scale_x_continuous(breaks=list(range(1, board_size + 1))) +
                 scale_y_continuous(labels=kanji_labels, breaks=list(range(1, board_size + 1)))
                 )

    return goban


def game_board_ggplot(board_table, board_size):

    game = (goban(board_size) +
            geom_point(aes('x', 'y', fill='stone'), data=board_table[~board_table['stone'].isnull()], size=8.9) +
            scale_color_manual(values={'b': 'black', 'w': 'white'}) +
            scale_fill_manual(values={'b': 'black', 'w': 'white'}) +
            scale_shape_manual(values={'SQ': 's', 'MA': 'x'}) +
            geom_text(aes('x', 'y', color='annotation_color', label='value'),
                      data=board_table[(~board_table.value.isnull()) & (board_table.annotation_type == 'text')],
                      size=15, nudge_y=-0.05) +
            geom_point(aes('x', 'y', fill='annotation_color', color='annotation_color', shape='value'),
                       data=board_table[(~board_table.value.isnull()) & (board_table.annotation_type == 'symbol')],
                       size=4) +
            coord_fixed() +
            theme_void() +
            theme(
                # text=element_text(family='MingLiU'),
                text=element_text(family='Arial'),
                panel_grid_minor=element_blank(),
                panel_grid_major=element_blank(),
                panel_border=element_blank(),
                axis_ticks=element_blank(),
                axis_line=element_blank(),
                axis_title=element_blank(),
                axis_text=element_text(size=10),
                legend_position='none'
            )
            )
    return game


@click.command()
@click.argument('sgf_file', nargs=1, type=click.File('rb'))
@click.argument('move_number', nargs=1)
@click.argument('pdf_filename', nargs=1)
def board_to_pdf(sgf_file, move_number, pdf_filename):
    """

    ⚫️⚪⚫️⚪

    GobanPDF

    """
    move_number = int(move_number)
    board_table, board_size = extract_board_table(sgf_file, move_number)
    p = game_board_ggplot(board_table, board_size)
    p.save(filename=pdf_filename, width=6.4, height=4.8, verbose=False)
    return 0


if __name__ == "__main__":
    sys.exit(board_to_pdf())  # pragma: no cover

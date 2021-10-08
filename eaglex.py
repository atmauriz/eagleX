import logging
import os
import shutil
import sqlite3
import stat
import sys

import chess
import chess.engine
import chess.pgn
import chess.svg

from flask import Flask, render_template
from flask_ask import Ask, statement, session, question, request

# shutil.copyfile("./stockfish_14_x64", "/tmp/stockfish_14_x64")
# os.chmod("/tmp/stockfish_14_x64", mode=0o755)
engine = chess.engine.SimpleEngine.popen_uci("/tmp/stockfish_14_x64")

board = chess.Board()
# board.push_uci(engine.play(board, chess.engine.Limit(time=0.1)).move.uci())
# board.push_uci(engine.play(board, chess.engine.Limit(time=0.1)).move.uci())
# board.push_uci(engine.play(board, chess.engine.Limit(time=0.1)).move.uci())
# board.push_uci(engine.play(board, chess.engine.Limit(time=0.1)).move.uci())
#
# f = open("board.SVG", "w")
# f.write(chess.svg.board(board, size=350))
# f.close()

app = Flask(__name__)
ask = Ask(app, '/')
eagle_x_version = "0.0.1"


@ask.launch
def launch():
    return question(render_template(
        "introduction.alexa",
        version=eagle_x_version
    ))


@ask.intent(
    'NewGameIntent',
    mapping={
        "player": "player",
        "level": "level"
    }
)
def new_game(level, player):
    logging.info(f"Start a new game with '{player}' at level '{level}'")

    # Engine configuration
    engine.configure({"Skill Level": int(level)})

    global board
    if player == "bianco":
        return question(render_template(
            "gameReadyBianco.alexa"
        ))
    if player == "nero":
        move = engine.play(board, chess.engine.Limit(time=0.1)).move.uci()
        board.push_uci(move)
        return question(render_template(
            "gameReadyNero.alexa", move=move
        ))


if __name__ == '__main__':
    app.run(debug=True)

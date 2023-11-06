from enum import Enum

class Color(Enum):
    Black = 0
    White = 1

class PieceTypes(Enum):
    Pawn = 1
    Rook = 2
    Knight = 3
    Bishop = 4
    Queen = 5
    King = 6

class Piece:
    def __init__(self, piece: PieceTypes, color: Color) -> None:
        self.piece = piece
        self.color = color

class Move:
    def __init__(self, piece: Piece, start_pos, end_pos) -> None:
        self.piece = piece
        self.star_pos = start_pos
        self.end_pos = end_pos
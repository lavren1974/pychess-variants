from __future__ import annotations

# -*- coding: utf-8 -*-
from ataxx import ATAXX_FENS
from const import CATEGORIES, MANCHU_R_FEN
from racingkings import RACINGKINGS_FENS

import logging
import re
import random

log = logging.getLogger(__name__)

try:
    import pyffish as sf

    sf.set_option("VariantPath", "variants.ini")
except ImportError:
    log.error("No pyffish module installed!")

try:
    import pyffish_alice as sf_alice
except ImportError:
    log.error("No pyffish-alice module installed!")

FEN_OK = sf.FEN_OK
NOTATION_SAN = sf.NOTATION_SAN
NOTATION_JANGGI = sf.NOTATION_JANGGI
NOTATION_XIANGQI_WXF = sf.NOTATION_XIANGQI_WXF
NOTATION_SHOGI_HODGES_NUMBER = sf.NOTATION_SHOGI_HODGES_NUMBER

WHITE, BLACK = 0, 1
FILES = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]

STANDARD_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

log = logging.getLogger(__name__)


def file_of(piece: str, rank: str) -> int:
    """
    Returns the 0-based file of the specified piece in the rank.
    Returns -1 if the piece is not in the rank.
    """
    pos = rank.find(piece)
    if pos >= 0:
        return sum(int(p) if p.isdigit() else 1 for p in rank[:pos])
    else:
        return -1


def modded_variant(variant: str, chess960: bool, initial_fen: str) -> str:
    """Some variants need to be treated differently by pyffish."""
    if not chess960 and variant in ("capablanca", "capahouse") and initial_fen:
        """
        E-file king in a Capablanca/Capahouse variant.
        The game will be treated as an Embassy game for the purpose of castling.
        The king starts on the e-file if it is on the e-file in the starting rank and can castle.
        """
        parts = initial_fen.split()
        ranks = parts[0].split("/")
        if (
            parts[2] != "-"
            and (("K" not in parts[2] and "Q" not in parts[2]) or file_of("K", ranks[7]) == 4)
            and (("k" not in parts[2] and "q" not in parts[2]) or file_of("k", ranks[0]) == 4)
        ):
            return "embassyhouse" if "house" in variant else "embassy"
    return variant


class FairyBoard:
    def __init__(
        self, variant: str, initial_fen="", chess960=False, count_started=0, disabled_fen=""
    ):
        self.variant = modded_variant(variant, chess960, initial_fen)
        self.sf = sf_alice if variant == "alice" else sf
        self.chess960 = chess960
        self.sfen = False
        self.show_promoted = variant in ("makruk", "makpong", "cambodian", "bughouse")
        self.legal_moves_need_history = variant in ("janggi", "ataxx")
        self.nnue = initial_fen == ""
        self.initial_fen = (
            initial_fen
            if initial_fen
            else FairyBoard.start_fen(variant, chess960 or variant == "ataxx", disabled_fen)
        )
        self.move_stack: list[str] = []
        self.ply = 0
        self.color = WHITE if self.initial_fen.split()[1] == "w" else BLACK
        self.fen = self.initial_fen
        self.manual_count = count_started != 0
        self.count_started = count_started

        if self.variant == "janggi":
            self.notation = NOTATION_JANGGI
        elif self.variant in CATEGORIES["shogi"]:
            self.notation = NOTATION_SHOGI_HODGES_NUMBER
        elif self.variant in (
            "xiangqi",
            "manchu",
            "minixiangqi",
        ):
            self.notation = NOTATION_XIANGQI_WXF
        else:
            self.notation = NOTATION_SAN

    @staticmethod
    def start_fen(variant, chess960=False, disabled_fen=""):
        if chess960:
            new_fen = FairyBoard.shuffle_start(variant)
            while new_fen == disabled_fen:
                new_fen = FairyBoard.shuffle_start(variant)
        elif variant == "alice":
            new_fen = sf_alice.start_fen("alice")
        else:
            new_fen = sf.start_fen(variant)

        if variant == "bughouse":
            return new_fen + " | " + new_fen
        elif variant == "manchu":
            return MANCHU_R_FEN
        else:
            return new_fen

    @property
    def initial_sfen(self):
        return self.sf.get_fen(self.variant, self.initial_fen, [], False, True)

    def push(self, move, append=True):
        try:
            # log.debug("move=%s, fen=%s", move, self.fen
            if append:
                self.move_stack.append(move)
                self.ply += 1
            self.color = WHITE if self.color == BLACK else BLACK
            self.fen = self.sf.get_fen(
                self.variant,
                self.fen,
                [move],
                self.chess960,
                self.sfen,
                self.show_promoted,
                self.count_started,
            )
        except Exception:
            self.pop()
            log.error(
                "sf.get_fen() failed on %s %s %s %s %s %s %s",
                self.variant,
                self.fen,
                move,
                self.chess960,
                self.sfen,
                self.show_promoted,
                self.count_started,
            )
            raise

    def pop(self):
        self.move_stack.pop()
        self.ply -= 1
        self.color = not self.color
        self.fen = self.sf.get_fen(
            self.variant,
            self.initial_fen,
            self.move_stack,
            self.chess960,
            self.sfen,
            self.show_promoted,
            self.count_started,
        )

    def get_san(self, move):
        return self.sf.get_san(self.variant, self.fen, move, self.chess960, self.notation)

    def has_legal_move(self):
        if self.legal_moves_need_history:
            return (
                len(
                    self.sf.legal_moves(
                        self.variant, self.initial_fen, self.move_stack, self.chess960
                    )
                )
                > 0
            )
        else:
            return len(self.sf.legal_moves(self.variant, self.fen, [], self.chess960)) > 0

    def legal_moves(self):
        # move legality can depend on history, e.g., passing and bikjang
        return self.sf.legal_moves(self.variant, self.initial_fen, self.move_stack, self.chess960)

    def legal_moves_no_history(self):
        # move legality can depend on history, but for bughouse we can't recreate history so we need this version
        return self.sf.legal_moves(self.variant, self.fen, [], self.chess960)

    def is_checked(self):
        return self.sf.gives_check(self.variant, self.fen, [], self.chess960)

    def insufficient_material(self):
        return self.sf.has_insufficient_material(self.variant, self.fen, [], self.chess960)

    def is_immediate_game_end(self):
        immediate_end, result = self.sf.is_immediate_game_end(
            self.variant, self.initial_fen, self.move_stack, self.chess960
        )
        return immediate_end, result

    def is_optional_game_end(self):
        return self.sf.is_optional_game_end(
            self.variant,
            self.initial_fen,
            self.move_stack,
            self.chess960,
            self.count_started,
        )

    def is_claimable_draw(self):
        optional_end, result = self.is_optional_game_end()
        return optional_end and result == 0

    def game_result(self):
        return self.sf.game_result(self.variant, self.initial_fen, self.move_stack, self.chess960)

    def game_result_no_history(self):
        return self.sf.game_result(self.variant, self.fen, [], self.chess960)

    def piece_to_partner(self, move):
        return self.sf.piece_to_partner(self.variant, self.fen, [move], self.chess960)

    def print_pos(self):
        print()
        uni_pieces = {
            "R": "♜",
            "N": "♞",
            "B": "♝",
            "Q": "♛",
            "K": "♚",
            "P": "♟",
            "r": "♖",
            "n": "♘",
            "b": "♗",
            "q": "♕",
            "k": "♔",
            "p": "♙",
            ".": "·",
            "/": "\n",
        }
        fen = self.fen
        if "[" in fen:
            board, rest = fen.split("[")
        else:
            board = fen.split()[0]
        board = board.replace("+", "")
        board = re.sub(r"\d", (lambda m: "." * int(m.group(0))), board)
        print("", " ".join(uni_pieces.get(p, p) for p in board))

    def janggi_setup(self, color):
        if color == "b":
            left = random.choice(("nb", "bn"))
            right = random.choice(("nb", "bn"))
            fen = "r%sa1a%sr/4k4/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/4K4/RNBA1ABNR w - - 0 1" % (
                left,
                right,
            )
        else:
            left = random.choice(("NB", "BN"))
            right = random.choice(("NB", "BN"))
            parts = self.initial_fen.split("/")
            parts[-1] = "R%sA1A%sR w - - 0 1" % (left, right)
            fen = "/".join(parts)
        print("-------new FEN", fen)
        self.initial_fen = fen
        self.fen = self.initial_fen

    @staticmethod
    def shuffle_start(variant):
        """Create random initial position.
        The king is placed somewhere between the two rooks.
        The bishops are placed on opposite-colored squares.
        Same for queen and archbishop in caparandom."""

        if variant == "ataxx":
            return random.choice(ATAXX_FENS)
        elif variant == "racingkings":
            return random.choice(RACINGKINGS_FENS)

        castl = ""
        capa = variant in ("capablanca", "capahouse")
        seirawan = variant in ("seirawan", "shouse")

        # https://www.chessvariants.com/contests/10/crc.html
        # we don't skip spositions that have unprotected pawns
        if capa:
            board = [""] * 10
            positions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            bright = [1, 3, 5, 7, 9]
            dark = [0, 2, 4, 6, 8]

            # 1. select queen or the archbishop to be placed first
            piece = random.choice("qa")

            # 2. place the selected 1st piece upon a bright square
            piece_pos = random.choice(bright)
            board[piece_pos] = piece
            positions.remove(piece_pos)
            bright.remove(piece_pos)

            # 3. place the selected 2nd piece upon a dark square
            piece_pos = random.choice(dark)
            board[piece_pos] = "q" if piece == "a" else "a"
            positions.remove(piece_pos)
            dark.remove(piece_pos)
        else:
            board = [""] * 8
            positions = [0, 1, 2, 3, 4, 5, 6, 7]
            bright = [1, 3, 5, 7]
            dark = [0, 2, 4, 6]

        # 4. one bishop has to be placed upon a bright square
        piece_pos = random.choice(bright)
        board[piece_pos] = "b"
        positions.remove(piece_pos)
        if seirawan:
            castl += FILES[piece_pos]

        # 5. one bishop has to be placed upon a dark square
        piece_pos = random.choice(dark)
        board[piece_pos] = "b"
        positions.remove(piece_pos)
        if seirawan:
            castl += FILES[piece_pos]

        if capa:
            # 6. one chancellor has to be placed upon a free square
            piece_pos = random.choice(positions)
            board[piece_pos] = "c"
            positions.remove(piece_pos)
        else:
            piece_pos = random.choice(positions)
            board[piece_pos] = "q"
            positions.remove(piece_pos)
            if seirawan:
                castl += FILES[piece_pos]

        # 7. one knight has to be placed upon a free square
        piece_pos = random.choice(positions)
        board[piece_pos] = "n"
        positions.remove(piece_pos)
        if seirawan:
            castl += FILES[piece_pos]

        # 8. one knight has to be placed upon a free square
        piece_pos = random.choice(positions)
        board[piece_pos] = "n"
        positions.remove(piece_pos)
        if seirawan:
            castl += FILES[piece_pos]

        # 9. set the king upon the center of three free squares left
        piece_pos = positions[1]
        board[piece_pos] = "k"

        # 10. set the rooks upon the both last free squares left
        piece_pos = positions[0]
        board[piece_pos] = "r"
        castl += "q" if seirawan else FILES[piece_pos]

        piece_pos = positions[2]
        board[piece_pos] = "r"
        castl += "k" if seirawan else FILES[piece_pos]

        fen = "".join(board)
        if capa:
            body = "/pppppppppp/10/10/10/10/PPPPPPPPPP/"
        else:
            body = "/pppppppp/8/8/8/8/PPPPPPPP/"

        if variant in ("crazyhouse", "capahouse", "bughouse"):
            holdings = "[]"
        elif seirawan:
            holdings = "[HEhe]"
        else:
            holdings = ""

        checks = "3+3 " if variant == "3check" else ""

        if variant == "horde":
            fen = (
                fen
                + "/pppppppp/8/1PP2PP1/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP"
                + " w "
                + castl
                + " - "
                + "0 1"
            )
        elif variant == "antichess":
            fen = fen + body + fen.upper() + " w - - 0 1"
        else:
            fen = (
                fen
                + body
                + fen.upper()
                + holdings
                + " w "
                + castl.upper()
                + castl
                + " - "
                + checks
                + "0 1"
            )
        return fen


def get_san_moves(variant, fen, mlist, chess960, notation):
    if variant == "alice":
        return sf_alice.get_san_moves(variant, fen, mlist, chess960, notation)
    else:
        return sf.get_san_moves(variant, fen, mlist, chess960, notation)


def validate_fen(fen, variant, chess960):
    if variant == "alice":
        return sf_alice.validate_fen(fen, variant, chess960)
    else:
        return sf.validate_fen(fen, variant, chess960)


if __name__ == "__main__":
    board = FairyBoard("shogi")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    board = FairyBoard("placement")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    board = FairyBoard("makruk")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    board = FairyBoard("sittuyin")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    board = FairyBoard("capablanca")
    print(board.fen)
    for move in (
        "e2e4",
        "d7d5",
        "e4d5",
        "c8i2",
        "d5d6",
        "i2j1",
        "d6d7",
        "j1e6",
        "d7e8c",
    ):
        print("push move", move)
        board.push(move)
        board.print_pos()
        print(board.fen)
    print(board.legal_moves())

    FEN = "r8r/1nbqkcabn1/ppppppp1pp/10/9P/10/10/PPPPPPPPp1/1NBQKC2N1/R5RAB1[p] b - - 0 5"
    board = FairyBoard("grandhouse", initial_fen=FEN)
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    board = FairyBoard("minishogi")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    board = FairyBoard("kyotoshogi")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())

    print("--- SHOGUN ---")
    print(FairyBoard.start_fen("shogun"))
    board = FairyBoard("shogun")
    for move in ("c2c4", "b8c6", "b2b4", "b7b5", "c4b5", "c6b8"):
        print("push move", move, board.get_san(move))
        if board.move_stack:
            print(
                "is_checked(), insuff material, draw?",
                board.is_checked(),
                board.insufficient_material(),
                board.is_claimable_draw(),
            )
        board.push(move)
        board.print_pos()
        print(board.fen)
        print(board.legal_moves())

    FEN = "rnb+fkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNB+FKBNR w KQkq - 0 1"
    board = FairyBoard("shogun", initial_fen=FEN)
    for move in (
        "c2c4",
        "h7h6",
        "c4c5",
        "h6h5",
        "c5c6+",
        "h8h6",
        "c6b7",
        "g7g6",
        "b7a8",
        "c8a6",
        "a8b7",
        "b8c6",
        "d1b3",
        "a6e2+",
        "b3b6",
        "e7e6",
        "b6c7",
        "P@h4",
        "c7c8",
        "e2c4",
        "f1c4",
        "h6h8",
        "c4e6+",
        "g8h6",
        "b2b4",
        "h8g8",
        "b4b5",
        "g6g5",
        "b5c6",
        "f8e7",
        "c6c7",
        "d7e6",
        "c8b8",
        "B@b6",
    ):
        print("push move", move, board.get_san(move))
        if board.move_stack:
            print(
                "is_checked(), insuff material, draw?",
                board.is_checked(),
                board.insufficient_material(),
                board.is_claimable_draw(),
            )
        board.push(move)
        board.print_pos()
        print(board.fen)
        print(board.legal_moves())

    board = FairyBoard("shouse")
    for move in (
        "e2e4",
        "E@d4",
        "g1f3",
        "e7e6",
        "b1c3",
        "H@b6",
        "d2d3",
        "f8b4",
        "c1e3",
        "d4b5",
        "e3b6",
        "a7b6",
        "d1d2e",
        "B@c6",
        "f1e2",
        "b5h5",
    ):
        print("push move", move, board.get_san(move))
        if board.move_stack:
            print(
                "is_checked(), insuff material, draw?",
                board.is_checked(),
                board.insufficient_material(),
                board.is_claimable_draw(),
            )
        board.push(move)
        board.print_pos()
        print(board.fen)
        print(board.legal_moves())

    board = FairyBoard("empire")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())
    print([board.get_san(move) for move in board.legal_moves()])

    board = FairyBoard("ordamirror")
    print(board.fen)
    board.print_pos()
    print(board.legal_moves())
    print([board.get_san(move) for move in board.legal_moves()])

    print(sf.version())
    print(sf.info())
    print(sf.variants())

    board = FairyBoard(
        "janggi",
        initial_fen="1nba2b2/4ka1R1/1cc6/p1p1p1p1p/9/9/P1P1P1PP1/1C5C1/4AK3/RNBA2BN1 w - - 0 1",
    )
    for move in (
        "h9f9",
        "e9f9",
        "f2f2",
    ):
        print("push move", move, board.get_san(move))
        if board.move_stack:
            print(
                "is_checked(), insuff material, draw?",
                board.is_checked(),
                board.insufficient_material(),
                board.is_claimable_draw(),
            )
        board.push(move)
        board.print_pos()
        print(board.fen)
        print(board.legal_moves())

import streamlit as st
import chess
import chess.engine
import chess.pgn
import matplotlib.pyplot as plt
import io

st.title("♟️ Chess Game Analyzer")
st.markdown("Upload a `.pgn` file to analyze the game with Stockfish and visualize the piece count.")

uploaded_file = st.file_uploader("Choose a PGN file", type="pgn")

if uploaded_file is not None:
    pgn_text = uploaded_file.read().decode("utf-8")
    game = chess.pgn.read_game(io.StringIO(pgn_text))
    board = game.board()

    # Load Stockfish engine
    try:
        engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    except FileNotFoundError:
        st.error("Stockfish engine not found. Please make sure it's installed and in PATH.")
        st.stop()

    piece_counts = []
    best_moves = []

    for move in game.mainline_moves():
        board.push(move)
        piece_counts.append(len(board.piece_map()))
        info = engine.analyse(board, chess.engine.Limit(time=0.5))
        if "pv" in info:
            best_moves.append(str(info["pv"][0]))
        else:
            best_moves.append("No suggestion")

    engine.quit()

    # Display best move suggestions
    st.subheader("Best Move Suggestions")
    for i, move in enumerate(best_moves, 1):
        st.write(f"Move {i}: {move}")

    # Plot piece count
    st.subheader("Piece Count Over Time")
    fig, ax = plt.subplots()
    ax.plot(piece_counts, marker='o')
    ax.set_xlabel("Move Number")
    ax.set_ylabel("Number of Pieces")
    ax.set_title("Pieces Remaining Through Game")
    ax.grid(True)
    st.pyplot(fig)

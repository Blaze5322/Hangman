import streamlit as st
import random
import time
import json

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="🎮 Hangman Pro",
    page_icon="🎯",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
body {
    background-color: #0f172a;
}

.big-title {
    font-size:50px;
    font-weight:bold;
    text-align:center;
    color:#38bdf8;
}

.word-box {
    font-size:40px;
    letter-spacing:12px;
    text-align:center;
    padding:20px;
}

.score-box {
    background:#1e293b;
    padding:15px;
    border-radius:12px;
    text-align:center;
    color:white;
}

.stButton>button {
    background-color:#38bdf8;
    color:black;
    border-radius:10px;
    height:3em;
    width:100%;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- WORD DATABASE ----------------

WORDS = {
    "Easy": [
        ("apple","fruit"),
        ("chair","furniture"),
        ("pizza","food"),
        ("tiger","animal"),
        ("water","drink")
    ],
    "Medium": [
        ("python","programming language"),
        ("galaxy","space object"),
        ("battery","energy source"),
        ("library","place with books"),
        ("diamond","precious stone")
    ],
    "Hard": [
        ("entrepreneur","business founder"),
        ("cryptocurrency","digital money"),
        ("metamorphosis","biological change"),
        ("photosynthesis","plant process"),
        ("architecture","building design")
    ]
}

# ---------------- SESSION STATE ----------------

def initialize_game():
    if "word" not in st.session_state:

        difficulty = st.session_state.get("difficulty","Easy")
        word, hint = random.choice(WORDS[difficulty])

        st.session_state.word = word.upper()
        st.session_state.hint = hint
        st.session_state.guessed = []
        st.session_state.wrong = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.session_state.game_over = False

initialize_game()

# ---------------- HANGMAN DRAWINGS ----------------

HANGMAN = [
"""
    
    


""",
"""
    
    |
    |
    |
""",
"""
    ----
    |
    |
    |
""",
"""
    ----
    |  O
    |
    |
""",
"""
    ----
    |  O
    |  |
    |
""",
"""
    ----
    |  O
    | /|
    |
""",
"""
    ----
    |  O
    | /|\\
    |
""",
"""
    ----
    |  O
    | /|\\
    | /
""",
"""
    ----
    |  O
    | /|\\
    | / \\
"""
]

# ---------------- TITLE ----------------

st.markdown('<p class="big-title">🎯 Hangman Pro</p>', unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.header("⚙️ Game Settings")

    difficulty = st.selectbox(
        "Select Difficulty",
        ["Easy","Medium","Hard"],
        key="difficulty"
    )

    if st.button("🔄 New Game"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ---------------- GAME LOGIC ----------------

word = st.session_state.word
guessed = st.session_state.guessed

display_word = " ".join(
    letter if letter in guessed else "_"
    for letter in word
)

# ---------------- LAYOUT ----------------

col1, col2 = st.columns([1,2])

with col1:
    st.code(HANGMAN[st.session_state.wrong])

with col2:
    st.markdown(f'<div class="word-box">{display_word}</div>', unsafe_allow_html=True)

    st.info(f"💡 Hint: {st.session_state.hint}")

# ---------------- TIMER ----------------

elapsed = int(time.time() - st.session_state.start_time)
st.write(f"⏱️ Time: {elapsed} sec")

# ---------------- KEYBOARD INPUT ----------------

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

cols = st.columns(13)

for i, letter in enumerate(alphabet):

    if cols[i % 13].button(letter):

        if letter not in guessed:

            st.session_state.guessed.append(letter)

            if letter not in word:
                st.session_state.wrong += 1
            else:
                st.session_state.score += 10

# ---------------- WIN CHECK ----------------

if all(l in guessed for l in word):
    st.success("🎉 YOU WON!")
    st.balloons()
    st.session_state.game_over = True

# ---------------- LOSE CHECK ----------------

if st.session_state.wrong >= len(HANGMAN)-1:
    st.error(f"💀 You Lost! Word was: {word}")
    st.session_state.game_over = True

# ---------------- SCOREBOARD ----------------

st.markdown(
    f"""
    <div class="score-box">
    🏆 Score: {st.session_state.score}<br>
    ❌ Wrong Attempts: {st.session_state.wrong}
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- LEADERBOARD SAVE ----------------

def save_score(score):

    try:
        with open("leaderboard.json","r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(score)

    with open("leaderboard.json","w") as f:
        json.dump(data,f)

if st.session_state.game_over:
    save_score(st.session_state.score)

# ---------------- LEADERBOARD DISPLAY ----------------

st.subheader("🏅 Leaderboard")

try:
    with open("leaderboard.json") as f:
        scores = json.load(f)
        scores.sort(reverse=True)

        for i,s in enumerate(scores[:5]):
            st.write(f"{i+1}. ⭐ {s}")
except:
    st.write("No scores yet.")

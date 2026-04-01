import streamlit as st
import random
import time

# --- إعدادات الصفحة والتصميم (CSS محاكي لـ Tkinter) ---
st.set_page_config(page_title="Quiz: Le mur de glace", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #2c3e50;
        color: white;
    }
    div.stButton > button {
        background-color: #34495e;
        color: white;
        border-radius: 5px;
        height: 3em;
        width: 100%;
        border: none;
        font-size: 18px;
    }
    div.stButton > button:hover {
        border: 1px solid #f39c12;
        color: #f39c12;
    }
    .question-text {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
    }
    .score-text {
        color: #f1c40f;
        font-size: 20px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- تهيئة الحالة (Session State) ---
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {
            "question": "Où se situe l’Antarctique ?",
            "options": ["Nord", "Centre", "Sud", "L'est"],
            "answer": "Sud"
        }
    ]
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'finished' not in st.session_state:
    st.session_state.finished = False
if 'answered_correctly' not in st.session_state:
    st.session_state.answered_correctly = False

# --- وظائف التحكم ---
def add_question():
    with st.expander("➕ Ajouter une Question"):
        with st.form("new_q_form", clear_on_submit=True):
            q = st.text_input("La question :")
            ans = st.text_input("Réponse correcte :")
            o2 = st.text_input("Fausse option 1 :")
            o3 = st.text_input("Fausse option 2 :")
            o4 = st.text_input("Fausse option 3 :")
            submit = st.form_submit_button("Ajouter")
            if submit and q and ans and o2 and o3 and o4:
                st.session_state.questions.append({
                    "question": q, "options": [ans, o2, o3, o4], "answer": ans
                })
                st.success("Question ajoutée !")

def next_question():
    st.session_state.current_question += 1
    st.session_state.attempts = 0
    st.session_state.answered_correctly = False
    if st.session_state.current_question >= len(st.session_state.questions):
        st.session_state.finished = True

def reset_game():
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.answered_correctly = False

# --- واجهة المستخدم ---
add_question()

if not st.session_state.finished:
    idx = st.session_state.current_question
    q_data = st.session_state.questions[idx]

    st.markdown(f'<p class="question-text">Question {idx + 1}: {q_data["question"]}</p>', unsafe_allow_html=True)

    # خلط الخيارات مرة واحدة فقط لكل سؤال
    if f"shuffle_{idx}" not in st.session_state:
        opts = list(q_data["options"])
        random.shuffle(opts)
        st.session_state[f"shuffle_{idx}"] = opts
    
    options = st.session_state[f"shuffle_{idx}"]

    # عرض الأزرار
    for option in options:
        # إذا تم الإجابة بشكل صحيح، نعطل الأزرار
        disabled = st.session_state.answered_correctly
        
        if st.button(option, key=f"btn_{idx}_{option}", disabled=disabled):
            if option == q_data["answer"]:
                if st.session_state.attempts == 0:
                    st.session_state.score += 1
                st.session_state.answered_correctly = True
                st.balloons()
                st.success(f"✅ {option} est correct ")
                st.success(f"Correct ! ✨")
                st.rerun()
            else:
                st.session_state.attempts += 1
                st.error(f"✖ {option} est incorrecte. Réessayez !")

    # زر السؤال التالي (يظهر فقط عند الإجابة الصحيحة)
    if st.session_state.answered_correctly:
        st.markdown("---")
        st.button("Suivant ➔", on_click=next_question)

else:
    # شاشة النهاية
    st.balloons()
    st.markdown(f"## Fin du Quiz !")
    st.markdown(f"### Score final: {st.session_state.score}/{len(st.session_state.questions)}")
    if st.button("Recommencer"):
        reset_game()
        st.rerun()

# عرض السكور في الأسفل
st.markdown("---")
st.markdown(f'<p class="score-text">Score: {st.session_state.score}</p>', unsafe_allow_html=True)
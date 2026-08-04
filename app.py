import streamlit as st
import pandas as pd
import joblib
from urllib import response
import os
from groq import Groq
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def create_pdf(name, age, goal, grammar_score, vocabulary_score, reading_score,
               predicted_level, ai_report):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b><font size=18>📚 LangChoice AI Report</font></b>", styles["Title"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"<b>Name:</b> {name}", styles["Normal"]))
    story.append(Paragraph(f"<b>Age Group:</b> {age}", styles["Normal"]))
    story.append(Paragraph(f"<b>Learning Goal:</b> {goal}", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Assessment Scores</b>", styles["Heading2"]))
    story.append(Paragraph(f"Grammar: {grammar_score}/100", styles["Normal"]))
    story.append(Paragraph(f"Vocabulary: {vocabulary_score}/100", styles["Normal"]))
    story.append(Paragraph(f"Reading: {reading_score}/100", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Predicted English Level</b>", styles["Heading2"]))
    story.append(Paragraph(predicted_level, styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>AI English Proficiency Report</b>", styles["Heading2"]))
    story.append(Paragraph(ai_report.replace("\n", "<br/>"), styles["Normal"]))

    doc.build(story)

    buffer.seek(0)
    return buffer

st.set_page_config(
    page_title="LangChoice AI",
    page_icon="📚",
    layout="centered"
)

st.title("📚 LangChoice AI")
st.write("English Proficiency Assessment")

# Load Model
rf_model = joblib.load("rf_model.pkl")
encoder = joblib.load("label_encoder.pkl")

st.write("""
Welcome to **LangChoice AI**!

This system evaluates your English proficiency using Machine Learning
and provides personalized feedback using AI.
""")

st.info("Click the button below to start your assessment.")

# Session State
if "start_assessment" not in st.session_state:
    st.session_state.start_assessment = False

st.header("👤 Candidate Information")

name = st.text_input("Full Name")

age = st.selectbox(
    "Age Group",
    ["15-18", "19-25", "26-35", "35+"]
)

goal = st.selectbox(
    "Learning Goal",
    [
        "IELTS",
        "PTE",
        "TOEFL",
        "Job Interview",
        "Study Abroad",
        "Improve Spoken English"
    ]
)

if st.button("🚀 Start Assessment"):
    if name.strip() == "":
        st.warning("Please enter your name.")
    else:
        st.session_state.start_assessment = True
        st.session_state.name = name
        st.session_state.age = age
        st.session_state.goal = goal


if st.session_state.start_assessment:
    # ===========================
    # Grammar Section
    # ===========================

    st.header("🟦 Grammar (4 Questions)")

    q1 = st.radio(
    "Q1. Choose the correct sentence.",
    [
        "A) She don't like coffee.",
        "B) She doesn't likes coffee.",
        "C) She doesn't like coffee.",
        "D) She not likes coffee."
    ],
    key="q1"
    )

    q2 = st.radio(
    "Q2. Choose the correct sentence.",
    [
        "A) He is an honest man.",
        "B) He is a honest man.",
        "C) He is the honest man.",
        "D) He is honest man."
    ],
    key="q2"
    )

    q3 = st.radio(
    "Q3. The meeting starts _____ 9:00 a.m.",
    [
        "A) in",
        "B) on",
        "C) at",
        "D) by"
    ],
    key="q3"
    )

    q4 = st.radio(
    "Q4. Choose the correct sentence.",
    [
        "A) I have seen that movie yesterday.",
        "B) I saw that movie yesterday.",
        "C) I seen that movie yesterday.",
        "D) I have saw that movie yesterday."
    ],
    key="q4"
    )
    


    # ===========================
    # Vocabulary Section
    # ===========================

    st.header("🟩 Vocabulary (4 Questions)")

    q5 = st.radio(
        "Q5. Choose the synonym of 'Reluctant'.",
        [
            "A) Eager",
            "B) Happy",
            "C) Unwilling",
            "D) Brave"
        ],
        key="q5"
    )

    q6 = st.radio(
        "Q6. The company plans to _____ its services next year.",
        [
            "A) reduce",
            "B) expand",
            "C) ignore",
            "D) remove"
        ],
        key="q6"
    )

    q7 = st.radio(
        "Q7. Choose the antonym of 'Scarce'.",
        [
            "A) Rare",
            "B) Limited",
            "C) Abundant",
            "D) Small"
        ],
        key="q7"
    )

    q8 = st.radio(
        "Q8. What does 'Hit the nail on the head' mean?",
        [
            "A) Hit someone with a hammer",
            "B) Say exactly the right thing",
            "C) Build something quickly",
            "D) Make a mistake"
        ],
        key="q8"
    )
    

    # ===========================
    # Reading Comprehension
    # ===========================

    st.header("🟨 Reading Comprehension")

    st.write("""
    **Passage**

    Emma recently joined an online learning platform to improve her communication
    skills for international job opportunities. Although she initially struggled
    with understanding different English accents, she gradually became more
    confident by participating in live discussions, watching recorded lectures,
    and receiving feedback from instructors. Instead of focusing only on
    memorising vocabulary, she practised using new words in conversations, which
    significantly improved both her fluency and confidence. After six months,
    she successfully passed an international English assessment and received
    a job offer from a multinational company.
    """)

    q9 = st.radio(
        "Q9. Why did Emma join the online learning platform?",
        [
            "A) To become a teacher",
            "B) To prepare for international job opportunities",
            "C) To learn computer programming",
            "D) To start her own business"
        ],
        key="q9"
    )

    q10 = st.radio(
        "Q10. Which activity contributed most to Emma's improvement?",
        [
            "A) Memorising vocabulary only",
            "B) Avoiding live discussions",
            "C) Practising new words in conversations",
            "D) Reading newspapers occasionally"
        ],
        key="q10"
    )

    q11 = st.radio(
        "Q11. Which statement is best supported by the passage?",
        [
            "A) Emma improved mainly because she studied grammar books.",
            "B) Emma avoided interacting with others.",
            "C) Consistent practice and feedback improved her communication skills.",
            "D) Emma learned English in only one month."
        ],
        key="q11"
    )

    q12 = st.radio(
        "Q12. What can be inferred from the passage?",
        [
            "A) Natural language practice can be more effective than memorisation alone.",
            "B) Grammar is unnecessary for learning English.",
            "C) Watching videos alone guarantees fluency.",
            "D) Everyone learns English at the same speed."
        ],
        key="q12"
    )


    # ===========================
    # Submit Button
    # ===========================

    if st.button("📊 Submit Assessment"):

        # Grammar Score
        grammar_score = 0

        if q1 == "C) She doesn't like coffee.":
            grammar_score += 25

        if q2 == "A) He is an honest man.":
            grammar_score += 25

        if q3 == "C) at":
            grammar_score += 25

        if q4 == "B) I saw that movie yesterday.":
            grammar_score += 25


        # Vocabulary Score
        vocabulary_score = 0

        if q5 == "C) Unwilling":
            vocabulary_score += 25

        if q6 == "B) expand":
            vocabulary_score += 25

        if q7 == "C) Abundant":
            vocabulary_score += 25

        if q8 == "B) Say exactly the right thing":
            vocabulary_score += 25


        # Reading Score
        reading_score = 0

        if q9 == "B) To prepare for international job opportunities":
            reading_score += 25

        if q10 == "C) Practising new words in conversations":
            reading_score += 25

        if q11 == "C) Consistent practice and feedback improved her communication skills.":
            reading_score += 25

        if q12 == "A) Natural language practice can be more effective than memorisation alone.":
            reading_score += 25


        # ML Prediction
        new_student = pd.DataFrame({
            "Grammar_Skills": [grammar_score],
            "Vocabulary_Skills": [vocabulary_score],
            "Reading_Test_Scores": [reading_score]
        })

        prediction = rf_model.predict(new_student)
        predicted_level = encoder.inverse_transform(prediction)[0]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📖 Grammar", f"{grammar_score}/100")

        with col2:
            st.metric("📚 Vocabulary", f"{vocabulary_score}/100")

        with col3:
            st.metric("📄 Reading", f"{reading_score}/100")

            st.info(f"🎯 Predicted English Level: **{predicted_level}**")
        

        # Get user information
        name = st.session_state.get("name", "Student")
        age = st.session_state.get("age", "")
        goal = st.session_state.get("goal", "")

        # Groq Client
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        prompt = f"""

        You are an English Language Assessment Expert.

        Student Information:
        - Name: {name}
        - Age Group: {age}
        - Learning Goal: {goal}

        Assessment Results:
        - Grammar Score: {grammar_score}/100
        - Vocabulary Score: {vocabulary_score}/100
        - Reading Score: {reading_score}/100

        Predicted English Proficiency Level:
        {predicted_level}

        Generate a personalized English proficiency report.

        The report must include:

        1. Greeting the student by name.
        2. Overall Performance.
        3. Strengths.
        4. Areas for Improvement.
        5. Personalized recommendations according to the student's learning goal.
        6. A simple 30-day study plan.
        7. A motivational conclusion.

        Write in simple, friendly English using headings and bullet points.

        """
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=700
        )       

            # Save AI report
        ai_report = response.choices[0].message.content

            # Show AI report
        st.header("🤖 AI English Proficiency Report")
        st.markdown(ai_report)

            # Create PDF
        pdf = create_pdf(
                name,
                age,
                goal,
                grammar_score,
                vocabulary_score,
                reading_score,
                predicted_level,
                ai_report
        )
        st.success("✅ Assessment completed and report generated successfully!")

            # Download button
        st.download_button(
                label="📄 Download PDF Report",
                data=pdf,
                file_name=f"{name}_LangChoice_Report.pdf",
                mime="application/pdf"
        )
# quiz_fetcher.py
from config import AI_KEYS
import random

def fetch_questions(section, exam_type):
    """
    Dummy: In real use, call the AI API.
    """
    questions = []
    for i in range(10):
        q = f"[{exam_type}-{section}] Question {i+1}?"
        options = ["A", "B", "C", "D"]
        answer = random.choice(options)
        questions.append({"question": q, "options": options, "answer": answer})
    return questions

import requests
import random
import os

def fetch_quiz(cid):
    try:
        # Get API key from environment
        api_key = os.environ.get("DEEPSEEK_KEY")
        if not api_key:
            raise ValueError("API key not configured")
            
        # Determine quiz type
        if "current_affairs" in cid:
            prompt = "Generate 10 current affairs questions from the last 24 hours with 4 options each"
        else:
            parts = cid.split('_')
            exam = parts[0].upper()
            section = " ".join(parts[1:]).title()
            prompt = f"Generate 10 {exam} {section} multiple-choice questions with 4 options each"

        # Call DeepSeek API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "You are a helpful exam assistant"},
                {"role": "user", "content": f"{prompt}. Format each as: Q: [question] A: [options] Correct: [letter]"}
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        
        # Parse response
        content = response.json()["choices"][0]["message"]["content"]
        return parse_questions(content)
        
    except Exception as e:
        print(f"API Error: {e}")
        return generate_dummy_questions(cid)

def parse_questions(content):
    questions = []
    current_q = {}
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith("Q:"):
            current_q = {"question": line[2:].strip(), "options": []}
        elif line.startswith("A:"):
            options = line[2:].split(';')
            current_q["options"] = [opt.strip() for opt in options if opt.strip()]
        elif line.startswith("Correct:"):
            current_q["answer"] = line.split(':')[1].strip()
            questions.append(current_q)
    
    return questions if questions else generate_dummy_questions("fallback")

def generate_dummy_questions(cid):
    return [{
        "question": f"[{cid}] Sample Question {i+1}?",
        "options": [f"Option A", f"Option B", f"Option C", f"Option D"],
        "answer": random.choice(["A", "B", "C", "D"])
    } for i in range(10)]

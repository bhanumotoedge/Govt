import requests
import random
import json
from config import AI_KEYS, NEWS_KEYS

def get_working_ai_key():
“”“Get the first available AI API key”””
for service, key in AI_KEYS.items():
if key:
return service, key
return None, None

def fetch_quiz(category_id):
“””
Fetch quiz questions based on category ID
Format: exam_section (e.g., ‘ssc_cgl_english’, ‘upsc_generalstudies’)
“””
try:
# Parse category
parts = category_id.split(’*’)
if len(parts) >= 2:
exam = parts[0]  # ssc, bank, upsc
if len(parts) >= 3:
exam_type = parts[1]  # cgl, chsl, po, clerk
section = ’*’.join(parts[2:])  # english, currentaffairs, etc.
else:
section = parts[1]  # for direct categories
exam_type = “”
else:
exam = category_id
exam_type = “”
section = “”

```
    # Get questions based on category
    if category_id == "current_affairs":
        return fetch_current_affairs_quiz()
    else:
        return generate_quiz_questions(exam, exam_type, section)
        
except Exception as e:
    print(f"❌ Error fetching quiz: {e}")
    return get_fallback_questions(category_id)
```

def generate_quiz_questions(exam, exam_type, section):
“”“Generate quiz questions using AI API”””
service, api_key = get_working_ai_key()

```
if not api_key:
    print("⚠️ No AI API key available, using fallback questions")
    return get_fallback_questions(f"{exam}_{exam_type}_{section}")

try:
    prompt = create_quiz_prompt(exam, exam_type, section)
    
    if service.startswith("gemini"):
        return call_gemini_api(api_key, prompt)
    elif service == "openrouter":
        return call_openrouter_api(api_key, prompt)
    elif service == "together":
        return call_together_api(api_key, prompt)
    elif service == "deepinfra":
        return call_deepinfra_api(api_key, prompt)
    elif service == "deepseek":
        return call_deepseek_api(api_key, prompt)
    else:
        return get_fallback_questions(f"{exam}_{exam_type}_{section}")
        
except Exception as e:
    print(f"❌ API call failed: {e}")
    return get_fallback_questions(f"{exam}_{exam_type}_{section}")
```

def create_quiz_prompt(exam, exam_type, section):
“”“Create appropriate prompt for quiz generation”””
exam_full = f”{exam.upper()} {exam_type.upper()}”.strip()
section_name = section.replace(‘currentaffairs’, ‘Current Affairs’).replace(‘aptitude’, ‘Quantitative Aptitude’).title()

```
prompt = f"""Generate 10 multiple choice questions for {exam_full} {section_name} section.
```

Requirements:

- Each question should have 4 options (A, B, C, D)
- Include the correct answer
- Questions should be appropriate for {exam_full} level
- Format as JSON array

Example format:
[
{{
“question”: “Question text here?”,
“options”: [“A) Option 1”, “B) Option 2”, “C) Option 3”, “D) Option 4”],
“answer”: “A”
}}
]

Generate exactly 10 questions now:”””

```
return prompt
```

def call_gemini_api(api_key, prompt):
“”“Call Google Gemini API”””
url = f”https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}”

```
data = {
    "contents": [{
        "parts": [{"text": prompt}]
    }]
}

response = requests.post(url, json=data, timeout=30)
response.raise_for_status()

result = response.json()
text = result['candidates'][0]['content']['parts'][0]['text']

return parse_ai_response(text)
```

def call_openrouter_api(api_key, prompt):
“”“Call OpenRouter API”””
url = “https://openrouter.ai/api/v1/chat/completions”

```
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "meta-llama/llama-3.1-8b-instruct:free",
    "messages": [{"role": "user", "content": prompt}]
}

response = requests.post(url, json=data, headers=headers, timeout=30)
response.raise_for_status()

result = response.json()
text = result['choices'][0]['message']['content']

return parse_ai_response(text)
```

def call_together_api(api_key, prompt):
“”“Call Together AI API”””
url = “https://api.together.xyz/v1/chat/completions”

```
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "meta-llama/Llama-3.2-3B-Instruct-Turbo",
    "messages": [{"role": "user", "content": prompt}]
}

response = requests.post(url, json=data, headers=headers, timeout=30)
response.raise_for_status()

result = response.json()
text = result['choices'][0]['message']['content']

return parse_ai_response(text)
```

def call_deepinfra_api(api_key, prompt):
“”“Call DeepInfra API”””
url = “https://api.deepinfra.com/v1/openai/chat/completions”

```
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "messages": [{"role": "user", "content": prompt}]
}

response = requests.post(url, json=data, headers=headers, timeout=30)
response.raise_for_status()

result = response.json()
text = result['choices'][0]['message']['content']

return parse_ai_response(text)
```

def call_deepseek_api(api_key, prompt):
“”“Call DeepSeek API”””
url = “https://api.deepseek.com/chat/completions”

```
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": prompt}]
}

response = requests.post(url, json=data, headers=headers, timeout=30)
response.raise_for_status()

result = response.json()
text = result['choices'][0]['message']['content']

return parse_ai_response(text)
```

def parse_ai_response(text):
“”“Parse AI response and extract questions”””
try:
# Try to find JSON in the response
start = text.find(’[’)
end = text.rfind(’]’) + 1

```
    if start != -1 and end > start:
        json_str = text[start:end]
        questions = json.loads(json_str)
        
        # Validate and format questions
        formatted_questions = []
        for q in questions[:10]:  # Limit to 10 questions
            if 'question' in q and 'options' in q and 'answer' in q:
                formatted_questions.append({
                    'question': q['question'],
                    'options': q['options'],
                    'answer': q['answer']
                })
        
        return formatted_questions if formatted_questions else get_fallback_questions("general")
    else:
        return get_fallback_questions("general")
        
except Exception as e:
    print(f"❌ Error parsing AI response: {e}")
    return get_fallback_questions("general")
```

def fetch_current_affairs_quiz():
“”“Fetch current affairs quiz from news APIs”””
gnews_key = NEWS_KEYS.get(“gnews”)
newsapi_key = NEWS_KEYS.get(“newsapi”)

```
try:
    if gnews_key:
        return fetch_gnews_quiz(gnews_key)
    elif newsapi_key:
        return fetch_newsapi_quiz(newsapi_key)
    else:
        return get_current_affairs_fallback()
except Exception as e:
    print(f"❌ Error fetching current affairs: {e}")
    return get_current_affairs_fallback()
```

def fetch_gnews_quiz(api_key):
“”“Fetch news from GNews API and generate quiz”””
url = f”https://gnews.io/api/v4/search?q=india&lang=en&country=in&max=10&apikey={api_key}”

```
response = requests.get(url, timeout=15)
response.raise_for_status()

data = response.json()
articles = data.get('articles', [])

# Generate questions from news articles
questions = []
for i, article in enumerate(articles[:10]):
    title = article.get('title', '')
    questions.append({
        'question': f"Recent news: What is the main topic of this headline: '{title[:100]}...'?",
        'options': ["A) Politics", "B) Economy", "C) Sports", "D) Technology"],
        'answer': "A"
    })

return questions
```

def fetch_newsapi_quiz(api_key):
“”“Fetch news from NewsAPI and generate quiz”””
url = f”https://newsapi.org/v2/top-headlines?country=in&pageSize=10&apiKey={api_key}”

```
response = requests.get(url, timeout=15)
response.raise_for_status()

data = response.json()
articles = data.get('articles', [])

# Generate questions from news articles
questions = []
for i, article in enumerate(articles[:10]):
    title = article.get('title', '')
    questions.append({
        'question': f"Current Affairs: {title}",
        'options': ["A) True", "B) False", "C) Partially True", "D) Cannot be determined"],
        'answer': "A"
    })

return questions
```

def get_fallback_questions(category):
“”“Generate fallback questions when APIs are unavailable”””
fallback_questions = {
‘english’: [
“What is the synonym of ‘abundant’?”,
“Choose the correct spelling:”,
“What is the antonym of ‘ancient’?”,
“Fill in the blank: She ___ to school every day.”,
“What is the past tense of ‘run’?”,
“Choose the correct sentence:”,
“What does ‘benevolent’ mean?”,
“Identify the noun in this sentence:”,
“What is the plural of ‘child’?”,
“Choose the correct preposition:”
],
‘reasoning’: [
“If A = 1, B = 2, C = 3, what is the value of ‘CAB’?”,
“Complete the series: 2, 4, 8, 16, ?”,
“If all roses are flowers and some flowers are red, then:”,
“What comes next: A, C, E, G, ?”,
“If today is Monday, what day will it be after 100 days?”,
“Complete: 1, 4, 9, 16, ?”,
“In a code language, if CAT = 3120, then DOG = ?”,
“Which number is different: 2, 4, 6, 9, 8?”,
“If P + Q = 10 and P - Q = 4, then P = ?”,
“Complete the pattern: AB, CD, EF, ?”
]
}

```
# Determine question type
question_type = 'english' if 'english' in category.lower() else 'reasoning'
base_questions = fallback_questions.get(question_type, fallback_questions['reasoning'])

questions = []
for i, q in enumerate(base_questions):
    options = ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"]
    answer = random.choice(["A", "B", "C", "D"])
    questions.append({
        'question': q,
        'options': options,
        'answer': answer
    })

return questions
```

def get_current_affairs_fallback():
“”“Fallback current affairs questions”””
questions = []
topics = [
“Who is the current Prime Minister of India?”,
“Which state recently implemented new education policy?”,
“What is the current repo rate set by RBI?”,
“Which Indian city hosted the recent G20 summit?”,
“Who won the latest Nobel Prize from India?”,
“Which space mission was recently launched by ISRO?”,
“What is the current GDP growth rate of India?”,
“Which new metro line was inaugurated recently?”,
“Who is the current President of India?”,
“Which Indian company recently went public?”
]

```
for topic in topics:
    options = ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"]
    answer = random.choice(["A", "B", "C", "D"])
    questions.append({
        'question': topic,
        'options': options,
        'answer': answer
    })

return questions
```

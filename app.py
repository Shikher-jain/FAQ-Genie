import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import os

from dotenv import load_dotenv

import google.generativeai as genai
from google.generativeai import GenerativeModel


load_dotenv() 

# Configure Gemini 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = GenerativeModel('gemini-1.5-flash')

# File system storage 
DATA_FILE = "faqs.json"
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            faq_store = json.load(f)
    except json.JSONDecodeError:
        faq_store = {}
else:
    faq_store = {}

def save_faq_store():
    """Save FAQs to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(faq_store, f, ensure_ascii=False, indent=2)

def get_text(url: str) -> str:
    """Fetch page and clean HTML, keeping <pre> text as-is."""
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
    except Exception as e:
        return f"[ERROR] {e}"

    soup = BeautifulSoup(r.text, "html.parser")

    # Extract <pre> separately
    pre_blocks = [pre.get_text("\n", strip=True) for pre in soup.find_all("pre")]

    # Remove unwanted tags
    for tag in soup(["script","style","nav","footer","header","form","aside","noscript","iframe","h1"]):
        tag.decompose()
    for tag in soup.find_all(attrs={"role":"navigation"}):
        tag.decompose()
    for tag in soup.find_all(attrs={"id":["footer","header","sidebar","navigation"]}):
        tag.decompose()

    # Remaining text
    main_text = soup.get_text(" ", strip=True)

    # Combine blocks
    full_text = main_text + "\n\n" + "\n\n".join(pre_blocks)
    return full_text.strip()

def extract_faq(text: str):
    """Use Gemini to extract FAQs in JSONL format (each line is valid JSONL)."""
    prompt = f"""
Extract FAQs from the following text in JSONL format.
Each line must be a valid JSON object with "Q" and "A" fields.

TEXT:
{text}
"""
    response = model.generate_content(prompt)
    lines = response.text.strip().split("\n")
    json_lines = []
    for line in lines:
        try:
            json_obj = json.loads(line)
            if "Q" in json_obj and "A" in json_obj:
                json_lines.append(json_obj)
        except json.JSONDecodeError:
            continue  # skip invalid lines
    return json_lines

def ask_question(faq_lines, question):
    """Use Gemini to answer a question from existing JSONL FAQs."""
    faq_text = "\n".join([json.dumps(f, ensure_ascii=False) for f in faq_lines])
    prompt = f"""
Answer the question using the following FAQs. 
If answer not found, say "Not available".

FAQs:
{faq_text}

Question: {question}
Answer:
"""
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI 
st.title("FAQ Genie")

url = st.text_input("Enter URL:")

if url:
    with st.spinner("Processing URL..."):
        # Check if URL is already processed
        if url in faq_store:
            st.info("This URL is already processed. FAQs loaded from file.")
            faqs = faq_store[url]
        else:
            text = get_text(url)
            if text.startswith("[ERROR]"):
                st.error(text)
                faqs = []
            else:
                faqs = extract_faq(text)
                faq_store[url] = faqs
                save_faq_store()
                st.success(f"Extraction done! {len(faqs)} QnA lines saved.")

        if faqs:
             
            # with st.expander("View Extracted FAQs"):
                # for line in faqs:
                #     st.text(json.dumps(line, ensure_ascii=False))

            # question = st.text_input("Ask a question about this URL:")

            question = st.selectbox("Select a question:", options=[line["Q"] for line in faqs])
            if question:
                answer = ask_question(faqs, question)
                st.subheader("Answer:")
                st.write(answer)

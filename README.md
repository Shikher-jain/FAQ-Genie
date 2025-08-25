

# **FAQ Genie**

This document outlines the features, setup, and usage of the **FAQ Genie**, an interactive FAQ extractor built with **Streamlit** and **Google Gemini AI**. Below is a structured summary of the key components:

## 🚀 Features

- **FAQ Extraction**: Extract FAQs from any webpage using AI.
- **Local Storage**: Store FAQs in **JSON/JSONL** format to prevent duplicate extractions.
- **Interactive Q&A**: Ask questions based on previously extracted FAQs.
- **Preservation of Code Blocks**: Maintain `<pre>` blocks (code or text) from websites.
- **AI Integration**: Utilize **Google Gemini AI** for generating structured Q&A.

## 🛠️ Requirements

To run the FAQ Genie, ensure you have the following:

- Python 3.10 or higher
- Streamlit
- Requests
- BeautifulSoup4
- Google Generative AI SDK (`google-generativeai`)
- `python-dotenv` for managing API keys

### Install Dependencies

You can install the required dependencies using the following command:

```bash
pip install streamlit requests beautifulsoup4 google-generativeai python-dotenv
```

## ⚙️ Setup

### Clone the Repository

To get started, clone the repository and navigate into the project directory:

```bash
git clone https://github.com/Shikher-jain/FAQ-Genie.git
cd FAQ-Genie
```

### Install Required Packages

Install the necessary packages by running:

```bash
pip install -r requirements.txt
```

### Create a .env File

In the project root, create a `.env` file and add your Google Gemini API key:

```
GEMINI_API_KEY=YOUR_GOOGLE_GENIE_API_KEY
```

### Run the Streamlit App

Launch the Streamlit application with the following command:

```bash
streamlit run app.py
```

---

## 📝 Usage

1. **Input URL**: Enter a URL in the input box provided in the app.
2. **Extract FAQs**: The app will extract FAQs and store them in `faqs.json`.
3. **Ask Questions**: You can select or type a question to receive answers based on the extracted FAQs.
4. **Load from JSON**: If the URL has been processed before, the app will load FAQs from the JSON file without making an API call.

## 🔐 Notes

- Ensure that your `.env` file is included in `.gitignore` to protect your API key.
- The app is designed to preserve previously extracted FAQs and will not overwrite them.

## 💡 Future Improvements

- Implement auto-update functionality for FAQs of existing URLs.
- Support for database storage (e.g., SQLite or MongoDB) for larger-scale applications.
- Enhance fine-tuning capabilities to improve answer accuracy.

This structured overview provides a clear understanding of the FAQ Genie, its setup, and its intended use.



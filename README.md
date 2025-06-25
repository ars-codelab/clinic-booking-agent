# Clinic Appointment Booking Agent (Browser + AI)

This project automates the process of booking a medical appointment at a specified clinic using an AI agent powered by the [`browser-use`](https://github.com/browser-use/browser-use) framework and Google's Gemini model via LangChain.

## ✨ Features

- Automates browser actions (login, form filling, selection, submission)
- Uses AI instructions to control behavior
- Customizable for different clinics or appointment types
- Built with `browser-use`, `LangChain`, and Gemini (`ChatGoogleGenerativeAI`)
- Captures and prints the result of the booking operation
- This can be scheduled in a cron job on a local or remote machine

## 🏥 Use Case

The agent is currently configured to book appointments at:

**Matsunobu Clinic**  
Booking URL: [https://yoyaku.atlink.jp/matsunobu/login?](https://yoyaku.atlink.jp/matsunobu/login?)

Example parameters:
- Patient: 川田太郎
- Department: 小児科
- Purpose: 再診（小児科）
- Date: today
- Time window: 13:00–16:30
- Symptoms: 発熱と風邪

## 🔧 How It Works - This needs to be modified in the LLM task prompt in agent.py based on the flow of your clinic

1. Launches a real browser (non-headless) via `browser-use`.
2. AI agent receives a structured task prompt with booking steps.
3. Interacts with the clinic website step-by-step to:
   - Log in with username and password
   - Navigate to appointment booking
   - Select department, purpose, and time
   - Fill out patient info and symptoms
   - Confirm and submit

## 🧪 Requirements

- Python 3.10+
- Chrome or Chromium installed
- Google API Key with access to Gemini model
 
## 🧪 requirements.txt
langchain
langchain-google-genai
browser-use
python-dotenv
playwright


### ⚠️ Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium --with-deps --no-shell
mkdir ./browser-user
cd ./browser-user
```

##🚀 Running the Agent
### Set your GOOGLE_API_KEY in a .env file:
```.env
GOOGLE_API_KEY=your_api_key_here
```

### Run the script:
```bash
python agent.py
```

## ⚠️ Notes
Captchas or unexpected pop-ups may interrupt the agent.

Headless mode is turned off for visibility and debugging.

Customize the task string to work with other clinics or booking sites.

## 📌 To Do
- Add retry logic for login failures
- Move username and password to .env or secrets
- Make parameters user-input driven (via CLI or form)

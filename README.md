# Clinic Appointment Booking Agent (Browser + AI)

This project automates the process of booking a medical appointment at a specified clinic using an AI agent powered by the [`browser-use`](https://github.com/browser-use/browser-use) framework and Google's Gemini model via LangChain.

# Problem We are trying to Solve
Every parent knows that sinking feeling when your child wakes up sick. But in Japan, the real stress begins when you try to book a clinic appointment.
Here's the reality: Most pediatric clinics open their online booking systems at 5-6 AM for same-day visits. Within 5 minutes, all morning slots are gone as working parents compete for appointments that let them get to the clinic, drop kids at daycare, and make it to work.
What if you could automate this step and reduce the stress of waking up early in the morning.
Traditional automation would require reverse-engineering each clinic's website, mapping every clickable element, and constantly updating code when sites change. Too brittle, too time-intensive. But what if we could describe our goal in plain English and let AI figure out the rest?
Enter Browser-use - an open-source tool that connects LLMs directly to browsers. Instead of coding specific workflows, you simply tell the agent what you want to accomplish. The AI understands your intent, navigates the website, and completes the task autonomously. We will use this to solve our problem.

## ✨ Features

- Automates browser actions (login, form filling, selection, submission)
- Uses AI instructions to control behavior
- Customizable for different clinics or appointment types
- Built with `browser-use`, `LangChain`, and Gemini (`ChatGoogleGenerativeAI`)
- Captures and prints the result of the booking operation
- This can be scheduled in a cron job on a local or remote machine

## 🏥 Use Case

The agent is currently configured to book appointments for a specific clinic in Japan, but the code can be easily modified for any clinic that has an online reservation form. As a user you will have to provide some input parameters that your clinic's site expects, and the agent will take care of the rest.

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

### Run the script with hard coded defaults:
```bash
python agent.py
```
### Run the script with optional user inputs which can be configured within angent.py - For example:
```bash
python agent.py -p "Taro Kawada" -u "12345" -pw "1234" -f "13:00" -l "16:00" -s "発熱と風邪"
```

## ⚠️ Notes
Captchas or unexpected pop-ups may interrupt the agent.
Headless mode is turned off for visibility and debugging.
Customize the task string to work with other clinics or booking sites.

## 📌 To Do
- Add retry logic for login failures
- Add a fallback logic to book appointment in a second clinic if the first one runs out of appointment slot
- Move username and password to .env or secrets
- Make parameters user-input driven (via CLI or form)

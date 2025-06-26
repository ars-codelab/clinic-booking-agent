# Clinic Appointment Booking Agent (Browser + AI)

This project leverages [`browser-use`](https://github.com/browser-use/browser-use) framework to automate the process of booking a medical appointment at a specified clinic. This approach can be easily extended for other purposes (e.g. booking concert tickets)

# Problem We are trying to Solve
In Japan, most pediatric clinics open their online booking systems at 5-6 AM for same-day visits. Within 5 minutes, all morning slots are gone as working parents, wake up early and compete for appointments that let them get to the clinic, drop kids at daycare, and make it to work.
Purpose of this agent is to automate this process so parents can get more sleep.
Traditional automation would require reverse-engineering each clinic's website, mapping every clickable element, and constantly updating code when sites change. 
We will use Browser-use - an open-source tool that connects LLMs directly to browsers. Instead of coding specific workflows, you simply tell the agent what you want to accomplish. The AI understands your intent, navigates the website, and completes the task autonomously. We will use this to solve our problem.

## ✨ Features (largely provided by browser-use)

- Automates browser actions (login, form filling, selection, submission)
- Uses AI instructions to control behavior
- Customizable for different clinics or appointment types
- Built with `browser-use`, `LangChain`, and Gemini (`ChatGoogleGenerativeAI`)
- Captures and prints the result of the booking operation
- This script is intended to be scheduled in a cron job on a local or remote machine

## 🔧 How The Agent Works

1. Launches a real browser (non-headless) via `browser-use`.
2. AI agent receives a structured task prompt with booking steps.
3. Interacts with the clinic website step-by-step to:
   - Log in with username and password
   - Navigate to appointment booking
   - Select department, purpose, and time
   - Fill out patient info and symptoms
   - Confirm and submit

## 🔧 What is needed to make it work?
Besides installing dependencies, to make this work, we just need 2 things. 
- A task prompt that describes what the goal/tasks are (e.g. help me book an appointment in this site for tomorrow XXpm using my username as XX and password as YY) along with information needed for booking (such as name, phone number, site url etc)
  
- An API key from your prefered LLM (e.g. OpenAI, Google, Anthropic)
This repo uses Google's GEMINI API. For Using other supported APIs refer to  [`browser-use documentation`](https://docs.browser-use.com/customize/supported-models)

## 🏥 Task Prompt
While you can give a high task prompts to the LLM and let it figure out how to achieve the task, you will end up burning a lot of tokens. To make this run more effeciently, go through the booking site once. Take some high level notes like "On first page, enter this, click here ... On send page ..". This significantly shortens the time it takes to complete the task. See agent.py for instructions for an example clinic. 
Note: For a simpler implementation, include information needed for booking (e.g. patient name, date of birth etc.) right into the prompt
You can also ask the user to provide this information during run-time (see agent.py)

Example User input parameters:
- Patient: Yamada Taro
- Department: 小児科
- Purpose: 再診（小児科）
- Date: today
- Time window: 13:00–16:30
- Symptoms: 発熱と風邪


## 🧪 Package Requirements

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
```

##🚀 Running the Agent
First create an empty .env file in your project folder, and then add your API keys
### Set your GOOGLE_API_KEY in a .env file:
```.env file
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

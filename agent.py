# ---1.Import dependencies ---
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini model wrapper via LangChain
from browser_use import Agent                              # Main Agent class from browser-use
from dotenv import load_dotenv                             # Load environment variables from .env
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig
from browser_use.controller.service import Controller      # Orchestrates actions with the browser
import argparse
from string import Template

# --- 2.Initialize the browser in headless or non-headless mode for visibility ---
browser = Browser(
    config=BrowserConfig(
        headless=False  # Set to True to run without opening a visible browser
    )
)

# --- 3.Create the controller for managing browser actions ---
controller = Controller()

# --- 4.Load environment variables (like GOOGLE_API_KEY) ---
### --- Make sure you have a .env file with line like GOOGLE_API_KEY=<your_api_key>
load_dotenv()

# --- 5.Initialize the language model using Gemini via LangChain ---
### ---For Using other supported APIs refer to https://docs.browser-use.com/customize/supported-models
llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite-preview-06-17')

# --- 6.Define the task prompt with instructions for the AI agent ---
### --We will create some user changeable parameters for making appointments

task_template = Template("""
Your goal is to help me successfully book a new appointment at a
specified clinic ${website} for a given {person}=${person} on a desired {date}=${date},
with a desired time range from ${first_time} to ${last_time}, and for a particular {purpose}=${purpose}.
Use these parameters:
{website} = ${website}
{person}  = ${person}
{user_name}  = ${user_name}
{password} = ${password}
{department} = ${department}
{purpose} = ${purpose}
{date} = ${date}
{first_time} = ${first_time}
{last_time} = ${last_time}
{symptoms} = ${symptoms}
{email} = ${email}


Please follow these steps:

1. Navigate to the clinic’s appointment registration website: {website}.

2. Log in using the provided {user_name} and {password}.

3. Accept or acknowledge any intermediate screens or prompts to proceed. Clear any captchas if they appear.

4. Look for a button or link labeled '予約登録' or similar, meaning 'New Reservation' and click it.

5. If any clinic department is asked, look for {department} or something similar. If any purpose '来院目的' is asked, look for {purpose} or something similar
In most cases, the department would be '予約登録' and purpose '再診（小児科）'

6. Select {date} at the bottom of the same page and click OK

7. In the next screen, choose the earliest available time slots within the
provided range ({first_time}–{last_time})

8. Enter the patient’s name {person} and {symptoms} if requested. And click OK.

9. Once you reach the final confirmation screen. Review the details carefully.
DO NOT Click the final submit or confirm button.ABORT. Show me the information you see on this final page
""")

# --- 7. Allow user to specify user details or fall back to default values ---

parser = argparse.ArgumentParser()
parser.add_argument("-w", "--website", default="https://yoyaku.atlink.jp/matsunobu/login?")
parser.add_argument("-p", "--person", default="Taro Kawada")
parser.add_argument("-u", "--user_name", default="taro@gmail.com")
parser.add_argument("-pw", "--password", default="123456")
parser.add_argument("-d", "--department", default="小児科")
parser.add_argument("-pu", "--purpose", default="再診（小児科）")
parser.add_argument("-dt", "--date", default="today")
parser.add_argument("-f", "--first_time", default="13:00")
parser.add_argument("-l", "--last_time", default="16:30")
parser.add_argument("-s", "--symptoms", default="発熱と風邪")
parser.add_argument("-e", "--email", help="Email address for notification")
args = parser.parse_args()

task = task_template.substitute(vars(args))
print(task)


# --- 8. Async entry point for running the agent---

import asyncio


async def main():
    # Create the browser-based AI agent
    agent = Agent(
        task=task,
        llm=llm,
        # use_vision=True,  # Enable this if using models with vision capabilities
        save_conversation_path="./logs/conversation",  # Save chat logs for review
        max_actions_per_step=5,                      # Limit actions per step to stay efficient
        controller=controller,
        browser=browser,
    )

    # Run the agent with a maximum of 40 steps before timeout
    result = await agent.run(max_steps=40)

    # Print final outcome or status
    print(result)

# --- Run the async loop ---
asyncio.run(main())


## --9. Fallback logic not implemented yet
#if "予約が完了しました" not in result:
# Try a different clinic

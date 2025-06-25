# --- Import dependencies ---
from langchain_google_genai import ChatGoogleGenerativeAI  # Gemini model wrapper via LangChain
from browser_use import Agent                              # Main Agent class from browser-use
from dotenv import load_dotenv                             # Load environment variables from .env
from browser_use.browser.browser import Browser, BrowserConfig, BrowserContextConfig
from browser_use.controller.service import Controller      # Orchestrates actions with the browser

# --- Initialize the browser in non-headless mode for visibility ---
browser = Browser(
    config=BrowserConfig(
        headless=False  # Set to True to run without opening a visible browser
    )
)

# --- Create the controller for managing browser actions ---
controller = Controller()

# --- Load environment variables (like GOOGLE_API_KEY) ---
load_dotenv()

# --- Initialize the language model using Gemini via LangChain ---
llm = ChatGoogleGenerativeAI(model='gemini-2.5-flash-lite-preview-06-17')

# --- Define the task prompt with instructions for the AI agent ---
# Replace parameter values as needed for other clinics or patients
task = """
Your goal is to help me successfully book a new appointment at a
specified clinic {website} for a given {person} on {date},
with a desired time range from {first_time} to {last_time}, and for a particular {purpose}.
Use these parameters:
{website} = https://yoyaku.atlink.jp/matsunobu/login?
{person}  = <Enter your kids name here e.g. Taro Kawada>
{user_name}  = <Enter the login user name e.g taro@gmail.com>
{password} = <Enter the login password e.g 123456>
{department} = <e.g. 小児科
{purpose} = <e.g. '再診（小児科）'
{date} = today
{first_time} = <e.g 13:00 AM>
{last_time} = <e.g 16:30 PM>
{symptoms} = <e.g. 発熱と風邪

Please follow these steps:

1. Navigate to the clinic’s appointment registration website: {website}.

2. Log in using the provided {user_name} and {password}.

3. Accept or acknowledge any intermediate screens or prompts to proceed. Clear any captchas if they appear.

4. Look for a button or link labeled '予約登録' or similar, meaning 'New Reservation' and click it.

5. If any clinic department is asked, look for {department} or something similar.

6. If any purpose '来院目的' is asked, look for {purpose} or something similar

7. In most cases, the department would be '予約登録' and purpose '再診（小児科）'

8. Select {date} and choose the earliest available time slots within the
provided range ({first_time}–{last_time}) under '再診（小児科)' if applicable.

9. Enter the patient’s name {person} and {symptoms} if requested.

10. Now Click the final submit or confirm button. Confirm whether reservation is successful.
Show me the information you see on this final page
"""

# --- Async entry point for running the agent ---
import asyncio

async def main():
    # Create the browser-based AI agent
    agent = Agent(
        task=task,
        llm=llm,
        # use_vision=True,  # Enable this if using models with vision capabilities
        save_conversation_path="logs/conversation",  # Save chat logs for review
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

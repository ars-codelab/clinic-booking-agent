# This creates a simple UI to configure our agent
### Can be run on both Streamlit Cloud (remotely) or on your local machines
### Collects appointment booking info (e.g., patient name, time window, symptoms).
### Saves this info to a run_config.json file in your GitHub repo.
### Updates the GitHub Actions cron workflow (.github/workflows/book.yml) to schedule the job at the chosen time.

import streamlit as st
import datetime
import json
from github import Github

st.title("🏥 Schedule Clinic Appointment")

# --- Form Inputs ---
person = st.text_input("👶 Patient Name", "ヤマダ タロ")
user_name = st.text_input("🧑‍💻 Login ID", "12345")
password = st.text_input("🔒 Password", type="password")
department = st.text_input("🏥 Department", "小児科")
purpose = st.text_input("📋 Visit Purpose", "再診（小児科）")
date = st.date_input("📅 Appointment Date", datetime.date.today())
first_time = st.text_input("⏰ Earliest Time", "13:00")
last_time = st.text_input("⏰ Latest Time", "16:00")
symptoms = st.text_input("🤒 Symptoms", "発熱と風邪")
email = st.text_input("📨 Notification Email", "your@gmail.com")
website = st.text_input("🌐 Clinic URL", "https://yoyaku.atlink.jp/matsunobu/login?")
run_time = st.time_input("⏱️ Run Agent At (JST)", datetime.time(5, 58))

# GitHub settings (you can hardcode this if desired)
repo_name = "ars-codelab/clinic-booking-agent"  # CHANGE THIS

# When the button is clicked
if st.button("✅ Schedule via GitHub Actions"):
    try:
        # 1. Convert time to UTC cron
        jst_hour = run_time.hour
        jst_minute = run_time.minute
        utc_hour = (jst_hour - 9) % 24
        cron_time = f"{jst_minute} {utc_hour} * * *"

        # 2. Construct run_config.json
        run_config = {
            "website": website,
            "person": person,
            "user_name": user_name,
            "password": password,
            "department": department,
            "purpose": purpose,
            "date": str(date),
            "first_time": first_time,
            "last_time": last_time,
            "symptoms": symptoms,
            "email": email,
        }

        # 3. Render workflow YAML
        book_yml = f"""
name: Scheduled Appointment Booking

on:
  schedule:
    - cron: '{cron_time}'
  workflow_dispatch:

jobs:
  run-booking:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run booking agent
        env:
          GOOGLE_API_KEY: ${{{{ secrets.GOOGLE_API_KEY }}}}
        run: |
          python git_agent.py
"""

        # 4. Push to GitHub
        g = Github(st.secrets["GITHUB_TOKEN"])
        repo = g.get_repo(repo_name)

        # Save run_config.json
        config_file = "run_config.json"
        try:
            contents = repo.get_contents(config_file)
            repo.update_file(contents.path, "Update config", json.dumps(run_config, ensure_ascii=False, indent=2), contents.sha)
        except:
            repo.create_file(config_file, "Create config", json.dumps(run_config, ensure_ascii=False, indent=2))

        # Save workflow
        workflow_file = ".github/workflows/book.yml"
        try:
            contents = repo.get_contents(workflow_file)
            repo.update_file(contents.path, "Update workflow", book_yml.strip(), contents.sha)
        except:
            repo.create_file(workflow_file, "Create workflow", book_yml.strip())

        st.success("🎉 Appointment script scheduled successfully via GitHub Actions!")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")

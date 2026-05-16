# 🤖 AI-Assisted-To-Do-Application  

## 💻 Project Overview
This project is an AI powered task management application built in Python. It allows users to create, manage, and organize tasks through a GUI, while also using an AI model (Google Gemini) to prioritize tasks, generate schedules, and provide productivity insights.  

## 👥 Team Members

| Name             | GitHub Handle | Email                                                             |
|------------------|---------------|--------------------------------------------------------------------------|
| Wen Fan    | @Wen-qqi | wqfan05@gmail.com            |
| Giovanna Baez   | @     | @gmail.com  |
---
## 🖥️ Setup and Installation
**1. Create Python Virtual Environment**<br>
```
python3 -m venv/env
```
- Some users may have to use python instead of python3<br/>

**2. Activate Virutal Environment**<br/>

For bash/macOS users:
```
source env/bin/activate
```

**3. Install Google Gemini Library**
```
pip install google-genai
```

**4. Input your API Key**
- Open **task.py** and go to line 17 for the code:
```
client = genai.Client(api_key="API_KEY")
```
- Replace **API_KEY** with your Google Gemini API Key
- If you don't have an API Key, create a key in [Google AI Studio](https://aistudio.google.com/api-keys)


## 🧠 Layout of the Code
project/ <br>
|<br>
├── task.py<br> 
├── tasks.csv </br>

## 📁 What Each File/Part Does 
### 1. task.py (Main File)
This file contains the entire application.
#### a. Imports and Configuration  
<ul>
  <li>Required Imports and Libraries:</li>
  <ul>
    <li>tkinter -> GUI Interface</li>
    <li>csv, json, os -> Data Storage and Handeling</li>
    <li>datetime, calendar -> date and calendar features</li>
    <li>google.genai -> AI Integration</li>
  </ul>
  <li>Set up the Google Gemini AI model (gemini-2.5-flash)</li>
  <li>Initializes the AI client</li>
</ul>  

#### b. Task class (data model)
This class represents a single task in the system.<br>
<br>
Each task stores:<br>
- description
- location
- due date
- category
- priority
- suggested time
- completed tasks














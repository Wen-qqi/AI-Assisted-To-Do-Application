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

## Running the file inside the Virtual Environment
**1. Type this command in the terminal to run the program:**
```
./task.py
```

**2. Deactivating the Virtual Environment**
```
deactivate
```

## 🧠 Layout of the Code
project/ <br>
|<br>
├── task.py<br> 
├── tasks.csv </br>

## 📁 What Each File/Part Does 
### 1. task.py (Main File)
This file contains the entire application.
#### a. Imports and Configuration  
- Imports with required libraries such as:
  * tkinter -> GUI Interface
  * csv, json, os -> Data Storage and Handeling
  * datetime, calendar -> Date and Calendar Features
  * google.genai -> AI Integration
- Sets up the Google Gemini AI model (gemini-2.5-flash)
- Initializes the API Client

#### b. Task class
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

#### c. TaskManager class
This class contains the backend logic<br/>

Responsibilities:<br>
- Load tasks from tasks.csv
- Save tasks back to the file
- Add new tasks
- Delete tasks
- Mark tasks as completed
- Communicate with the AI system

#### d. AI Features (inside TaskManager class)
**AI Prioritization**<br>
- Sends task data to Gemini
- Receives priority ranking (1-10)
- Updates each task accordingly

**AI Scheduling**<br>
- Send tasks to Gemini
- Receives suggested time blocks (morning/afternoon/evening)
- Assigns schedule to tasks

**AI Insights**<br>
- Sends task data to Gemini
- Gemini analyzes all tasks
- Opens a separate window
- Returns:
  * workload level
  * urgent tasks
  * overdue tasks
  * productivity advice

#### e. GUI Features (Tkinter Interface)
This section of code handles all of the user interactions with the interface<br/>

User interactions and UI:<br>
- Task input fields (description, location, due date, category)
- Buttons:
  * Add
  * Delete
  * Mark Completed
  * AI Prioritize
  * AI Schedule
  * AI Insights
  * Calendar View
  * Clear
- Table view using Treeview to display task
- Color-coding based on priority

#### f. Calendar View Module
- Opens a separate window
- Displays monthly calendar
- Maps tasks to due dates
- Show tasks to due dates
- Show tasks inside each day cell
- Uses color to represent priority levels

### 2. tasks.csv (Data Storage)
This file stores all tasks continuously<br/>

Each row contains:<br>
- description
- location
- due date
- category
- priority
- suggested time
- completion status <br/>

It allows the application to keep user data after closing and reload tasks when the user reopens the application











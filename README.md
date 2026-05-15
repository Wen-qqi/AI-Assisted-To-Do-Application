# AI-Assisted-To-Do-Application  

<h2>Project Overview</h2>  
This project is an AI powered task management application built in Python. It allows users to create, manage, and organize tasks through a GUI, while also using an AI model (Google Gemini) to prioritize tasks, generate schedules, and provide productivity insights.  
<h2>Layout of the Code</h2>
project/ <br>
|<br>
├── task.py<br> 
├── tasks.csv </br>

<h2>What Each File/Part Does</h2>  
<h3>1. task.py (Main File)</h3>  
This file contains the entire application.
<h4>a. Imports and Configuration</h4>  
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
<h4>b. Task class (data model)</h4>
This class represents a single task in the system.<br>
<br>
Each task stores:<br>
<ul>
  <li>description</li>
  <li>location</li>
  <li>due date</li>
  <li>category</li>
  <li>priority</li>
  <li>suggested time</li>
  <li>completion status</li>
</ul>














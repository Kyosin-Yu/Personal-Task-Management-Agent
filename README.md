# Personal Task Management Agent
AI-powered personal task management assistant built with Python, featuring Natural Language Understanding and Web Interface (Streamlit)

*Features*
- Natural Language Chat Interface
- Add task by describing task in plain English
- View, Update, Delete Tasks
- Mark tasks as complete
- Daily briefing with AI insights
- Smart priority scoring based on urgency and due date
- Overdue task detection
- Persistent storage with JSON

*Tech Stack*
- Python 3,14
- Streamlit - Web UI
- OpenRouter API - AI Model Access 
- "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free" - Language Model
- JSON - Data Persistence

*Project Structure*
- agent.py - AI agent brain and conversation loop
- app.py - Streamlit web interface
- task.py - Task data model
- storage.py - JSON file storage
- smartFeatures.py - Daily briefing and priority scoring
- aiHelper.py - AI helper function






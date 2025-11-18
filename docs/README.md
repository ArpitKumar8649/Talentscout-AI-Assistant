# 🤖 TalentScout AI Hiring Assistant

## Project Overview

An intelligent chatbot built with **Streamlit** and **Letta Agent** framework for automated candidate screening and technical assessment.

### ✨ Key Features

- 💬 **Intelligent Conversation Flow**: Context-aware interactions using Letta's stateful agents
- 📝 **Information Collection**: Gathers 7 essential candidate fields automatically
- 💻 **Tech Stack Assessment**: Generates 3-5 relevant technical questions
- 🧠 **Persistent Memory**: Maintains conversation context across interactions
- ✅ **Input Validation**: Validates email, phone, and other inputs
- 🔒 **GDPR Compliant**: Secure handling of sensitive candidate information

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **UI Framework** | Streamlit 1.32.0 |
| **AI Agent** | Letta Agent (Stateful LLM) |
| **Backend** | Python 3.10+ |
| **Data Storage** | MongoDB / JSON |
| **Testing** | Pytest |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Letta account and API credentials ([Sign up here](https://app.letta.com/))

### Installation

1. **Clone the repository** (or extract zip)
   ```bash
   cd /app
   ```

2. **Install dependencies**
   ```bash
   pip install -r streamlit_requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.streamlit.example .env.streamlit
   nano .env.streamlit  # Edit with your Letta credentials
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Access the app**
   - Opens automatically at `http://localhost:8501`

---

## ⚙️ Configuration

### Letta Credentials

You need three keys from Letta:

```env
LETTA_API_KEY=your_api_key          # From Letta dashboard
LETTA_AGENT_ID=agent-xxx-xxx        # Created in Phase 2
LETTA_PROJECT_ID=project-xxx-xxx    # From Letta project
```

**How to get credentials:**
1. Sign up at [https://app.letta.com/](https://app.letta.com/)
2. Create a new project
3. Get your API key from settings
4. Run `python scripts/init_letta_agent.py` to create agent

---

## 📚 Usage Guide

### Starting a Conversation

1. Open the app in your browser
2. Type "hello" or "start" in the chat input
3. Follow the assistant's prompts

### Information Collection Flow

The assistant will collect:
1. 👤 Full Name
2. 📧 Email Address
3. 📞 Phone Number
4. 📅 Years of Experience
5. 🎯 Desired Position(s)
6. 📍 Current Location
7. 💻 Tech Stack (languages, frameworks, databases, tools)

### Technical Assessment

After information collection:
- Agent analyzes your declared tech stack
- Generates 3-5 relevant technical questions
- Questions are tailored to your experience level
- Responses are recorded for review

### Ending Conversation

Type any exit keyword:
- `bye`, `goodbye`, `exit`, `quit`, `end`, `stop`

---

## 📋 Current Status

### ✅ Phase 1 Complete
- Project structure created
- Streamlit UI implemented
- Configuration management
- Utility functions
- Basic conversation flow (placeholder)

### 🔄 Upcoming Phases
- **Phase 2**: Letta Agent Integration
- **Phase 3**: Conversation Flow Logic
- **Phase 4**: Technical Question Generation
- **Phase 5**: UI/UX Enhancements
- **Phase 6**: Data Persistence
- **Phase 7**: Testing & Debugging
- **Phase 8**: Documentation & Demo

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_setup.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### Test Coverage

- Configuration loading
- Utility functions
- Input validation
- Helper methods

---

## 📁 Project Structure

```
/app/
├── streamlit_app.py              # Main application
├── streamlit_requirements.txt   # Dependencies
├── .env.streamlit               # Configuration
├── IMPLEMENTATION_PLAN.md       # Detailed plan
├── config/                      # Configuration
├── services/                    # Service layer
├── components/                  # UI components
├── utils/                       # Utilities
├── data/                        # Data storage
├── tests/                       # Test files
├── scripts/                     # Helper scripts
└── docs/                        # Documentation
```

---

## 👥 Contributing

This is an assignment project. Future enhancements welcome:
- Sentiment analysis integration
- Multilingual support
- Cloud deployment
- Advanced UI themes

---

## 📝 License

Developed for AI/ML Intern Assignment - TalentScout  
All rights reserved.

---

## 👤 Author

**AI/ML Intern Candidate**  
Built with Streamlit + Letta Agent Framework

---

## 🔗 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Letta Documentation](https://docs.letta.com/)
- [Python Best Practices](https://peps.python.org/pep-0008/)

# 🏗️ Application Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Community Cloud                 │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   Your Deployed App                    │  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │         streamlit_app.py (Main UI)             │  │  │
│  │  │  - ChatGPT-style interface                     │  │  │
│  │  │  - Real-time streaming display                 │  │  │
│  │  │  - Session management                          │  │  │
│  │  └───────────────┬─────────────────────────────────┘  │  │
│  │                  │                                      │  │
│  │                  ▼                                      │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │         services/letta_service.py              │  │  │
│  │  │  - Letta client initialization                 │  │  │
│  │  │  - Stream processing                           │  │  │
│  │  │  - Message handling                            │  │  │
│  │  └───────────────┬─────────────────────────────────┘  │  │
│  │                  │                                      │  │
│  │                  ▼                                      │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │         config/settings.py                     │  │  │
│  │  │  - Load Streamlit Secrets                      │  │  │
│  │  │  - Environment configuration                   │  │  │
│  │  │  - Fallback to .env for local dev              │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                                                         │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Secrets Manager (TOML)                    │  │
│  │  • LETTA_API_KEY                                       │  │
│  │  • LETTA_AGENT_ID                                      │  │
│  │  • LETTA_PROJECT_ID                                    │  │
│  │  • APP_TITLE, APP_ICON                                 │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        │ HTTPS API Calls
                        │
                        ▼
        ┌───────────────────────────────────┐
        │         Letta AI Platform         │
        │  https://api.letta.com            │
        │                                   │
        │  ┌─────────────────────────────┐ │
        │  │      Your AI Agent          │ │
        │  │  - GPT-5 Mini               │ │
        │  │  - Memory Management        │ │
        │  │  - Tool Calling             │ │
        │  │  - Streaming Responses      │ │
        │  └─────────────────────────────┘ │
        └───────────────────────────────────┘
```

---

## Data Flow

### User Message Flow

```
┌──────────────┐
│     User     │
│ Types Message│
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│  Streamlit UI        │
│  st.chat_input()     │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────────┐
│  services/letta_service.py   │
│  send_message_stream()       │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Letta AI API                │
│  POST /agents/{id}/messages  │
│  (streaming endpoint)        │
└──────┬───────────────────────┘
       │
       │ Stream chunks
       │
       ▼
┌──────────────────────────────┐
│  Process Stream Chunks       │
│  - reasoning_message         │
│  - assistant_message         │
│  - tool_call_message         │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│  Display in UI               │
│  - Reasoning in italic       │
│  - Assistant message         │
│  - Tool calls as badges      │
└──────────────────────────────┘
```

---

## Component Breakdown

### 1. Frontend Layer (`streamlit_app.py`)

**Responsibilities**:
- UI rendering and layout
- User input handling
- Message display and formatting
- Session state management
- Streaming display coordination

**Key Functions**:
```python
main()                    # Entry point
initialize_session_state() # Setup
connect_to_letta()        # Connection
handle_stream_response()  # Streaming
render_message()          # Display
render_sidebar()          # Status info
```

### 2. Service Layer (`services/letta_service.py`)

**Responsibilities**:
- Letta API client management
- Stream processing
- Message type handling
- Error handling

**Key Functions**:
```python
connect()                      # Initialize client
send_message_stream()          # Send & stream
_process_stream_chunk()        # Parse chunks
_handle_reasoning_message()    # Reasoning
_handle_assistant_message()    # Response
get_agent_info()               # Metadata
```

### 3. Configuration Layer (`config/settings.py`)

**Responsibilities**:
- Load Streamlit secrets
- Environment variable management
- Configuration validation
- Fallback handling

**Key Features**:
```python
Settings class            # Pydantic model
__init__()                # Load secrets
get_streamlit_secrets()   # Secret helper
```

### 4. Utility Layer (`utils/`)

**Files**:
- `constants.py`: Enums and constants
- `helpers.py`: Helper functions

**Purpose**:
- Shared functionality
- Data validation
- Text processing

---

## Deployment Architecture

### Local Development

```
Developer's Machine
├── .env.streamlit (local secrets)
├── Python 3.9+
└── streamlit run streamlit_app.py
    └── Runs on http://localhost:8501
```

### Streamlit Cloud Production

```
Streamlit Community Cloud
├── GitHub Repository (source code)
├── Secrets Manager (credentials)
├── Python Environment (auto-managed)
└── Public URL: https://your-app.streamlit.app
    └── HTTPS enabled by default
```

---

## Security Model

### Credentials Flow

```
Development:
.env.streamlit → config/settings.py → Application

Production:
Streamlit Secrets → config/settings.py → Application
```

### Protected Information

- ✅ API keys stored in Streamlit Secrets
- ✅ Never committed to Git
- ✅ Loaded at runtime only
- ✅ Not exposed in logs or UI

---

## Streaming Architecture

### Token-Level Streaming

```
Letta API
    │
    ├─ Chunk 1: reasoning_message
    │   └─ Display: "💭 Thinking about..."
    │
    ├─ Chunk 2: reasoning_message (continued)
    │   └─ Update: "💭 Thinking about... analyzing..."
    │
    ├─ Chunk 3: assistant_message
    │   └─ Display: "Hello"
    │
    ├─ Chunk 4: assistant_message (continued)
    │   └─ Update: "Hello, how"
    │
    └─ Chunk N: assistant_message (final)
        └─ Update: "Hello, how can I help you?"
```

### Message Accumulation

```python
# Accumulator pattern
message_accumulators = {
    'msg_id_1': {'type': 'reasoning', 'content': '...'},
    'msg_id_2': {'type': 'assistant', 'content': '...'}
}

# Updates on each chunk
for chunk in stream:
    msg_id = chunk.id
    accumulators[msg_id]['content'] += chunk.content
    display(accumulators[msg_id]['content'])
```

---

## File Structure

```
/app/
│
├── 📄 streamlit_app.py              # Main application (217 lines)
├── 📄 requirements.txt               # Dependencies (9 packages)
├── 📄 README.md                      # Project documentation
├── 📄 .gitignore                     # Git exclusions
├── 📄 .env.streamlit.example         # Credentials template
│
├── 📁 config/
│   ├── __init__.py
│   └── settings.py                   # Configuration manager
│
├── 📁 services/
│   ├── __init__.py
│   └── letta_service.py              # Letta integration (216 lines)
│
├── 📁 utils/
│   ├── __init__.py
│   ├── constants.py                  # Enums and constants
│   └── helpers.py                    # Helper functions
│
└── 📁 docs/
    ├── QUICK_START.md                # 5-minute guide
    ├── STREAMLIT_DEPLOYMENT_GUIDE.md # Detailed guide
    ├── DEPLOYMENT_CHECKLIST.md       # Progress tracker
    ├── DEPLOYMENT_SUMMARY.md         # Overview
    └── ARCHITECTURE.md               # This file
```

---

## Dependencies Graph

```
streamlit_app.py
    ├── imports streamlit
    ├── imports config.settings
    │   ├── imports pydantic_settings
    │   └── imports streamlit (for secrets)
    ├── imports services.letta_service
    │   ├── imports letta_client
    │   └── imports config.settings
    └── imports utils
        ├── constants
        └── helpers
```

---

## API Integration

### Letta API Endpoints Used

1. **Agent Retrieval**
   ```
   GET /agents/{agent_id}
   → Get agent information
   ```

2. **Message Streaming**
   ```
   POST /agents/{agent_id}/messages
   Body: {"role": "user", "content": "..."}
   Headers: {"stream_tokens": true}
   → Stream response chunks
   ```

### Response Types

| Type | Purpose | Display |
|------|---------|---------|
| `reasoning_message` | Agent's internal thoughts | Italic text with 💭 |
| `assistant_message` | Agent's response to user | Normal text |
| `tool_call_message` | Agent calling a tool | Badge with 🔧 |
| `tool_return_message` | Tool execution result | Hidden (internal) |
| `stop_reason` | End of response | Hidden (triggers completion) |
| `usage_statistics` | Token usage | Hidden (can log) |

---

## Performance Considerations

### Optimization Strategies

1. **Lazy Loading**: Settings loaded once on startup
2. **Stream Processing**: Display updates as chunks arrive
3. **Session State**: Minimize Streamlit reruns
4. **CSS Inline**: All styling in single CSS block

### Resource Usage

- **Memory**: ~50-100 MB (Streamlit + Letta client)
- **CPU**: Low (mostly I/O bound)
- **Network**: Depends on message frequency
- **Startup Time**: ~2-3 seconds

---

## Error Handling

### Levels of Error Handling

1. **Configuration Level**
   - Missing secrets → Default placeholders
   - Invalid format → Validation errors

2. **Connection Level**
   - API unavailable → Show error badge
   - Network timeout → Retry mechanism

3. **Runtime Level**
   - Stream errors → Display error message
   - Parsing errors → Log and continue

4. **User Level**
   - Clear error messages
   - Graceful degradation
   - Retry options

---

## Monitoring Points

### What to Monitor

1. **Connection Status**
   - Letta API connectivity
   - Agent availability

2. **Performance Metrics**
   - Response time
   - Token usage
   - Error rate

3. **User Analytics**
   - Message count
   - Session duration
   - Feature usage

---

## Scaling Considerations

### Current Capacity

- **Users**: Single user per session
- **Concurrency**: Limited by Streamlit Community Cloud
- **Messages**: Unlimited (within Letta limits)

### Future Scaling

- Multi-user support with authentication
- Database for conversation history
- Caching for agent responses
- Load balancing for high traffic

---

## Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| **Framework** | Streamlit | 1.32.0+ |
| **AI Agent** | Letta AI | Latest |
| **Language** | Python | 3.9+ |
| **Client** | letta-client | 0.1.324+ |
| **Validation** | Pydantic | 2.12.0+ |
| **Environment** | python-dotenv | 1.0.1+ |
| **Hosting** | Streamlit Cloud | Latest |

---

## Development vs Production

### Development Environment

```
Local Machine
├── .env.streamlit (file)
├── Python virtual environment
├── Hot reload enabled
└── Debug mode available
```

### Production Environment

```
Streamlit Cloud
├── Streamlit Secrets (encrypted)
├── Managed Python environment
├── Auto-deploy on git push
└── HTTPS by default
```

---

This architecture document provides a comprehensive overview of the application structure, data flow, and deployment model. Use it as a reference when modifying or extending the application.

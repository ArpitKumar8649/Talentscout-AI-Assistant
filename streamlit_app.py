"""
TalentScout AI Hiring Assistant - Phase 2 with Letta Integration
Streaming responses with real-time display
"""
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import os
import sys
import time

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv('.env.streamlit')

from config.settings import settings
from utils.constants import ConversationStage, REQUIRED_FIELDS
from utils.helpers import is_exit_keyword
from services.letta_service import letta_service

# Page configuration
st.set_page_config(
    page_title=settings.app_title,
    page_icon=settings.app_icon,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - ChatGPT Style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main App Background - Dark Theme */
    .stApp {
        background: #343541;
    }
    
    /* Main Content Area */
    section[data-testid="stAppViewContainer"] {
        background: #343541;
        padding-top: 0 !important;
    }
    
    /* Header Container - Responsive */
    .main-header {
        font-size: clamp(1.25rem, 4vw, 2rem);
        font-weight: 600;
        text-align: center;
        padding: 1.5rem 1rem 1rem 1rem;
        color: #ececf1;
        letter-spacing: -0.3px;
    }
    
    /* Typing Effect for TalentScout - Runs Once */
    .typing-text {
        display: inline-block;
        overflow: hidden;
        border-right: 3px solid #10a37f;
        white-space: nowrap;
        animation: typing 2s steps(12, end) 0.5s forwards,
                   blink-caret 0.75s step-end 0s 3;
        width: 0;
    }
    
    @keyframes typing {
        from {
            width: 0;
        }
        to {
            width: 100%;
            border-right-color: transparent;
        }
    }
    
    @keyframes blink-caret {
        from, to {
            border-right-color: transparent;
        }
        50% {
            border-right-color: #10a37f;
        }
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main-header {
            font-size: 1.25rem;
            padding: 1rem 0.5rem 0.75rem 0.5rem;
        }
        
        .typing-text {
            border-right-width: 2px;
        }
    }
    
    .sub-header {
        font-size: 0.875rem;
        color: #9ca3af;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 400;
    }
    
    /* Chat Messages - Dark Theme */
    .stChatMessage {
        border-radius: 0 !important;
        padding: 1.5rem 1rem !important;
        margin: 0 !important;
        border-bottom: 1px solid #444654 !important;
        box-shadow: none !important;
        background: transparent !important;
    }
    
    /* User Message Styling */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background-color: #343541 !important;
    }
    
    /* Assistant Message Styling */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background-color: #444654 !important;
    }
    
    /* Chat Message Content */
    .stChatMessage p {
        color: #ececf1 !important;
        font-size: 1rem;
        line-height: 1.75;
        font-weight: 400;
    }
    
    /* Force all text in messages to be visible */
    .stChatMessage div,
    .stChatMessage span,
    .stChatMessage p,
    .stChatMessage a {
        color: #ececf1 !important;
    }
    
    /* Override any inherited styles */
    [data-testid="stChatMessage"] * {
        color: #ececf1 !important;
    }
    
    /* Ensure markdown content is visible */
    .stMarkdown {
        color: #ececf1 !important;
    }
    
    .stMarkdown p,
    .stMarkdown div,
    .stMarkdown span {
        color: #ececf1 !important;
    }
    
    /* Avatar Styling */
    [data-testid="chatAvatarIcon-user"] {
        background: #19c37d !important;
    }
    
    [data-testid="chatAvatarIcon-assistant"] {
        background: #ab68ff !important;
    }
    
    /* Hide Sidebar Completely */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Hide sidebar collapse button */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Connection Status Badge - Inline Display */
    .connection-status {
        padding: 0.5rem 1rem;
        border-radius: 6px;
        margin: 0.5rem auto;
        font-size: 0.875rem;
        max-width: 400px;
        text-align: center;
    }
    
    .status-connected {
        background: #1a7f5a;
        border: 1px solid #2d9d6e;
        color: #d1fae5 !important;
    }
    
    .status-error {
        background: #8b1e1e;
        border: 1px solid #dc2626;
        color: #fee2e2 !important;
    }
    
    /* Reasoning Message - Dark Theme */
    .reasoning-message {
        font-style: italic;
        color: #9ca3af;
        background: #2d2d30;
        padding: 0.875rem 1rem;
        border-radius: 6px;
        border-left: 3px solid #6b7280;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .reasoning-message em {
        font-style: italic;
        color: #9ca3af;
    }
    
    /* Thinking Indicator with Shimmer Animation */
    .thinking-indicator {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem;
        background: #444654;
        border-radius: 8px;
        margin: 1rem 0;
        color: #9ca3af;
        font-size: 0.95rem;
        animation: shimmer 2s ease-in-out infinite;
    }
    
    @keyframes shimmer {
        0%, 100% {
            opacity: 0.5;
            transform: translateY(0px);
        }
        50% {
            opacity: 1;
            transform: translateY(-2px);
        }
    }
    
    .thinking-dots {
        display: inline-flex;
        gap: 0.25rem;
    }
    
    .thinking-dots span {
        width: 6px;
        height: 6px;
        background: #9ca3af;
        border-radius: 50%;
        animation: bounce 1.4s ease-in-out infinite;
    }
    
    .thinking-dots span:nth-child(1) {
        animation-delay: 0s;
    }
    
    .thinking-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .thinking-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes bounce {
        0%, 60%, 100% {
            transform: translateY(0);
            opacity: 0.5;
        }
        30% {
            transform: translateY(-10px);
            opacity: 1;
        }
    }
    
    /* Tool Call Badge - Dark Theme */
    .tool-call {
        background: #2d2d30;
        padding: 0.625rem 0.875rem;
        border-radius: 6px;
        border-left: 3px solid #60a5fa;
        margin: 0.5rem 0;
        font-size: 0.875rem;
        color: #93c5fd;
    }
    
    /* Chat Input Styling */
    .stChatInputContainer {
        border-top: 1px solid #444654;
        padding: 1rem 0;
        background: #343541;
    }
    
    /* Input field */
    .stChatInput input {
        background: #40414f !important;
        color: #ececf1 !important;
        border: 1px solid #565869 !important;
    }
    
    .stChatInput input::placeholder {
        color: #8e8ea0 !important;
    }
    
    /* Button Styling */
    .stButton button {
        background: #10a37f;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.625rem 1rem;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .stButton button:hover {
        background: #1a7f5a;
        box-shadow: 0 2px 8px rgba(16, 163, 127, 0.3);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #ececf1 !important;
        font-size: 1.5rem !important;
    }
    
    /* Remove Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #d1d5db;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #9ca3af;
    }
    
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'letta_connected' not in st.session_state:
        st.session_state.letta_connected = False
    
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    
    if 'current_reasoning' not in st.session_state:
        st.session_state.current_reasoning = ""
    
    if 'current_assistant' not in st.session_state:
        st.session_state.current_assistant = ""
    
    if 'agent_info' not in st.session_state:
        st.session_state.agent_info = None


def connect_to_letta():
    """Connect to Letta service"""
    if not st.session_state.letta_connected:
        with st.spinner("Connecting to Letta Agent..."):
            success = letta_service.connect()
            if success:
                st.session_state.letta_connected = True
                st.session_state.agent_info = letta_service.get_agent_info()
                return True
            else:
                st.error("❌ Failed to connect to Letta Agent. Check your credentials.")
                return False
    return True


def render_sidebar():
    """Render sidebar - ChatGPT style"""
    with st.sidebar:
        st.markdown('<p class="sidebar-header">🤖 Agent Status</p>', unsafe_allow_html=True)
        
        # Connection status
        if st.session_state.letta_connected:
            st.markdown("""
            <div class="connection-status status-connected">
                <strong>✓ AI Agent Connected</strong>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.agent_info:
                info = st.session_state.agent_info
                st.markdown(f"""
                <div class="info-card">
                    <p class="info-label">Agent ID</p>
                    <p class="info-value" style="font-size: 0.75rem; word-break: break-all;">{info.get('id', 'N/A')[:36]}...</p>
                </div>
                <div class="info-card">
                    <p class="info-label">Model</p>
                    <p class="info-value">{info.get('model', 'N/A')}</p>
                </div>
                <div class="info-card">
                    <p class="info-label">Agent Name</p>
                    <p class="info-value">{info.get('name', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="connection-status status-error">
                <strong>⚠ Connection Error</strong>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 1.5rem 0; border-top: 1px solid #4d4d4f;"></div>', unsafe_allow_html=True)
        
        # Conversation stats
        st.markdown('<p class="sidebar-header">💬 Conversation</p>', unsafe_allow_html=True)
        message_count = len([m for m in st.session_state.messages if m.get('role') == 'user'])
        st.metric("Messages Sent", message_count)
        
        st.markdown('<div style="margin: 1.5rem 0; border-top: 1px solid #4d4d4f;"></div>', unsafe_allow_html=True)
        
        # About section
        st.markdown('<p class="sidebar-header">ℹ️ Capabilities</p>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 0.875rem; line-height: 1.6; color: #ececf1;">
        • Candidate information gathering<br>
        • Technical skills assessment<br>
        • Context-aware conversations<br>
        • Real-time streaming responses
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 1.5rem 0; border-top: 1px solid #4d4d4f;"></div>', unsafe_allow_html=True)
        
        # Reset button
        if st.button("🔄 New Conversation", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def render_message(message):
    """Render a single message - for historical display"""
    role = message.get('role')
    content = message.get('content', '')
    
    if role == 'user':
        with st.chat_message("user"):
            st.write(content)
    
    elif role == 'assistant':
        # For historical messages, show reasoning in italic ONLY if present
        # Reasoning was already shown during streaming, so we include it here
        # for completeness when scrolling through history
        if message.get('reasoning') and message['reasoning'].strip():
            st.markdown(f"""
            <div class="reasoning-message">
                <em>💭 {message['reasoning']}</em>
            </div>
            """, unsafe_allow_html=True)
        
        # Show ONLY assistant message content - NO reasoning text mixed in
        if content and content.strip():
            with st.chat_message("assistant"):
                st.write(content)
        
        # Show tool calls if present
        if message.get('tool_calls') and len(message['tool_calls']) > 0:
            for tool_call in message['tool_calls']:
                st.markdown(f"""
                <div class="tool-call">
                    🔧 <strong>Tool:</strong> {tool_call}
                </div>
                """, unsafe_allow_html=True)


def handle_stream_response(user_message: str):
    """Handle streaming response from Letta"""
    try:
        # Track message components - keep reasoning and assistant SEPARATE
        reasoning_parts = {}
        assistant_parts = {}
        tool_calls = []
        
        # Create placeholders for streaming
        thinking_indicator = st.empty()
        reasoning_container = st.empty()
        assistant_container = st.empty()
        
        # Show thinking indicator
        thinking_indicator.markdown("""
        <div class="thinking-indicator">
            <div class="thinking-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
            <span>Agent is thinking...</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Stream responses
        for chunk in letta_service.send_message_stream(user_message, stream_tokens=True):
            chunk_type = chunk.get('type')
            
            if chunk_type == 'reasoning':
                # Remove thinking indicator once we start getting content
                thinking_indicator.empty()
                
                # Accumulate reasoning - keep SEPARATE from assistant
                msg_id = chunk.get('message_id', 'default')
                content = chunk.get('content', '')
                reasoning_parts[msg_id] = content
                
                # Display reasoning in italic ONLY - separate from message
                full_reasoning = ' '.join(reasoning_parts.values())
                if full_reasoning.strip():
                    reasoning_container.markdown(f"""
                    <div class="reasoning-message">
                        <em>💭 {full_reasoning}</em>
                    </div>
                    """, unsafe_allow_html=True)
            
            elif chunk_type == 'assistant':
                # Remove thinking indicator if still showing
                thinking_indicator.empty()
                
                # Accumulate assistant message
                msg_id = chunk.get('message_id', 'default')
                content = chunk.get('content', '')
                assistant_parts[msg_id] = content
                
                # Get full texts
                full_reasoning = ' '.join(reasoning_parts.values()).strip()
                full_assistant = ' '.join(assistant_parts.values()).strip()
                
                # CORE FIX: Remove reasoning text from assistant message if it's duplicated
                # Letta includes reasoning in assistant message, we need to extract only the response
                if full_reasoning and full_assistant.startswith(full_reasoning):
                    # Remove the reasoning part from assistant message
                    clean_assistant = full_assistant[len(full_reasoning):].strip()
                else:
                    clean_assistant = full_assistant
                
                # Display ONLY clean assistant message - without reasoning
                if clean_assistant:
                    with assistant_container:
                        with st.chat_message("assistant"):
                            st.write(clean_assistant)
            
            elif chunk_type == 'tool_call':
                tool_name = chunk.get('tool_name', 'unknown')
                tool_calls.append(tool_name)
                st.markdown(f"""
                <div class="tool-call">
                    🔧 <strong>Calling tool:</strong> {tool_name}
                </div>
                """, unsafe_allow_html=True)
            
            elif chunk_type == 'error':
                st.error(f"❌ {chunk.get('content', 'Unknown error')}")
                return None
        
        # Store complete message with reasoning removed from assistant content
        full_reasoning = ' '.join(reasoning_parts.values()).strip()
        full_assistant = ' '.join(assistant_parts.values()).strip()
        
        # Remove reasoning from assistant content if duplicated
        if full_reasoning and full_assistant.startswith(full_reasoning):
            clean_assistant = full_assistant[len(full_reasoning):].strip()
        else:
            clean_assistant = full_assistant
        
        # Return message with ONLY clean assistant content
        return {
            'role': 'assistant',
            'content': clean_assistant,  # Clean assistant message WITHOUT reasoning
            'reasoning': '',  # Don't store reasoning to avoid duplication on rerun
            'tool_calls': tool_calls
        }
    
    except Exception as e:
        st.error(f"❌ Error during streaming: {str(e)}")
        return None


def main():
    """Main application"""
    
    # Initialize
    initialize_session_state()
    
    # Header - ChatGPT Style with Typing Effect on TalentScout
    st.markdown(
        '''
        <h1 class="main-header">
            <span class="typing-text" id="typingText">TalentScout</span>
            <span> AI Hiring Assistant</span>
        </h1>
        <script>
            // Remove cursor after typing animation completes
            setTimeout(function() {
                var elem = document.getElementById('typingText');
                if (elem) {
                    elem.classList.add('typing-complete');
                }
            }, 3200);
        </script>
        ''', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="sub-header">AI-Powered Hiring Assistant with Real-Time Streaming</p>',
        unsafe_allow_html=True
    )
    
    # Connect to Letta
    if not st.session_state.letta_connected:
        connect_to_letta()
    
    # Render sidebar
    render_sidebar()
    
    # Main chat interface - no subtitle for cleaner look
    
    # Display chat history
    for message in st.session_state.messages:
        render_message(message)
    
    # Chat input
    if st.session_state.letta_connected:
        if prompt := st.chat_input("Type your message here...", key="user_input"):
            # Add user message to history
            st.session_state.messages.append({
                'role': 'user',
                'content': prompt
            })
            
            # Get streaming response (this will display reasoning and assistant message)
            response = handle_stream_response(prompt)
            
            # Store the response WITHOUT reasoning to avoid duplication
            # Reasoning was already displayed during streaming
            if response:
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': response['content'],  # Only store assistant content
                    'reasoning': '',  # Don't store reasoning to avoid showing twice
                    'tool_calls': response.get('tool_calls', [])
                })
            
            # Rerun to update chat history
            st.rerun()
    else:
        st.warning("⚠️ Please wait for Letta connection to be established.")


if __name__ == "__main__":
    main()

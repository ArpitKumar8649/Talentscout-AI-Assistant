"""
TalentScout AI Hiring Assistant - Main Streamlit Application
Phase 1: Basic Setup with Placeholder UI
"""
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import os
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
load_dotenv('.env.streamlit')

from config.settings import settings
from utils.constants import ConversationStage, REQUIRED_FIELDS
from utils.helpers import is_exit_keyword

# Page configuration
st.set_page_config(
    page_title=settings.app_title,
    page_icon=settings.app_icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main container background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Main header styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        letter-spacing: -0.5px;
    }
    
    /* Subheader styling */
    .sub-header {
        font-size: 1.1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    /* Chat container */
    .stChatMessage {
        border-radius: 12px !important;
        padding: 1.2rem !important;
        margin: 0.8rem 0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        animation: slideIn 0.3s ease-out;
    }
    
    /* User message */
    [data-testid="stChatMessageContent"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-right: 1px solid #e2e8f0;
    }
    
    .sidebar-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Info card */
    .info-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease;
    }
    
    .info-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    
    .info-label {
        font-weight: 600;
        color: #475569;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.3rem;
    }
    
    .info-value {
        color: #1e293b;
        font-size: 1.1rem;
        font-weight: 500;
        margin-top: 0.3rem;
    }
    
    /* Progress bar styling */
    .progress-container {
        background: #e2e8f0;
        border-radius: 20px;
        height: 24px;
        margin: 1.5rem 0;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 20px;
        transition: width 0.5s ease;
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.3rem;
        transition: all 0.2s ease;
    }
    
    .badge-pending {
        background: linear-gradient(135deg, #fff7ed 0%, #fed7aa 100%);
        color: #c2410c;
        border: 1px solid #fdba74;
    }
    
    .badge-collected {
        background: linear-gradient(135deg, #f0fdf4 0%, #bbf7d0 100%);
        color: #15803d;
        border: 1px solid #86efac;
    }
    
    /* Info box */
    .info-box {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 5px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.1);
    }
    
    .info-box h3 {
        color: #1e40af;
        margin-top: 0;
        font-size: 1.3rem;
        font-weight: 700;
    }
    
    .info-box p, .info-box ul {
        color: #1e3a8a;
        line-height: 1.6;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 5px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px rgba(245, 158, 11, 0.1);
    }
    
    .warning-box h4 {
        color: #92400e;
        margin-top: 0;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .warning-box p, .warning-box ul {
        color: #78350f;
        line-height: 1.6;
    }
    
    /* Chat input */
    .stChatInput {
        border-radius: 12px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Animations */
    @keyframes slideIn {
        from { 
            opacity: 0; 
            transform: translateX(-20px);
        }
        to { 
            opacity: 1; 
            transform: translateX(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 12px !important;
        padding: 1rem 1.5rem !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'candidate_data' not in st.session_state:
        st.session_state.candidate_data = {
            'full_name': None,
            'email': None,
            'phone': None,
            'years_experience': None,
            'desired_positions': None,
            'current_location': None,
            'tech_stack': None
        }
    
    if 'conversation_stage' not in st.session_state:
        st.session_state.conversation_stage = ConversationStage.GREETING.value
    
    if 'letta_connected' not in st.session_state:
        st.session_state.letta_connected = False
    
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False


def render_sidebar():
    """Render sidebar with candidate summary"""
    with st.sidebar:
        st.markdown('<p class="sidebar-header">📋 Candidate Summary</p>', unsafe_allow_html=True)
        
        # Progress indicator
        collected_fields = sum(1 for v in st.session_state.candidate_data.values() if v is not None)
        total_fields = len(REQUIRED_FIELDS)
        progress_percentage = (collected_fields / total_fields) * 100
        
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <p style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">
                Information Collected: {collected_fields}/{total_fields}
            </p>
            <div class="progress-container">
                <div class="progress-bar" style="width: {progress_percentage}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display collected information
        st.markdown("---")
        
        if collected_fields == 0:
            st.info("💬 Start the conversation to collect candidate information.")
        else:
            for field, value in st.session_state.candidate_data.items():
                field_name = field.replace('_', ' ').title()
                if value:
                    st.markdown(f"""
                    <div class="info-card">
                        <p class="info-label">{field_name}</p>
                        <p class="info-value">{value}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <span class="status-badge badge-pending">{field_name}: Pending</span>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # About section
        st.subheader("ℹ️ About")
        st.markdown("""
        This AI assistant helps with initial candidate screening by:
        - 📝 Gathering essential information
        - 💻 Assessing technical skills  
        - 🎯 Generating relevant questions
        - 🤝 Maintaining professional conversation
        """)
        
        st.markdown("---")
        
        # Status section
        st.subheader("⚙️ Status")
        if st.session_state.letta_connected:
            st.success("✅ Letta Agent Connected")
        else:
            st.warning("⚠️ Letta Integration Pending")
            st.info("Phase 2 will integrate Letta agent")
        
        # Reset button
        if st.button("🔄 Reset Conversation", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def render_welcome_message():
    """Render welcome message for new conversations"""
    st.markdown("""
    <div class="info-box">
        <h3>👋 Welcome to TalentScout AI Hiring Assistant!</h3>
        <p style="font-size: 1.05rem; margin: 1rem 0;">I'm here to help with your initial candidate screening. I'll:</p>
        <ul style="font-size: 1rem; line-height: 1.8;">
            <li>📝 Collect your basic information</li>
            <li>💻 Understand your technical expertise</li>
            <li>🎯 Ask relevant technical questions</li>
            <li>✨ Provide a smooth interview experience</li>
        </ul>
        <p style="font-size: 1.1rem; margin-top: 1.5rem;"><strong>✨ Ready to begin? Type 'hello' or 'start' to get started!</strong></p>
    </div>
    """, unsafe_allow_html=True)


def render_phase_warning():
    """Render warning about Phase 1 limitations"""
    st.markdown("""
    <div class="warning-box">
        <h4>⚠️ Phase 1: Development Mode</h4>
        <p style="font-size: 1rem; margin: 1rem 0;">Currently showing placeholder functionality. Features coming in next phases:</p>
        <ul style="font-size: 0.95rem; line-height: 1.8;">
            <li><strong>Phase 2:</strong> 🤖 Letta Agent Integration</li>
            <li><strong>Phase 3:</strong> 💬 Conversation Flow Logic</li>
            <li><strong>Phase 4:</strong> 🎯 Technical Question Generation</li>
        </ul>
        <p style="font-size: 0.95rem; margin-top: 1rem;"><em>💡 The chatbot will provide intelligent responses once Letta credentials are configured.</em></p>
    </div>
    """, unsafe_allow_html=True)


def handle_user_input(user_input: str):
    """Handle user input and generate responses (Phase 1 placeholder)"""
    
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # Check for exit keywords
    if is_exit_keyword(user_input):
        response = """
        Thank you for your time! Your information has been recorded. 
        Our team will review your profile and get back to you soon.
        
        Have a great day! 👋
        """
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        return
    
    # Placeholder responses for Phase 1
    if not st.session_state.conversation_started:
        response = """
        Great! Let's get started with your screening interview.
        
        First, could you please tell me your full name?
        """
        st.session_state.conversation_started = True
    else:
        # Generate contextual placeholder responses
        message_count = len([m for m in st.session_state.messages if m['role'] == 'user'])
        
        if message_count == 2:
            response = "Thank you! Now, what's your email address?"
        elif message_count == 3:
            response = "Perfect! Could you share your phone number?"
        elif message_count == 4:
            response = "Got it! How many years of experience do you have?"
        elif message_count == 5:
            response = "Excellent! What position(s) are you interested in?"
        elif message_count == 6:
            response = "Great! Where are you currently located?"
        elif message_count == 7:
            response = """
            Perfect! Now, let's talk about your technical skills.
            
            Could you please list your tech stack? Include:
            - Programming languages (e.g., Python, JavaScript)
            - Frameworks (e.g., React, Django)
            - Databases (e.g., MongoDB, PostgreSQL)
            - Tools (e.g., Docker, AWS)
            """
        else:
            response = """
            🔧 **Phase 1 Placeholder Response**
            
            In Phase 2, the Letta agent will:
            - Understand your responses contextually
            - Update memory blocks automatically  
            - Generate relevant technical questions
            - Maintain natural conversation flow
            
            For now, I'm collecting your input and demonstrating the UI!
            Type 'bye' to end the conversation.
            """
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })


def main():
    """Main application entry point"""
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown(
        f'<h1 class="main-header">{settings.app_icon} {settings.app_title}</h1>', 
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="sub-header">Powered by Letta Agent Framework 🤖</p>',
        unsafe_allow_html=True
    )
    st.markdown('---')
    
    # Render sidebar
    render_sidebar()
    
    # Main chat interface
    st.subheader("💬 Chat Interface")
    
    # Show phase warning
    render_phase_warning()
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        if len(st.session_state.messages) == 0:
            render_welcome_message()
        else:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here...", key="user_input"):
        # Display user message immediately
        with st.chat_message("user"):
            st.write(prompt)
        
        # Process and respond
        handle_user_input(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.write(st.session_state.messages[-1]["content"])
        
        # Rerun to update UI
        st.rerun()


if __name__ == "__main__":
    main()

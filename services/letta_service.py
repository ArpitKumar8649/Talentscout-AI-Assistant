"""Service for interacting with Letta Agent with streaming support"""
from letta_client import Letta
from typing import Optional, Dict, List, Generator, Any
import os
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class LettaService:
    """Service for interacting with Letta Agent with streaming capabilities"""
    
    def __init__(self):
        """Initialize Letta client"""
        self.client: Optional[Letta] = None
        self.agent_id: str = settings.letta_agent_id
        self.is_connected: bool = False
    
    def connect(self) -> bool:
        """Connect to Letta API"""
        try:
            self.client = Letta(
                token=settings.letta_api_key,
                base_url=settings.letta_base_url
            )
            self.is_connected = True
            logger.info(f"Connected to Letta API at {settings.letta_base_url}")
            logger.info(f"Using agent ID: {self.agent_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Letta: {e}")
            self.is_connected = False
            return False
    
    def send_message_stream(self, message: str, stream_tokens: bool = True) -> Generator[Dict[str, Any], None, None]:
        """Send message to Letta agent and stream responses
        
        Args:
            message: User message to send
            stream_tokens: If True, use token streaming for real-time UX
            
        Yields:
            Dict containing message chunks with type, content, and metadata
        """
        if not self.is_connected:
            raise ConnectionError("Letta client not connected. Call connect() first.")
        
        try:
            # Create streaming request
            stream = self.client.agents.messages.create_stream(
                agent_id=self.agent_id,
                messages=[{"role": "user", "content": message}],
                stream_tokens=stream_tokens
            )
            
            # Message accumulators for token streaming
            message_accumulators = {}
            
            # Process stream
            for chunk in stream:
                processed_chunk = self._process_stream_chunk(chunk, message_accumulators)
                if processed_chunk:
                    yield processed_chunk
                    
        except Exception as e:
            logger.error(f"Error during streaming: {e}")
            yield {
                "type": "error",
                "content": f"Error: {str(e)}",
                "error": True
            }
    
    def _process_stream_chunk(self, chunk: Any, accumulators: Dict) -> Optional[Dict[str, Any]]:
        """Process individual stream chunk
        
        Args:
            chunk: Raw chunk from Letta stream
            accumulators: Dict to accumulate partial messages
            
        Returns:
            Processed chunk dict or None
        """
        try:
            # Check if chunk has message_type attribute
            if not hasattr(chunk, 'message_type'):
                return None
            
            msg_type = chunk.message_type
            
            # Handle different message types
            if msg_type == 'reasoning_message':
                return self._handle_reasoning_message(chunk, accumulators)
            
            elif msg_type == 'assistant_message':
                return self._handle_assistant_message(chunk, accumulators)
            
            elif msg_type == 'tool_call_message':
                tool_call = getattr(chunk, 'tool_call', None)
                tool_name = 'unknown'
                if tool_call:
                    if hasattr(tool_call, 'name'):
                        tool_name = tool_call.name
                    elif isinstance(tool_call, dict):
                        tool_name = tool_call.get('name', 'unknown')
                return {
                    "type": "tool_call",
                    "content": f"Calling tool: {tool_name}",
                    "tool_name": tool_name
                }
            
            elif msg_type == 'tool_return_message':
                return {
                    "type": "tool_return",
                    "content": "Tool execution completed",
                    "tool_return": getattr(chunk, 'tool_return', '')
                }
            
            elif msg_type == 'stop_reason':
                return {
                    "type": "stop",
                    "content": "",
                    "stop_reason": getattr(chunk, 'stop_reason', 'end_turn')
                }
            
            elif msg_type == 'usage_statistics':
                return {
                    "type": "usage",
                    "content": "",
                    "usage": {
                        "completion_tokens": getattr(chunk, 'completion_tokens', 0),
                        "prompt_tokens": getattr(chunk, 'prompt_tokens', 0),
                        "total_tokens": getattr(chunk, 'total_tokens', 0),
                        "step_count": getattr(chunk, 'step_count', 0)
                    }
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error processing chunk: {e}")
            return None
    
    def _handle_reasoning_message(self, chunk: Any, accumulators: Dict) -> Optional[Dict[str, Any]]:
        """Handle reasoning message chunks"""
        try:
            msg_id = getattr(chunk, 'id', 'unknown')
            reasoning_content = getattr(chunk, 'reasoning', '')
            
            # Initialize accumulator if new message
            if msg_id not in accumulators:
                accumulators[msg_id] = {
                    'type': 'reasoning',
                    'content': ''
                }
            
            # Accumulate content
            accumulators[msg_id]['content'] += reasoning_content
            
            return {
                "type": "reasoning",
                "content": accumulators[msg_id]['content'],
                "partial": True,
                "message_id": msg_id
            }
            
        except Exception as e:
            logger.error(f"Error handling reasoning message: {e}")
            return None
    
    def _handle_assistant_message(self, chunk: Any, accumulators: Dict) -> Optional[Dict[str, Any]]:
        """Handle assistant message chunks"""
        try:
            msg_id = getattr(chunk, 'id', 'unknown')
            content = getattr(chunk, 'content', '')
            
            # Initialize accumulator if new message
            if msg_id not in accumulators:
                accumulators[msg_id] = {
                    'type': 'assistant',
                    'content': ''
                }
            
            # Accumulate content
            accumulators[msg_id]['content'] += content
            
            return {
                "type": "assistant",
                "content": accumulators[msg_id]['content'],
                "partial": True,
                "message_id": msg_id
            }
            
        except Exception as e:
            logger.error(f"Error handling assistant message: {e}")
            return None
    
    def get_agent_info(self) -> Optional[Dict]:
        """Get information about the connected agent"""
        if not self.is_connected:
            return None
        
        try:
            agent = self.client.agents.retrieve(self.agent_id)
            return {
                "id": agent.id,
                "name": getattr(agent, 'name', 'Unknown'),
                "model": getattr(agent, 'llm_config', {}).model if hasattr(agent, 'llm_config') else 'Unknown',
                "created_at": getattr(agent, 'created_at', 'Unknown')
            }
        except Exception as e:
            logger.error(f"Error getting agent info: {e}")
            return None

# Global instance
letta_service = LettaService()

"""
Chainlit UI for the Physical AI RAG Chatbot.
Implements a chat interface with session handling.
"""
import chainlit as cl
from typing import Dict, Any, List
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our API components
from .api import get_book_answer
from .services.chat_service import chat_service


@cl.on_chat_start
async def start_chat():
    """
    Initialize the chat session when a user starts chatting.
    """
    # Create a new session ID or use an existing one from user session
    session_id = cl.user_session.get("session_id")
    if not session_id:
        session_id = chat_service.create_session()
        cl.user_session.set("session_id", session_id)

    # Send a welcome message
    welcome_msg = (
        "Hello! I'm your Physical AI textbook assistant. "
        "Ask me anything about the Physical AI textbook content, "
        "and I'll provide answers based on the book with proper citations."
    )
    await cl.Message(content=welcome_msg).send()


@cl.on_message
async def handle_message(message: cl.Message):
    """
    Handle incoming messages from the user.

    Args:
        message: Chainlit message object containing user input
    """
    # Get the user's query
    user_query = message.content

    # Get the session ID
    session_id = cl.user_session.get("session_id")
    if not session_id:
        session_id = chat_service.create_session()
        cl.user_session.set("session_id", session_id)

    try:
        # Get conversation history for context
        history = chat_service.get_formatted_history_for_llm(session_id)

        # Get the answer from our BookRAG agent
        result = get_book_answer(user_query, history)

        # Extract response and citations
        response = result.get("response", "I couldn't generate a response.")
        citations = result.get("citations", [])
        retrieved_chunks = result.get("retrieved_chunks", 0)
        is_not_covered = result.get("is_not_covered", False)

        # Format the response with citations if available
        if citations:
            # Add citations to the response
            citation_text = "\n\nCitations:\n"
            for i, citation in enumerate(citations[:3]):  # Show first 3 citations to avoid clutter
                file_path = citation.get("file", "unknown")
                lines = citation.get("lines", [0, 0])
                citation_text += f"- {file_path}:{lines[0]}-{lines[1]}\n"

            response += citation_text

        # Send the response to the user
        msg = cl.Message(content=response)
        await msg.send()

        # Add messages to the session (now that we have both user and assistant messages)
        chat_service.add_message_to_session(session_id, "user", user_query)
        chat_service.add_message_to_session(
            session_id, "assistant", response, citations=citations
        )

        # If this is a "not covered" response, let the user know
        if is_not_covered:
            await cl.Message(
                content="I couldn't find information about this topic in the Physical AI textbook. "
                        "Please try asking about another topic covered in the book."
            ).send()

    except Exception as e:
        # Handle any errors gracefully
        error_msg = f"Sorry, I encountered an error processing your request: {str(e)}"
        await cl.Message(content=error_msg).send()


@cl.password_auth_callback
def auth_callback(username: str, password: str) -> Dict[str, Any]:
    """
    Optional: Implement authentication callback if needed.
    For now, we'll allow all users without authentication.
    """
    # In a production environment, you would validate the username and password
    # For this implementation, we'll just return a user profile
    return {"id": username, "metadata": {"role": "user", "provider": "credentials"}}


@cl.on_settings_update
async def setup_agent(settings: Dict[str, Any]):
    """
    Handle settings updates from the UI.
    """
    print("Settings updated:", settings)


# Additional UI elements and configuration
def setup_ui():
    """
    Setup additional UI configuration.
    """
    # Set up the UI theme and other configuration
    pass


if __name__ == "__main__":
    # This would be run with: chainlit run rag/ui.py -w
    # The UI is configured through Chainlit's built-in server
    print("Chainlit UI ready. Run with: chainlit run rag/ui.py -w")
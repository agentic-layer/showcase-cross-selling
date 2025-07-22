import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, Optional, Protocol

from google.adk.agents import Agent
from google.adk.tools import ToolContext
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


# Todo add invoke method
def send_email(
    tool_context: ToolContext,
    to_email: str,
    subject: str,
    body: str,
    from_email: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Sends an email to the specified recipient.

    Args:
        tool_context: Context to manage session state
        to_email: Recipient email address
        subject: Email subject line
        body: Email body content
        from_email: Sender email address (optional, uses default if not provided)

    Returns:
        Dictionary with status and message about the email sending result.
    """
    # Input validation
    if not to_email or not to_email.strip():
        return {
            "status": "error",
            "message": "Recipient email address is required.",
            "error_code": "MISSING_TO_EMAIL",
        }

    if not subject or not subject.strip():
        return {
            "status": "error",
            "message": "Email subject is required.",
            "error_code": "MISSING_SUBJECT",
        }

    if not body or not body.strip():
        return {
            "status": "error",
            "message": "Email body is required.",
            "error_code": "MISSING_BODY",
        }

    # Use default sender if not provided
    sender_email = from_email or "noreply@company.com"

    try:
        # Create message
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email.strip()
        msg["Subject"] = subject.strip()

        # Add body to email
        msg.attach(MIMEText(body.strip(), "plain"))

        # In production, this would connect to an actual SMTP server
        # For demo purposes, we'll simulate sending
        print(f"[EMAIL SIMULATION] Sending email to {to_email}")
        print(f"[EMAIL SIMULATION] Subject: {subject}")
        print(f"[EMAIL SIMULATION] Body: {body}")

        return {
            "status": "success",
            "message": f"Email sent successfully to {to_email}",
            "recipient": to_email.strip(),
            "subject": subject.strip(),
            "sender": sender_email,
            "email_sent": True,
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send email: {str(e)}",
            "error_code": "EMAIL_SEND_FAILED",
            "recipient": to_email.strip(),
        }


class SlackClientProtocol(Protocol):
    """Protocol for Slack client dependency injection."""

    def chat_postMessage(self, *, channel: str, text: str) -> Dict[str, Any]: ...


class SlackClientWrapper:
    """Wrapper for Slack WebClient to enable dependency injection and testing."""

    def __init__(self, token: Optional[str] = None):
        self.client = WebClient(token=token or os.getenv("SLACK_BOT_TOKEN", ""))

    def chat_postMessage(self, *, channel: str, text: str) -> Dict[str, Any] | bytes:
        """Send a message to a Slack channel or user."""
        try:
            response = self.client.chat_postMessage(channel=channel, text=text)
            return response.data
        except SlackApiError as e:
            return {
                "ok": False,
                "error": e.response["error"],
                "response_metadata": e.response.get("response_metadata", {}),
            }


def send_slack_direct_message(tool_context: ToolContext, slack_user_id: str, message: str) -> Dict[str, Any]:
    """
    Sends a direct message to a specific Slack user by their user ID.

    Args:
        tool_context: Context to manage session state
        slack_user_id: Slack user ID (e.g., "U1234567890")
        message: Message content to send

    Returns:
        Dictionary with status and message about the Slack sending result.
    """
    # Input validation
    if not slack_user_id or not slack_user_id.strip():
        return {
            "status": "error",
            "message": "Slack user ID is required.",
            "error_code": "MISSING_USER_ID",
        }

    if not message or not message.strip():
        return {
            "status": "error",
            "message": "Message content is required.",
            "error_code": "MISSING_MESSAGE",
        }

    # Validate user ID format (Slack user IDs start with 'U' followed by alphanumeric characters)
    user_id = slack_user_id.strip()
    if not user_id.startswith("U") or len(user_id) < 9:
        return {
            "status": "error",
            "message": "Invalid Slack user ID format. User IDs should start with 'U' followed by alphanumeric characters.",
            "error_code": "INVALID_USER_ID_FORMAT",
        }

    # Create default Slack client
    client = SlackClientWrapper()

    try:
        # Send direct message using Slack SDK
        response = client.chat_postMessage(channel=user_id, text=message.strip())

        return {
            "status": "success",
            "message": f"Direct message sent successfully to user {user_id}",
            "user_id": user_id,
            "message_content": message.strip(),
            "slack_sent": True,
            "slack_response": response,
        }

    except SlackApiError as e:
        return {
            "status": "error",
            "message": f"Slack API error: {e.response['error']}",
            "error_code": "SLACK_API_ERROR",
            "user_id": user_id,
            "slack_error": e.response.get("error"),
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send Slack direct message: {str(e)}",
            "error_code": "SLACK_SEND_FAILED",
            "user_id": user_id,
        }


root_agent = Agent(
    name="communications_agent",
    model="gemini-2.0-flash-exp",
    description="Communications Agent - Handles email and Slack direct messaging for automated communications",
    instruction="""\
        You are a professional communications src that helps with sending emails and Slack direct messages.
        You can draft texts, send emails to any email address and send direct messages to individual Slack users by 
        their user ID.
        
        # Available Functions
        1. **Draft Texts**: Use the text_draft tool to draft messages in various formats (plain text, markdown, HTML).
        2. **Email Sending**: Use send_email to send emails with subject and body content
        3. **Slack Direct Messaging**: Use send_slack_direct_message to send direct messages to specific Slack users by their user ID
        
        # Email Guidelines
        - Always include a clear subject line
        - Write professional, clear email content
        - Validate email addresses before sending
        - Ask for clarification if sender email is important
        
        # Slack Guidelines  
        - Only direct messages to individual users are supported
        - User IDs must be provided (e.g., "U1234567890") - these start with 'U' followed by alphanumeric characters
        - Keep messages concise and clear
        - Use appropriate formatting for readability
        - Requires SLACK_BOT_TOKEN environment variable to be set
        
        # Communication Style
        - Be professional and helpful
        - Confirm all details before sending
        - Provide clear status updates on message delivery
        - Ask for clarification when information is missing
        
        # Security Notes
        - These are simulation functions for demonstration
        - In production, proper authentication and configuration would be required
        - Always respect privacy and communication policies
        
        # Example Usage
        - "Send an email to john@example.com about the meeting tomorrow"
        - "Send a direct message to user U1234567890 about the project update"
        """,
    tools=[
        send_email,
        send_slack_direct_message,
    ],
)

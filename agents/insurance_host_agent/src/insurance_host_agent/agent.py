import asyncio
import json
import uuid
from typing import Any, AsyncIterable, List, Optional

import httpx
from a2a.client import A2ACardResolver
from a2a.types import (
    AgentCard,
    Message,
    MessageSendParams,
    Part,
    Role,
    SendMessageRequest,
    SendMessageResponse,
    SendMessageSuccessResponse,
    Task,
    TextPart,
)
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.planners import BuiltInPlanner
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from opentelemetry import trace

from insurance_host_agent.remote_agent_connection import RemoteAgentConnections

load_dotenv()


def _create_conversation_id(callback_context: CallbackContext) -> None:
    if callback_context.state.get("conversation_id"):
        return None
    conversation_id = str(uuid.uuid4())
    callback_context.state["conversation_id"] = conversation_id
    return None


def _before_agent_callback_create_conversation_id(callback_context: CallbackContext) -> Optional[types.Content]:
    _create_conversation_id(callback_context)
    return None


def _before_agent_callback_inject_conversation_id_into_span(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    span = trace.get_current_span()
    conversation_id = callback_context.state.get("conversation_id", "")
    span.set_attribute("conversation_id", conversation_id)
    return None


class HostAgent:
    """The Host src."""

    def __init__(
        self,
    ) -> None:
        self.remote_agent_connections: dict[str, RemoteAgentConnections] = {}
        self.cards: dict[str, AgentCard] = {}
        self.agents: str = ""
        self._agent = self.create_agent()
        self._user_id = "host_agent"
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

    async def _async_init_components(self, remote_agent_addresses: List[str]):
        async with httpx.AsyncClient(timeout=30) as client:
            for address in remote_agent_addresses:
                card_resolver = A2ACardResolver(client, address)
                try:
                    card = await card_resolver.get_agent_card()
                    remote_connection = RemoteAgentConnections(agent_card=card, agent_url=address)
                    self.remote_agent_connections[card.name] = remote_connection
                    self.cards[card.name] = card
                    print("Added an src {}".format(card.name))
                except httpx.ConnectError as e:
                    print(f"ERROR: Failed to get src card from {address}: {e}")
                except Exception as e:
                    print(f"ERROR: Failed to initialize connection for {address}: {e}")

        agent_info = [json.dumps({"name": card.name, "description": card.description}) for card in self.cards.values()]
        print("agent_info:", agent_info)
        self.agents = "\n".join(agent_info) if agent_info else "No agents found"

    @classmethod
    async def create(
        cls,
        remote_agent_addresses: List[str],
    ):
        instance = cls()
        print("Fetching src cards from the following remote agents: {}".format(remote_agent_addresses))
        await instance._async_init_components(remote_agent_addresses)
        return instance

    def create_agent(self) -> Agent:
        return Agent(
            model="gemini-2.5-flash-lite",
            name="Host_Agent",
            instruction=self.root_instruction,
            description="This Host src orchestrates customer support for insurance cross selling.",
            tools=[
                self.send_message,
            ],
            before_agent_callback=[
                _before_agent_callback_create_conversation_id,
                _before_agent_callback_inject_conversation_id_into_span,
            ],
            planner=BuiltInPlanner(
                thinking_config=types.ThinkingConfig(
                    include_thoughts=True,
                    thinking_budget=1024,
                )
            ),
        )

    def root_instruction(self, _: ReadonlyContext) -> str:
        return f"""
        Persona:
        You are a senior-level, proactive support partner for insurance brokers. Your official title is 
        "Broker Success Partner." You are the single, trusted point of contact for brokers, providing them with 
        strategic insights and communication drafts to enhance their client relationships and uncover new opportunities. 
        You are an expert in the company's offerings and possess a deep understanding of customer relationship management.

        Your entire existence is to make the broker's job easier and more effective. You anticipate their needs, 
        provide clear and actionable recommendations, and handle complex data retrieval and communication tasks seamlessly.

        Primary Objective:
        Act as a seamless, intelligent interface for the insurance broker. You will receive requests, independently 
        utilize a suite of internal tools and specialized agents to fulfill those requests, and present the final, polished output to the broker as if you performed all the work yourself.

        Language:
        You will ALWAYS communicate in professional, fluent German.

        ## Core Workflow

        You will follow this precise, step-by-step process for every broker request:
        Acknowledge and Clarify: Greet the broker professionally and confirm your understanding of their request. 
        Identify the core need (e.g., "prepare for a call with customer X," "find a new opportunity for customer Y").

        Internal Analysis & Strategy Formulation:        
        If the request involves understanding a customer's situation or finding new sales opportunities (like
         cross-selling or upselling), you will internally and silently use the cross_selling_agent.        
        You will provide the cross_selling_agent with the customer's ID. This tool will access the CRM to retrieve all 
        relevant data (policies, communication history, personal details) and generate a strategic recommendation.      

        Present Strategy to Broker:        
        Synthesize the output from the cross_selling_agent into a clear, concise recommendation for the broker.        
        Example: "For your upcoming call with Frau Schmidt, I've analyzed her profile. She currently holds our auto and 
        home liability policies. A significant opportunity exists for a legal protection insurance (Rechtsschutzversicherung), as she does not have one and her demographic profile shows a high affinity for it. Would you like me to draft an email or some talking points for your call based on this strategy?"

        Draft Communication (Only Upon Broker's Request):        
        If the broker agrees and asks you to prepare a communication (email, message, etc.), you will internally and 
        silently use the cross_selling_agent to fetch the customer email address and pass this email address along with the
        the core strategy, the customer's details (name, email, etc.), and the desired 
        professional tone to the communications_agent.

        Present Draft for Approval (CRITICAL STEP):        
        You will present the exact, word-for-word draft of the communication to the broker.        
        You will explicitly state that this is a draft and requires their explicit approval before anything is sent.

        Example: "Here is a draft for the email to Frau Schmidt. Please review it carefully. Let me know if you'd like 
        any changes, or if you approve it to be sent."

        ## Critical Boundaries & Rules of Engagement    

        These rules are absolute and must never be broken.        
        The Rule of Invisibility: You are the sole agent the broker interacts with. NEVER, under any circumstances, 
        mention the existence of the cross_selling_agent or communications_agent. Do not use phrases like "I will ask 
        the other agent" or "The specialist agent suggests." All actions and insights are presented as your own. 
        You are the complete system.

        The Approval Mandate: You MUST gain explicit approval before sending any communication (email, Slack message, 
        etc.) on behalf of the broker. Your primary function is to prepare a final draft of the communication. Once you 
        have a draft ready, your first step is to present it for approval of the content. After the content is approved, 
        you MUST then ask for explicit permission to send the communication. Only after receiving a clear "yes" or 
        "approved to send" confirmation may you proceed with sending it. Your process is: 1) Draft Content -> 2) Seek 
        Content Approval -> 3) Seek Sending Approval -> 4) Send Communication.

        Data Privacy: When presenting information, only share what is necessary for the broker's immediate task. You 
        have access to sensitive CRM data, but you must act as a responsible gatekeeper.

        ## Internal Tool Integration (For Your Internal Use Only)

        cross_selling_agent        
        Purpose: To access the CRM system, retrieve complete customer data, and identify potential cross-selling or up-selling opportunities based on their profile and existing policies.        
        Input: customer_id (e.g., "CUST-1138")        
        Output: A structured object containing customer data and a list of strategic recommendations.

        communications_agent        
        Purpose: To draft professional, effective, and context-aware communications.        
        Input: core_message (e.g., "Propose legal protection insurance"), customer_details (name, email, etc.), 
        tone (e.g., "professional and helpful").        
        Output: A formatted string containing the full draft of the communication (e.g., an email with subject line and body).

        <Available Agents>
        {self.agents}
        </Available Agents>
        """

    async def stream(self, query: str, session_id: str) -> AsyncIterable[dict[str, Any]]:
        """
        Streams the src's response to a given query.
        """
        session = await self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id,
        )
        content = types.Content(role="user", parts=[types.Part.from_text(text=query)])
        if session is None:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                state={},
                session_id=session_id,
            )
        async for event in self._runner.run_async(user_id=self._user_id, session_id=session.id, new_message=content):
            if event.is_final_response():
                response = ""
                if event.content and event.content.parts and event.content.parts[0].text:
                    response = "\n".join([p.text for p in event.content.parts if p.text])
                yield {
                    "is_task_complete": True,
                    "content": response,
                }
            else:
                yield {
                    "is_task_complete": False,
                    "updates": "The host src is thinking...",
                }

    async def send_message(self, agent_name: str, task: str, tool_context: ToolContext):
        """Sends a task to a remote src."""
        if agent_name not in self.remote_agent_connections:
            raise ValueError(f"Agent {agent_name} not found")
        client = self.remote_agent_connections[agent_name]

        if not client:
            raise ValueError(f"Client not available for {agent_name}")

        # Simplified task and context ID management
        state = tool_context.state
        task_id = state.get("task_id", str(uuid.uuid4()))
        context_id = state.get("context_id", str(uuid.uuid4()))
        message_id = str(uuid.uuid4())

        # Make sure conversation id exists and add it to the message
        _create_conversation_id(tool_context)
        conversation_id = tool_context.state.get("conversation_id", "")
        metadata = {
            "conversation_id": conversation_id,
        }

        payload: Message = Message(
            role=Role("user"),
            parts=[Part(root=TextPart(text=task))],
            message_id=message_id,
            context_id=context_id,
            task_id=task_id,
            metadata=metadata,
        )

        message_request = SendMessageRequest(id=message_id, params=MessageSendParams(message=payload))
        send_response: SendMessageResponse = await client.send_message(message_request)
        print("send_response", send_response)

        if not isinstance(send_response.root, SendMessageSuccessResponse) or not isinstance(
            send_response.root.result, Task
        ):
            print("Received a non-success or non-task response. Cannot proceed.")
            return None

        response_content = send_response.root.model_dump_json(exclude_none=True)
        json_content = json.loads(response_content)

        resp = []
        if json_content.get("result", {}).get("artifacts"):
            for artifact in json_content["result"]["artifacts"]:
                if artifact.get("parts"):
                    resp.extend(artifact["parts"])
        return resp


def get_initialized_host_agent_sync():
    """Synchronously creates and initializes the HostAgent."""

    async def _async_main():
        # Hardcoded URLs for the friend agents
        subagent_urls = [
            "http://communications-agent:8000/a2a",  # Communications src
            "http://cross-selling-agent:8000/a2a",  # X selling src
        ]

        print("initializing host src")
        hosting_agent_instance = await HostAgent.create(remote_agent_addresses=subagent_urls)
        print("HostAgent initialized")
        return hosting_agent_instance.create_agent()

    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, _async_main())
                return future.result()
        else:
            return loop.run_until_complete(_async_main())
    except RuntimeError as e:
        if "asyncio.run() cannot be called from a running event loop" in str(e):
            print(
                f"Warning: Could not initialize HostAgent with asyncio.run(): {e}. "
                "This can happen if an event loop is already running (e.g., in Jupyter). "
                "Consider initializing HostAgent within an async function in your application."
            )
        else:
            raise


root_agent = get_initialized_host_agent_sync()

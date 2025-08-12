from time import time

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    Part,
    TaskState,
    TextPart,
)
from a2a.utils import new_agent_text_message, new_task
from google.adk.artifacts import InMemoryArtifactService
from google.adk.events import Event, EventActions
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from base.agent_communication_dashboard_plugin import AgentCommunicationDashboardPlugin


class A2AAgentExecutor(AgentExecutor):
    def __init__(
        self,
        agent,
        status_message="Processing request...",
        artifact_name="response",
    ):
        """Initialize a generic A2A executor.

        Args:
            agent: The ADK agent instance
            status_message: Message to display while processing
            artifact_name: Name for the response artifact
        """
        self.agent = agent
        self.status_message = status_message
        self.artifact_name = artifact_name
        self.runner = Runner(
            app_name=agent.name,
            agent=agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
            plugins=[AgentCommunicationDashboardPlugin()],
        )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Cancel the execution of a specific task."""
        raise NotImplementedError("Cancellation is not implemented for ADKAgentExecutor.")

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query = context.get_user_input()
        if context.current_task is not None:
            task = context.current_task
        elif context.message is not None:
            task = new_task(context.message)
        else:
            raise TypeError

        await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)
        if context.call_context:
            user_id = context.call_context.user.user_name
        else:
            user_id = "a2a_user"

        try:
            # Update status with custom message
            await updater.update_status(
                TaskState.working,
                new_agent_text_message(self.status_message, task.context_id, task.id),
            )

            # Process with ADK src
            session = await self.runner.session_service.create_session(
                app_name=self.agent.name,
                user_id=user_id,
                state={},
                session_id=task.context_id,
            )

            # Set conversation_id in session state
            message = context.message
            metadata = getattr(message, "metadata", {})
            conversation_id = metadata.get("conversation_id")
            current_time = time()
            state_changes = {
                "conversation_id": conversation_id,
            }
            actions_with_update = EventActions(state_delta=state_changes)
            system_event = Event(
                invocation_id="update_state",
                author=self.agent.name,
                actions=actions_with_update,
                timestamp=current_time,
            )
            await self.runner.session_service.append_event(session, system_event)

            content = types.Content(role="user", parts=[types.Part.from_text(text=query)])

            response_text = ""
            async for event in self.runner.run_async(user_id=user_id, session_id=session.id, new_message=content):
                if event.is_final_response() and event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            response_text += part.text + "\n"
                        elif hasattr(part, "function_call"):
                            # Log or handle function calls if needed
                            pass  # Function calls are handled internally by ADK

            # Add response as artifact with custom name
            await updater.add_artifact(
                [Part(root=TextPart(text=response_text))],
                name=self.artifact_name,
            )

            await updater.complete()

        except Exception as e:
            await updater.update_status(
                TaskState.failed,
                new_agent_text_message(f"Error: {e!s}", task.context_id, task.id),
                final=True,
            )

import copy
from typing import Any

from aidial_sdk.chat_completion import Message, Role

from task.utils.constants import TOOL_CALL_HISTORY_KEY


def unpack_messages(messages: list[Message], state_history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for message in messages:
        if message.role == Role.ASSISTANT:
            if custom_content := message.custom_content:
                state = custom_content.state
                if state and isinstance(state, dict):
                    tool_call_history = state.get(TOOL_CALL_HISTORY_KEY)
                    if tool_call_history and isinstance(tool_call_history, list):
                        for history_msg in tool_call_history:
                            if history_msg.get("role") == Role.TOOL.value:
                                result.append(
                                    {
                                        "role": Role.TOOL.value,
                                        "content": history_msg.get("content"),
                                        "custom_content": history_msg.get("custom_content"),
                                        "tool_call_id": history_msg.get("tool_call_id"),
                                    }
                                )
                            else:
                                result.append(history_msg)

                    msg = copy.deepcopy(message)
                    msg.custom_content = None
                    result.append(msg.dict())
        else:
            msg = copy.deepcopy(message)
            if msg.custom_content and not msg.custom_content.attachments:
                msg.custom_content = None
            result.append(msg.dict())

    if state_history:
        result.extend(state_history)

    return result

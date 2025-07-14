import asyncio
import json
from typing import Any

from aidial_client.types.chat.legacy.chat_completion import CustomContent, ToolCall
from aidial_sdk.chat_completion import Message, Role, Choice, Request, Response
from openai import AsyncAzureOpenAI

from task.tools.base import BaseTool
from task.utils.constants import TOOL_CALL_HISTORY_KEY
from task.utils.history import unpack_messages
from task.utils.response import capture_attachments
from task.utils.stage import StageProcessor


class LLMAgent:

    def __init__(
            self,
            endpoint: str,
            api_key: str,
            api_version: str,
            system_prompt: str,
            request: Request,
            tools: list[BaseTool],
    ):
        self.endpoint = endpoint
        self.api_key = api_key
        self.api_version = api_version
        self.system_prompt = system_prompt
        self.request = request
        self.tools = tools
        self._tools_dict: dict[str, BaseTool] = {
            tool.name: tool
            for tool in tools
        }
        self.state = {
            TOOL_CALL_HISTORY_KEY: []
        }

    async def handle_request(
            self, choice: Choice, deployment_name: str, response: Response, **kwargs
    ) -> Message:
        client: AsyncAzureOpenAI = AsyncAzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.api_key,
            api_version=self.api_version,
        )

        chunks = await client.chat.completions.create(
            **{
                "messages": self._prepare_messages(self.request.messages),
                "tools": [tool.schema for tool in self.tools],
                "stream": True,
                "model": deployment_name,
            }
        )

        tool_call_index_map = {}
        content = ''
        custom_content: CustomContent = CustomContent(attachments=[])
        async for chunk in chunks:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    choice.append_content(delta.content)
                    content += delta.content

                if custom_content := getattr(chunk.choices[0].delta, "custom_content", None):
                    custom_content.attachments.extend(capture_attachments(chunk))

                if delta.tool_calls:
                    for tool_call_delta in delta.tool_calls:
                        if tool_call_delta.id:
                            tool_call_index_map[tool_call_delta.index] = tool_call_delta
                        else:
                            tool_call = tool_call_index_map[tool_call_delta.index]
                            if tool_call_delta.function:
                                argument_chunk = tool_call_delta.function.arguments or ''
                                tool_call.function.arguments += argument_chunk

        assistant_message = Message(
            role=Role.ASSISTANT,
            content=content,
            custom_content=custom_content,
            tool_calls=[ToolCall.validate(tool_call) for tool_call in tool_call_index_map.values()]
        )

        if assistant_message.tool_calls:
            tasks = [
                self._process_tool_call(
                    tool_call=tool_call,
                    choice=choice,
                    response=response,
                )
                for tool_call in assistant_message.tool_calls
            ]
            tool_messages = await asyncio.gather(*tasks)

            self.state[TOOL_CALL_HISTORY_KEY].append(assistant_message.dict())
            self.state[TOOL_CALL_HISTORY_KEY].extend(tool_messages)

            return await self.handle_request(choice, deployment_name, response, **kwargs)

        choice.set_state(self.state)

        return assistant_message

    def _prepare_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        unpacked_messages = unpack_messages(messages, self.state[TOOL_CALL_HISTORY_KEY])
        unpacked_messages.insert(
            0,
            {
                "role": Role.SYSTEM.value,
                "content": self.system_prompt,
            }
        )

        print("\nHistory:")
        for msg in unpacked_messages:
            print(f"     {json.dumps(msg)}")

        print(f"{'-' * 100}\n")

        return unpacked_messages

    async def _process_tool_call(self, tool_call: ToolCall, choice: Choice, response: Response) -> dict[str, Any]:
        """Process a tool call and update the message history."""

        tool_name = tool_call.function.name

        stage = StageProcessor.open_stage(
            choice,
            tool_name
        )
        await response.aflush()

        tool = self._tools_dict[tool_name]
        stage.append_content(
            f"```json\n\r{json.dumps(json.loads(tool_call.function.arguments), indent=2)}\n\r```\n\r")
        tool_message = await tool.execute(tool_call, stage, response)

        StageProcessor.close_stage_safely(stage)

        return tool_message.dict()

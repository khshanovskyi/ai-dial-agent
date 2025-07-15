import asyncio
import json
from typing import Any

from aidial_client import AsyncDial
from aidial_client.types.chat.legacy.chat_completion import CustomContent, ToolCall
from aidial_sdk.chat_completion import Message, Role, Choice, Request, Response

from task.tools.base import BaseTool
from task.utils.constants import TOOL_CALL_HISTORY_KEY
from task.utils.history import unpack_messages
from task.utils.stage import StageProcessor


class LLMAgent:

    def __init__(
            self,
            endpoint: str,
            api_version: str,
            system_prompt: str,
            request: Request,
            tools: list[BaseTool],
    ):
        self.endpoint = endpoint
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
        # We persist tool calls in `state` in the `tool_call_history` list

    async def handle_request(
            self, choice: Choice, deployment_name: str, response: Response, api_key: str, **kwargs
    ) -> Message:
        #TODO:
        # Create client with:
        #   - base_url=self.endpoint
        #   - api_key=api_key
        #   - api_version=self.api_version
        client: AsyncDial = None

        chunks = await client.chat.completions.create(
            #TODO:
            # Configure chat completion request (it will return `AsyncStream[ChatCompletionChunk]`):
            #   - messages=self._prepare_messages(self.request.messages)
            #   - tools=[tool.schema for tool in self.tools]
            #   - deployment_name=deployment_name
            #   - stream=True
        )

        tool_call_index_map = {}
        content = ''
        custom_content: CustomContent = CustomContent(attachments=[])
        async for chunk in chunks:
            if chunk.choices and len(chunk.choices) > 0:
                #TODO:
                # Now let's handle stream with ChatCompletionChunk:
                # 1. Get `delta` from chunk (`chunk.choices[0].delta`) and assign to `delta` variable
                # 2. If `delta` is present and has `content`:
                #   - append `delta.content` to `choice`
                #   - collect `delta.content` to `content` (we need to form an assistant message later and we need full content for it)
                # 3. Collect tool calls:
                #   - if `delta` has `tool_calls`:
                #       - iterate through tool_calls and:
                #           - if tool call delta has `id` then put it to the `tool_call_index_map` (key is `index`, value is tool call delta)
                #           - Otherwise: get the `tool_call` from `tool_call_index_map` by index and if the tool call delta
                #             has `function` then get its `arguments` (tool_call_delta.function.arguments) and concat them
                #             with `tool_call.function.arguments`
                pass


        assistant_message = Message(
            #TODO:
            # Configure assistant_message:
            #   - role=Role.ASSISTANT
            #   - content=content
            #   - custom_content=custom_content
            #   - tool_calls=[ToolCall.validate(tool_call) for tool_call in tool_call_index_map.values()]
        )

        if assistant_message.tool_calls:
            #TODO:
            # Now let's handle tool calls:
            # 1. Prepare tool call processing tasks:
            #   - create list with tasks. You need to iterate through `assistant_message.tool_calls` and call the
            #     `self._process_tool_call` with:
            #       - tool_call=tool_call (tool call from `assistant_message.tool_calls`)
            #       - choice=choice
            #       - api_key=api_key
            # 2. Run tasks: `await asyncio.gather(*tasks)` and assign result to `tool_messages` variable
            # 3. Append to state tool history assistant_message as dict: `self.state[TOOL_CALL_HISTORY_KEY].append(assistant_message.dict())`
            # 4. Add to state tool history tool_messages: self.state[TOOL_CALL_HISTORY_KEY].extend(tool_messages)
            # 5. Now we need make a recursive call to proceed processing of user request

            return None

        #TODO:
        # Set state for choice with `self.state`. With this step we pack tool message history into state of the
        # assistant message the will shown to user.

        return assistant_message

    def _prepare_messages(self, messages: list[Message]) -> list[dict[str, Any]]:
        #TODO:
        # 1. Call method `unpack_messages` from `utils` with `messages` and `self.state[TOOL_CALL_HISTORY_KEY]` and
        #    assign it to the `unpacked_messages` variable. With this step we 'unpack' whole history for LLM that LLM
        #    will have the whole context of what tools were called and with what arguments, and how tools responded on that
        # 2. Add system prompt to the `unpacked_messages`:
        #   - insert into `unpacked_messages` by index 0 dict with such parameters:
        #       - "role": Role.SYSTEM.value,
        #       - "content": self.system_prompt


        # Code bellow prints `unpacked_messages` to console and returns it as list of dicts
        print("\nHistory:")
        for msg in unpacked_messages:
            print(f"     {json.dumps(msg)}")

        print(f"{'-' * 100}\n")

        return unpacked_messages

    async def _process_tool_call(self, tool_call: ToolCall, choice: Choice, api_key: str) -> dict[str, Any]:
        #TODO:
        # 1. Get `tool_call.function.name` and assign it to the `tool_name` variable
        # 2. Create new stage that will represent tool call in chat (request arguments and tool response):
        #   - CallStageProcessor.open_stage(choice, tool_name) and assign to the `stage` variable
        # 3. Append request arguments to the stage:
        #   - stage.append_content("## Request arguments: \n")
        #   - stage.append_content(f"```json\n\r{json.dumps(json.loads(tool_call.function.arguments), indent=2)}\n\r```\n\r")
        #   - stage.append_content("## Response: \n")
        # 4. Get tool from `self._tools_dict` and assign to the `tool` variable
        # 5. Execute tool and resul assign to `tool_message` variable
        # 6. Close `stage` safely with StageProcessor
        # 7. return `tool_message.dict()`

        return None

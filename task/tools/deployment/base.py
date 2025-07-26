import json
from abc import ABC, abstractmethod
from typing import Any

from aidial_client import AsyncDial
from pydantic import StrictStr

from task.tools.base import BaseTool

from aidial_sdk.chat_completion import Stage, Message, Role, ToolCall, CustomContent, Choice


class DeploymentTool(BaseTool, ABC):

    #TODO:
    # Create such methods:
    # 1. Create constructor with:
    #       - endpoint: str
    #       - api_version: str
    # 2. Create `deployment_name` method (each child of DeploymentTool will have preconfigured deployment name, such
    #    as dalle-e-3, google-web-search, etc.):
    #   - mark as `@property`
    #   - mark as `@abstractmethod`
    #   - returns str
    #   - Instead of implementation add `pass`
    # 3. Create `tool_parameters` method (this method will provide additional preconfigured parameters):
    #   - mark as `@property`
    #   - returns dict[str, Any]
    #   - return empty dict (by default)


    async def execute(self, tool_call: ToolCall, stage: Stage, choice: Choice, api_key: str) -> Message:
        #TODO:
        # Create client with:
        #   - base_url=self.endpoint
        #   - api_key=api_key
        #   - api_version=self.api_version
        client: AsyncDial = None

        #TODO:
        # 1. Get arguments as dict (use `json.loads()`) and assign to `arguments` variable
        # 2. Get `prompt` value from `arguments` and assign to `prompt` variable. `prompt` is the text request from LLM
        #    that we will later pass as message content.
        # 3. Delete `prompt` from `arguments` (del arguments["prompt"]). We need it since LLM can provide additional
        #    arguments that we will propagate to deployment via `custom_fields` and `prompt` is not need there.

        chunks = await client.chat.completions.create(
            #TODO:
            # Configure call to chat completion:
            #   - messages=[{"role": "user", "content": prompt}]
            #   - deployment_name=self.deployment_name
            #   - stream=True (we will stream response from deployment to stage)
            #   - extra_body={"custom_fields":{"configuration": {**arguments}}} (For some models we can provide additional configuration)
            #   - **self.tool_parameters
        )

        content = ''
        custom_content: CustomContent = CustomContent(attachments=[])
        async for chunk in chunks:
            if chunk.choices and len(chunk.choices) > 0:
                #TODO:
                # Now let's handle stream with ChatCompletionChunk:
                # 1. Get `delta` from chunk (`chunk.choices[0].delta`) and assign to `delta` variable
                # 2. If `delta` is present and has `content`:
                #   - append `delta.content` to `stage`
                #   - collect `delta.content` to `content` (we need to form an tool message later)
                # 3. Collect attachments:
                #   - if `delta` is present and has `custom_content` with ``attachments:
                #       - get attachments and assign them to the `attachments` variable
                #       - extend `custom_content.attachments` with retrieved `attachments`
                #       - iterate through `attachments` and add them to stage (add_attachment method):
                #       - `stage.add_attachment(type=attachment.type, title=attachment.title, data=attachment.data, url=attachment.url,
                #                              reference_url=attachment.reference_url,reference_type=attachment.reference_type)`
                raise

        return Message(
            #TODO:
            # Configure tool message:
            #   - role=Role.TOOL
            #   - content=StrictStr(content)
            #   - custom_content=custom_content
            #   - tool_call_id=StrictStr(tool_call.id)
        )

from typing import Any

from aidial_sdk.chat_completion import ToolCall, Stage, Message, Choice

from task.tools.deployment.base import DeploymentTool


class ImageGenerationTool(DeploymentTool):

    async def execute(self, tool_call: ToolCall, stage: Stage, choice: Choice, api_key: str) -> Message:
        msg =  await super().execute(tool_call, stage, choice, api_key)

        if msg.custom_content and msg.custom_content.attachments:
            for attachment in msg.custom_content.attachments:
                if attachment.type in ("image/png", "image/jpeg"):
                    # Here is interesting point, we print the picture in choice directly (in stage it will be added as attachment)
                    choice.append_content(f"\n\r![image]({attachment.url})\n\r")
                    if not msg.content:
                        msg.content = 'The image has been successfully generated according to request and shown to user!'

        return msg

    @property
    def deployment_name(self) -> str:
        return "dall-e-3"

    @property
    def name(self) -> str:
        return "image_generation_tool"

    @property
    def description(self) -> str:
        return "# Image generator\nGenerates image based on the provided description.\n## Instructions:\n- Use that tool when user asks to generate an image based on the description or to visualize some text or information.\n- Choose the best size from available options based on user request or image type. For specific size requests, use the closest supported option.\n- When the tool returns a markdown image URL, always include it in your response and follow it with a brief description.\n## Restrictions:\n- Never use this tool for data or numerical information visualization."

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Extensive description of the image that should be generated."
                },
                "size": {
                    "type": "string",
                    "description": "The size of the generated image.",
                    "enum": [
                        "1024x1024",
                        "1024x1792",
                        "1792x1024"
                    ],
                    "default": "1024x1024"
                },
                "style": {
                    "type": "string",
                    "description": "The style of the generated image. Must be one of `vivid` or `natural`. \n- `vivid` causes the model to lean towards generating hyperrealistic and dramatic images. \n- `natural` causes the model to produce more natural, less realistic looking images.",
                    "enum": [
                        "natural",
                        "vivid"
                    ],
                    "default": "natural"
                },
                "quality": {
                    "type": "string",
                    "description": "The quality of the image that will be generated. ‘hd’ creates images with finer details and greater consistency across the image.",
                    "enum": [
                        "standard",
                        "hd"
                    ],
                    "default": "standard"
                }
            },
            "required": [
                "prompt",
                "size",
                "style",
                "quality"
            ]
        }
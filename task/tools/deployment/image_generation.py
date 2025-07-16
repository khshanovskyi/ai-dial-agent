from typing import Any

from aidial_sdk.chat_completion import ToolCall, Stage, Message, Choice
from pydantic import StrictStr

from task.tools.deployment.base import DeploymentTool


class ImageGenerationTool(DeploymentTool):

    #TODO:
    # Override async `execute` method (here we will additionally propagate the picture to Choice):
    #   1. Get result of execution from parent class `super().execute` and assign it to `msg` variable
    #   2. If `msg` has `custom_content` and `attachments`:
    #       - Iterate through attachments and if `attachment.type` in ("image/png", "image/jpeg"):
    #           - append such content to `choice`: `f"\n\r![image]({attachment.url})\n\r"`
    #             DIAL Core will load image by this url from bucket directly to the choice in chat and user will be able to see it
    #   3. If `msg` doesn't have `content`:
    #       - Add to `msg.content` info that image has been generated and shown to user
    #   4. return msg
    # ---
    # All other required methods are implemented, you can check them.
    # Pay attention at the `properties` (size, style, quality) - it is additional configuration for `dall-e-3` model
    # and they will be passed as `extra_body -> custom_fields -> configuration` additional arguments (they are custom)

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
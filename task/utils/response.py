from aidial_sdk.chat_completion import Attachment
from openai.types.chat import ChatCompletionChunk


def capture_attachments(chunk: ChatCompletionChunk) -> list[Attachment]:
    custom_content = getattr(chunk.choices[0].delta, "custom_content", {})
    if custom_content and isinstance(custom_content, dict):
        attachments = custom_content.get("attachments")
        if attachments:
            return [
                Attachment(
                    type=attachment.get("type"),
                    title=attachment.get("title"),
                    data=attachment.get("data"),
                    url=attachment.get("url"),
                    reference_url=attachment.get("reference_url"),
                    reference_type=attachment.get("reference_type"),
                )
                for attachment in attachments
            ]
    return []

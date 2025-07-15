from typing import Any

from aidial_sdk.chat_completion import Attachment


def capture_attachments(custom_content_dict: dict[str, Any]) -> list[Attachment]:
    print(custom_content_dict)
    attachments = custom_content_dict.get("attachments")
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

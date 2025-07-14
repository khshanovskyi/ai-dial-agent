from typing import Optional

from aidial_sdk.chat_completion import Choice, Stage


class StageProcessor:

    @staticmethod
    def open_stage(choice: Choice, name: Optional[str] = None) -> Stage:
        stage = choice.create_stage(name)
        stage.open()
        stage.append_content("")
        print("Stage opened!!!")
        print(stage._opened)
        return stage

    @staticmethod
    def close_stage_safely(stage: Stage) -> None:
        try:
            stage.close()
        except Exception as e:
            print("⚠️ Unable to close stage. ", e)

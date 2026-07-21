#memory/conversation_memory.py
import json
from pathlib import Path
import config

class ConversationMemory:

    def __init__(self, session_id=1):

        self.session_id = session_id
        self.file_path = Path(config.CONVERSATION_MEMORY_FILE)

        if not self.file_path.exists():

            self.file_path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            self.save([])


    def load(self):
        """
        Load complete conversation history from the json file.
        """

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    def save(self, conversation):
        """
        Save conversation history into the json file.
        """

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                conversation,
                f,
                indent=4,
                ensure_ascii=False
            )


    def add(self, role, content):
        """
        Add a new conversation message to the current session
        and persist it in the json file.
        """

        conversation = self.load()

        conversation.append(
            {
                "session_id" : self.session_id,  #session_id because user can be more than one at a time
                "role": role,
                "content": content
            }
        )

        self.save(conversation)


    def get(self, limit=5):
        """
        Retrieve conversation history for the current session
        from the JSON file.

        Returns the most recent 'limit' messages.
        If limit is None, returns the entire session history.
        """

        conversation = self.load()

        conversation = [

            message

            for message in conversation
            if message["session_id"] == self.session_id
        ]

        if limit is None:
            return conversation

        return conversation[-limit:]


    # def clear(self):
    #     """
    #     Remove all messages belonging to the current session
    #     from the JSON file.
    #     """

    #     conversation = self.load()

    #     conversation = [

    #         message

    #         for message in conversation
    #         if message["session_id"] == self.session_id
    #     ]

    #     self.save(conversation)
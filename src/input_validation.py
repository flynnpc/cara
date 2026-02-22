import os
from typing import TypeAlias

Validation: TypeAlias = callable[str, bool]


class InputValidation:
    def __init__(self):
        self.accepted_bool_responses: list[str] = ["y", "yes", "no", "n"]
        self.messages: dict[str, str] = {
            "check_boolean_input": "That is not a recognized input. Please enter yes (Y) or no (N).",
            "check_valid_path": "That is not a valid path. Please try again.",
        }

    def repeat_input(self, validation_func: Validation) -> bool:
        new_answer = input(self.messages[validation_func.__name__])
        if validation_func(new_answer):
            return True
        else:
            return self.repeat_input(validation_func)

    def check_boolean_input(self, answer: str, overide_messeage: False) -> bool:
        is_accepted_response = answer.lower() in self.accepted_bool_responses
        if is_accepted_response:
            return True
        else:
            return self.repeat_input(self.check_boolean_input)

    def check_valid_path(self, path: str, overide_messeage: False) -> bool:
        is_accepted_response = os.path.isfile(path)
        if is_accepted_response:
            return True
        else:
            return self.repeat_input(self.check_boolean_input)

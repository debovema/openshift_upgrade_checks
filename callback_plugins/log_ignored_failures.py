from ansible.plugins.callback import CallbackBase
import os
import json

LOG_FILE = "./errors.json"

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'log_ignored_failures'

    def __init__(self):
        super(CallbackModule, self).__init__()
        # Ensure log file is clean on start and start a JSON array
        with open(LOG_FILE, 'w') as f:
            f.write("[\n")

    def v2_playbook_on_stats(self, stats):
        # remove the last comma and close the JSON array
        with open(LOG_FILE, 'r+') as file:
            # Read all lines except the last one
            lines = file.readlines()
            if lines:
                file.seek(0)  # Move to the start of the file
                file.writelines(lines[:-1])  # Write all lines except the last
                file.truncate()  # Truncate the file to remove leftover content
            # Close the JSON array
            file.write(']\n')
        # read the final JSON file
        with open(LOG_FILE, "r") as file:
            data = json.load(file)
        # wite the pretty-printed JSON back to the file
        with open(LOG_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        if ignore_errors:
            task_name = result.task_name or result._task.name
            host = result._host.get_name()
            msg = result._result.get('msg', 'No error message')
            result_data = result._result
            result_data["task_name"] = task_name     
            full_result = json.dumps(result_data, indent=4, ensure_ascii=False)
            with open(LOG_FILE, 'a') as f:
                f.write(f"  {full_result}\n")
                f.write("  ,\n")

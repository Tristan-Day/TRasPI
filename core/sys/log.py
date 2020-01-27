import core
import json
import time
import traceback


def exception_info(error: Exception) -> dict:
    if error.__cause__ is not None:
        cause = exception_info(error.__cause__)
    else:
        cause = {}

    trace = traceback.extract_tb(error.__traceback__)
    stack = []
    for frame in trace:
        stack.append({
            "lineno": frame.lineno,
            "file": frame.filename,
            "name": frame.name,
            "line": frame.line
        })

    return {
        "lineno": stack[-1]["lineno"],
        "type": error.__class__.__name__,
        "message" : str(error),
        "line": stack[-1]["line"],
        "time": time.strftime("%d/%m/%y @ %H:%M:%S")
    }

class Log:

    @classmethod
    def log(cls, error):
        try:
            _error = exception_info(error)
            print(_error)
        except AttributeError:
            print("Attribute Error: Log not created")
        try:
            with open(f"{core.sys.PATH}core/error/eventlog.json", 'r') as eventlog:
                data = json.load(eventlog)
        except (IOError, json.JSONDecodeError):
            data = []
        with open(f"{core.sys.PATH}core/error/eventlog.json", 'w') as eventlog:
            data.append(_error)
            json.dump(data, eventlog)

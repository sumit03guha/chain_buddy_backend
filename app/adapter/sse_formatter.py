import json


def format_server_sent_event(data: str, event: str = None, functions: list = []) -> str:
    """
    Formats the provided data into a JSON string suitable for Server-Sent Events (SSE).

    Args:
    data (str): The main data to be sent as part of the event.
    event (str, optional): Specifies the type of event. Default is None.
    functions (list, optional): A list of function names related to the event. Default is an empty list.

    Returns:
    str: A JSON-formatted string representing the server-sent event, appended with a newline character for SSE compatibility.
    """

    response = {"event": event, "data": data}
    if functions:
        response["functions"] = functions

    return json.dumps(response) + "\n"

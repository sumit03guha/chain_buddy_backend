import traceback

from flask import current_app as app


def handle_error(error):
    """Return a custom response for various errors."""
    tb_list: traceback.StackSummary = traceback.extract_tb(error.__traceback__)
    last_call: traceback.FrameSummary = tb_list[-1]

    app.logger.error(
        f"Exception in {last_call.name} at {last_call.filename}:{last_call.lineno} - {str(error)}"
    )

    response = {"message": error.description, "code": error.code}

    return response, error.code

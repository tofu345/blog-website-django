def newResponse(responseCode, message, data, is_error=False):
    data = {
        "reponseCode": responseCode,
        "message": message
    }
    data["errors" if is_error else "data"] = data
    return data

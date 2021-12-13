def flatten(artifact: object) -> object:
    """
    :rtype: object
    :param artifact: this is the artifact dictionary fetched from the Museum API
    :return: This function returns the flattened JSON from a complex nested JSON recieved from the API response object
    """
    try:
        for constituent in artifact['constituents']:
            for key, value in constituent.items():
                artifact[key] = value
            artifact.pop('constituents')
    except TypeError:
        pass

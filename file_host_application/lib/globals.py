authorizations = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Api-Key'
    }
}

def close_logfilehandlers():
    for handler in reversed(logging.getLogger().handlers):
        handler.close()

def handle_exception(e):
    current_app.logger.error(e.description)
    return make_response({'message':e.description}, e.code)
template = {
    "swagger": "2.0",
    "info": {
        "title": "SCHOLARSHUB API",
        "description": "API for Scholarshub Web Contents",
        "contact": {
            "responsibleOrganization": "ephphathagc",
            "responsibleDeveloper": "ephphathagc",
            "email": "ephphathagc@gmail.com",
            "url": "https://www.linkedin.com/in/inioluwa-jeremiah-adewara-a5984b147",
        },
        "termsOfService": "",
        "version": "1.0"
    },
    "host": "www.scholarshub.academy",  # overrides localhost:500
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "operationId": "getmyData",
    "securityDefinitions": {
        "Bearer": {
            "type": "apikey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
}
swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/"
}

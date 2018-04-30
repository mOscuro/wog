"""
This module lists all settings that are project wide in relation with Django REST Framework.
"""

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    # 'PAGE_SIZE': 50,
    #'DEFAULT_PAGINATION_CLASS': 'wogether.core.pagination.StandardResultsSetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        # We want our parameters to follow camel-case convention
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

from cerberus import Validator

schema = {'user_id': {'type': 'number', 'required': True},
          'workspace_id': {'type': 'number', 'required': True},
          'file_path': {'type': 'string', 'required': True},
          'template_id': {'type': 'string', 'required': True}
          }

post_validator = Validator(schema)
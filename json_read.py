import json
credential_file = 'credentials.json'
credentials = json.load(open(credential_file))
print(credentials['project_id'])
credentials['project_id'] = 'AFTER UPDATE'
print(credentials['project_id'])
import couchdb.mapping as cmap

class User(cmap.Document):
    """  Class used to map a user document inside the '_users' database to a
    Python object.

    For better understanding check https://wiki.apache.org
        /couchdb/Security_Features_Overview

    Args:
        name: Name of the user
        password: password of the user in plain text
        type: (Must be) 'user'
        roles: Roles for the users

    """

    def __init__(self, **values):
        # For user in the _users database id must be org.couchdb.user:<name>
        # Here we're auto-generating it.
        if 'name' in values:
            _id = 'org.couchdb.user:{}'.format(values['name'])
            cmap.Document.__init__(self, id=_id, **values)

    type = cmap.TextField(default='user')
    name = cmap.TextField()
    password = cmap.TextField()
    roles = cmap.ListField(cmap.TextField())

    @cmap.ViewField.define('users')
    def default(doc):
        if doc['name']:
            yield doc['name'], doc
from google.appengine.ext import ndb


class Contact(ndb.Model):
    """contacts"""
    name      = ndb.StringProperty()
    email     = ndb.StringProperty(required=True)
    subscribe = ndb.BooleanProperty()
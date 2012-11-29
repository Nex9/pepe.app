#!/usr/bin/env python

import os, re, random, webapp2, modules, logging

from google.appengine.api import users, memcache, mail, namespace_manager

from imageapp.models import Collection
from models import Contact
from createsend import *

from base import utils, decorators
from base.handlers import BaseHandler, StaticFileHandler
from base.models import CacheFlushCounter

from memberapp.decorators import member_required

# blog imports
from blogapp.models import *
from blogapp.blog import HomeHandler as BlogHomeHandler
from blogapp.blog import TagsHandler as BlogTagsHandler
from blogapp.blog import FeedHandler as BlogFeedHandler
from blogapp.blog import EntryHandler as BlogEntryHandler
from blogapp.blog import AgeVerifyHandler as AgeVerifyHandler
from blogapp.blog import get_entries

from appengine_config import DEBUG

class HomeHandler(BaseHandler):
    @decorators.addslash
    @decorators.cache_page()
    def get(self):
        self.render('home.html')

class PortfolioHandler(BaseHandler):
    """ this handler gets directly all images instead of the subcollections """
    @decorators.normalize_url
    @decorators.removeslash
    @decorators.cache_page(with_keywords=True)
    def get(self, tags=None):
        result = Collection.get_assets(tags)
        if result is None:
            return self.status(404,'Collection Not Found')
        self.render('imageapp/portfolio.html', result = result,
                                      cleanup_list = utils.cleanup_list)

class PortfolioSectionHandler(BaseHandler):
    @decorators.normalize_url
    @decorators.removeslash
    @decorators.cache_page(with_keywords=True)
    def get(self, tags=None):
        result = Collection.get_assets(tags, asset_kind='Collection')
        self.render('imageapp/listing.html', result = result,
                                    cleanup_list = utils.cleanup_list)



class ContactHandler(BaseHandler):
    """displays contact page"""
    @decorators.removeslash
    def get(self):
        self.render("contact.html")

    def post(self):
        name = self.request.get('name','')
        email = self.request.get('email','')
        message = self.request.get('message','')
        subscribe = self.request.get('subscribe', False)

        contact = Contact(name = name,
                          email = email,
                          subscribe = utils.string_to_bool(subscribe))
        contact.put()

        if subscribe:
            try:
                # campaign monitor
                createsend = self.handler.preferences.preferences.get('createsend')
                listid = createsend.get('list_id')
                CreateSend.api_key = createsend.get('api_key')
                subscriber = Subscriber(listid, contact.email)
                subscriber.add(listid, contact.email, contact.name, [], True)
            except Exception, e:
                subj = 'CreateSend Exception'
                msg  = '%s' %e
                logging.warning('%s | %s' %(subj, msg))
                utils.service_notification(subj, msg)

        emailMessage = mail.EmailMessage(sender='ImageApp <nex9llc@gmail.com>',
                                         subject='Contact',
                                         reply_to=email,
                                         to='nex9llc@gmail.com',
                                         bcc='nex9llc@gmail.com')

        emailMessage.body = """ you got a message from: %s, %s\n\n %s """ % (name, email, message)
        emailMessage.send()

        return self.redirect('/thanx')

class ThanxHandler(BaseHandler):
    @decorators.removeslash
    def get(self):
        self.render('thanx.html')


settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "xsrf_cookies": True,
    "debug": DEBUG,
    "ui_modules": modules,
    "cacheflushcounter" : CacheFlushCounter.get_count()
}
routes = [
    (r"/%s/static/(.*)" % namespace_manager.get_namespace(), StaticFileHandler),

    (r"/?", HomeHandler),
    (r"/contact/?", ContactHandler),
    (r"/thanx/?", ThanxHandler)

]

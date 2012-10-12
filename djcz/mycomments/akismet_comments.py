from django.conf import settings
from django.db.models import signals
from django.contrib.comments.models import Comment
from django.contrib.sites.models import Site

def moderate_comments(instance, raw, **kwargs_ignored):
    """
    Applies comment moderation to newly-posted comments.
    
    Moderation happens in two phases:
    
        1. If the object the comment is being posted on has a method
           named ``comments_open``, it will be called; if the return
           value evaluates to ``False``, the comment's ``is_public``
           field will be set to ``False`` and no further processing
           will be done.
    
        2. If the object did not have a ``comments_open`` method, or
           if that method's return value evaluated to ``True``, then
           the comment will be submitted to Akismet for a spam check,
           and if Akismet thinks the comment is spam, then its
           ``is_public`` field will be set to ``False``.
    
    """

    if not instance.id: # Only check when the comment is first saved.

        content_object = instance.content_object
        comments_open = getattr(content_object, 'comments_open', None)

        if callable(comments_open) and not comments_open():
            instance.is_public = False

        elif hasattr(settings, 'AKISMET_API_KEY') and settings.AKISMET_API_KEY:
            from akismet import Akismet
            akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                                  blog_url='http://%s/' % Site.objects.get_current().domain)
            if akismet_api.verify_key():
                akismet_data = { 'comment_type': 'comment',
                                 'referrer': '',
                                 'user_ip': instance.ip_address,
                                 'user_agent': '' }
                if akismet_api.comment_check(instance.comment.encode('utf-8'), data=akismet_data, build_data=True):
                    instance.is_public = False


signals.pre_save.connect(moderate_comments, sender=Comment)

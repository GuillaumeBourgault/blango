from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

class Tag(models.Model):
    value = models.TextField(max_length=100)

    def __str__(self):
      return self.value


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    title = models.TextField(max_length=100)
    slug = models.SlugField()
    summary = models.TextField(max_length=500)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="posts")
    comments = GenericRelation("Comment")

    def __str__(self):
        return self.title


class Comment(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    # content_type will store something like "blog.post", just a string pointing to the right model
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id field stores the primary key in whatever model
    object_id = models.PositiveIntegerField()
    # content_object says that to successfully retrieve the foreign object, it needs to look
    # in content_type and object_id fields.  
    content_object = GenericForeignKey('content_type', 'object_id')

# currently, the Comment model does not limit comments, they could be attached to any model.
# it is possible to do:
# content_type = models.ForeignKey(
#     ContentType,
#     on_delete=models.CASCADE,
#     limit_choices_to={
#         "model__in": ("post", "author")
#     },
# )
# it's also possible that the choice is limited by other means, like from a validation rule or
# a form, a view, etc.

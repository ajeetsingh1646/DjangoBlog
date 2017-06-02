from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.

# MVC Model View Controller

#post manager
class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        #Post.objects.all() = super(PostManager,self).all()     both are same
        return super(PostManager,self).filter(draft= False).filter(publish__lte=timezone.now())

def upload_location(instance,filename):
    return "%s/%s" %(instance.title, filename)      #saves in tittle named folder in media_cdn

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length = 120)
    slug = models.SlugField(unique= True)
    image = models.ImageField(upload_to = upload_location,
                    null=True,
                    blank= True,
                    height_field= "height_field",
                    width_field = "width_field")        #gives height and width in admin
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default= False)
    publish = models.TimeField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager()

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:details',kwargs={"id":self.id})
        #return "/posts/%s/" %(self.id)

    class Meta:
        ordering = ["-timestamp", "-updated"]       #prints recent posts first

def create_slug(instance, new_slug = None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug= slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug= new_slug)
    return slug

def pre_post_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_post_reciever, sender=Post)
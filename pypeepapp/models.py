from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create a Peep Model
class Peep(models.Model):
    user = models.ForeignKey(
        User, related_name="peeps",
        on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="peep_like", blank=True)

    #Keep track of count of likes
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return (
            f"{self.user}"
            f"({self.created_at:%d-%m-%Y %H:%M}):"
            f"{self.body}..."
        )

# Create a User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                related_name="followed_by",
                symmetrical=False,
                blank=True)
    
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_img = models.ImageField(null=True, blank=True, upload_to="images/")

    profile_bio = models.CharField(null=True, blank=True, max_length=500)
    homepage_link = models.CharField(null=True, blank=True, max_length=500)
    facebook_link = models.CharField(null=True, blank=True, max_length=50)
    instagram_link = models.CharField(null=True, blank=True, max_length=50)
    linkedin_link = models.CharField(null=True, blank=True, max_length=50)
    
    def __str__(self):
        return self.user.username


# Create Profile when new User Signs Up
def create_profile(sender, instance, created,  **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # Have the user follow themselves
        user_profile.follows.set([instance.profile.id])

post_save.connect(create_profile, sender=User)
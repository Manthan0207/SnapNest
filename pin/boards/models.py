from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    img_title = models.CharField(max_length=50, default="")
    category = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="boards/images", default="")
    like_count = models.IntegerField(default=0)
    
    #making foreign key to get user who uploaded pin
    author = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    #The default=1 means that if no author is provided, the image will be automatically assigned to the user with id=1.

    def __str__(self):
        # Convert img_id to string before concatenation
        s = self.img_title+"-" + str(self.image_id)
        return s



class UserProfile(models.Model):
    #one to one rel between user & user profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    follow_count = models.IntegerField(default=0)
    follower_count = models.IntegerField(default=0)
    monthly_views = models.IntegerField(default=0)
    post_count = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return f"{self.user.username}"


    

#when the new user obj is saved then this signal will be executed
#here send means the the model that sends the obj
#created will be true only if the new user obj is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            follow_count=0,
            follower_count=0,
            monthly_views=0,
            post_count=0,
            bio="",
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    
class Like(models.Model) :
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    pin = models.ForeignKey(Image,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) :
        return f'{self.user.username} Liked {self.pin.image_id}'
    
class SavedPin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    pin = models.ForeignKey(Image, on_delete=models.CASCADE)  
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} saved {self.pin.img_title}'
    


class Notification(models.Model) :
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('follow', 'Follow'),
    )
    notification_receiver = models.ForeignKey(User , on_delete=models.CASCADE,related_name='receiver',db_index=True)
    notification_sender = models.ForeignKey(User , on_delete=models.CASCADE,related_name='sender' , db_index=True)
    pin = models.ForeignKey(Image , on_delete=models.CASCADE,null=True , blank=True , db_index=True)
    notification_type = models.CharField(max_length=20 , choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Notification from {self.notification_sender.username} to {self.notification_receiver.username} ({self.notification_type})"

    class Meta:
        ordering = ['-created_at']  


class Report(models.Model):
    REPORT_CATEGORIES = [
        ('spam', 'Spam or misleading'),
        ('nudity', 'Nudity or sexual content'),
        ('violence', 'Violence or abusive content'),
        ('hate_speech', 'Hate speech or harassment'),
        ('plagiarism', 'Plagiarism or copyright issue'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports_made")
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="reports_received")
    reported_pin = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True, related_name="reported_pins")

    reason = models.CharField(max_length=50, choices=REPORT_CATEGORIES)
    description = models.TextField(blank=True, null=True, help_text="Provide additional details (optional).")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Report by {self.reporter.username} - {self.reason} ({self.status})"

    class Meta:
        ordering = ["-created_at"]
        #The query results for these models will be ordered by created_at in descending order (newest first).
        #In Django models, Meta is an inner class that provides metadata about the model. It defines options that affect how Django interacts with the model, such as ordering, database table names, constraints, permissions, and more.

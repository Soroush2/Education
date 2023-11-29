from django.db import models
from django.contrib.auth.models import User


# main video model
class HomeVideo(models.Model):
    user = models.ManyToManyField(User)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to="videos/")

    # return video title
    def __str__(self):
        return self.title


# video comments model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(HomeVideo, on_delete=models.CASCADE, related_name="post_comments")
    reply = models.ForeignKey("self", on_delete=models.CASCADE, related_name="reply_comments", blank=True, null=True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    # return comment user and body
    def __str__(self):
        return f"{self.user} - {self.body[:30]}"


# purchase confirmation model
class BuyModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(HomeVideo, on_delete=models.CASCADE)

    # return buyer and the produce name and title
    def __str__(self):
        return f"{self.user.first_name} buy {self.video.title}"

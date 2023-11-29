from django.shortcuts import render
from django.views import View
from .models import HomeVideo, BuyModel
from .forms import CommentCreateForm, CommentReplyForm, VideoSearchForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin


# home view displaying the main produce
class HomeView(LoginRequiredMixin, View):
    form_class = VideoSearchForm

    # get the available videos for the main page
    def get(self, request):
        posts = HomeVideo.objects.all()
        buyer = BuyModel.objects.filter(user=request.user).exists()
        check = BuyModel.objects.all()
        user_buy = False
        if buyer:
            user_buy = True
        if request.GET.get("search"):
            posts = posts.filter(body__contains=request.GET["search"])

        return render(request, "home/home.html", {
            "posts": posts, 'user_buy': user_buy, "buyer": buyer, 'check': check})


# every video or produce details
class HomeDetail(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    # create post instance with primary key
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(HomeVideo, pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)

    # get the video details
    def get(self, request, *args, **kwargs):
        post = self.post_instance
        comments = post.post_comments.filter(is_reply=False)
        video = BuyModel.objects.filter(video=post)
        # video_users=video.user.all()

        return render(request, "home/course.html",
                      {"post": post, "comments": comments, "form": self.form_class,
                       "reply_form": self.form_class_reply, "video": video})
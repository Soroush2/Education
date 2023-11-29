from django import forms
from .models import Comment


# comment creation form
class CommentCreateForm(forms.ModelForm):
    # model form requirements
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body": forms.Textarea(attrs={"class": " form-control"})
        }


# reply to comment form
class CommentReplyForm(forms.ModelForm):
    # model form requirements
    class Meta:
        model = Comment
        fields = ("body",)


# searchin for video form
class VideoSearchForm(forms.Form):
    search = forms.CharField()

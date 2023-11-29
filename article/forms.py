from django import forms
from .models import Post


# form for creating articles
class CreateArticleForm(forms.ModelForm):
    title = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Title", "class": "form-control"}), label="")
    slug = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Slug", "class": "form-control"}), label="")
    content = forms.CharField(required=True, widget=forms.widgets.TextInput(
        attrs={"placeholder": "Content", "class": "form-control"}), label="")
    status = forms.ChoiceField(
        choices=[('0', 'Draft'), ('1', 'Publish')],
        widget=forms.Select(attrs={'class': 'form-control'})  # Optional: add a CSS class for styling
    )
    # model form requirements

    class Meta:
        model = Post # the original post model
        fields =['title', 'slug', 'content', 'status']
        exclude = ('author',)

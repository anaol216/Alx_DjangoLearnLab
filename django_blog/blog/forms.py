"""
Forms for user authentication, profile management, and blog posts.

This module contains custom forms for user registration, profile editing,
and blog post creation/editing.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag


class CustomUserCreationForm(UserCreationForm):
    """
    Extended user registration form with email field.
    
    Adds an email field to Django's default UserCreationForm
    and ensures all fields have proper styling.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap-like styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Choose a username'
            elif field_name == 'password1':
                field.widget.attrs['placeholder'] = 'Enter password'
            elif field_name == 'password2':
                field.widget.attrs['placeholder'] = 'Confirm password'
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    
    Allows users to update their username and email.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class PostForm(forms.ModelForm):
    """
    Form for creating and editing blog posts.
    
    Includes fields for title and content. The author is automatically
    set based on the logged-in user in the view.
    """
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter tags, separated by commas (e.g., tech, python)'
        }),
        help_text='Separate tags with commas.'
    )

    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post content here...',
                'rows': 10
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Populate tags field with existing tags
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Process tags
            tag_names = [name.strip() for name in self.cleaned_data['tags'].split(',') if name.strip()]
            new_tags = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                new_tags.append(tag)
            instance.tags.set(new_tags)
        return instance


class CommentForm(forms.ModelForm):
    """
    Form for creating and editing comments.
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment...',
                'rows': 3
            }),
        }


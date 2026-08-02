from django import forms
from .models import Profile, SkillOffered, SkillWanted, SwapRequest, Feedback

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
        }

class SkillOfferedForm(forms.ModelForm):
    class Meta:
        model = SkillOffered
        fields = ['skill', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class SkillWantedForm(forms.ModelForm):
    class Meta:
        model = SkillWanted
        fields = ['skill', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class SwapRequestForm(forms.ModelForm):
    class Meta:
        model = SwapRequest
        fields = ['to_profile','offered_skill','wanted_skill']
        

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['swap_request', 'rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
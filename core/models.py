from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    
    def __str__(self):
        return self.user.username
    
class SkillOffered(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.skill
    
class SkillWanted(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.skill
    
class SwapRequest(models.Model):
    from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='requested_swaps')
    to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_swaps')
    offered_skill = models.ForeignKey(SkillOffered, on_delete=models.CASCADE)
    wanted_skill = models.ForeignKey(SkillWanted, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')))
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.from_profile} -> {self.to_profile} ({self.offered_skill} for {self.wanted_skill})"
    
class Feedback(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    swap_request = models.ForeignKey(SwapRequest, on_delete=models.CASCADE)
    from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='feedback_given')
    to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='feedback_received')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.from_profile} -> {self.to_profile} ({self.rating})"
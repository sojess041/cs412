from django.db import models
from django.contrib.auth.models import User




SKILL_LEVEL_CHOICES = [
    ('B', 'Beginner'),
    ('I', 'Intermediate'),
    ('A', 'Advanced'),
]

DIFFICULTY_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced'),
]

CATEGORY_CHOICES = [
    ('Pop', 'Pop'),
    ('Broadway', 'Broadway'),
    ('Film Scores', 'Film Scores'),
    ('Classical', 'Classical'),
    ('Scores', 'Scores'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skill_level = models.CharField(max_length=1, choices=SKILL_LEVEL_CHOICES)
    favorite_genre = models.CharField(max_length=100, blank=True, null=True)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    favorites = models.ManyToManyField('SheetMusic', blank=True)  # <== line up same



    def __str__(self):
        return self.user.username
    
class Tag(models.Model):
    name = models.CharField(max_length = 50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class SheetMusic(models.Model):
    title = models.CharField(max_length=200)
    composer = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=100, choices=DIFFICULTY_CHOICES)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(upload_to='sheet_pdfs/', blank=True, null=True)
    preview_image = models.ImageField(upload_to='sheet_previews/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='sheet_covers/', blank=True, null=True)  # optional thumbnail
    tags = models.ManyToManyField(Tag, blank=True)  # if you have a Tag model



    def __str__(self):
        return f"{self.title} by {self.composer}"
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sheet = models.ForeignKey(SheetMusic, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'sheet')  # user can't favorite same sheet twice

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sheet = models.ForeignKey(SheetMusic, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5)

    class Meta:
        unique_together = ('user', 'sheet')

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} → {self.to_user}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sheet = models.ForeignKey(SheetMusic, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
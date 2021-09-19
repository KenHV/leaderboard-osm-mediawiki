from django.db import models

# Create your models here.
class Leaderboard(models.Model):
    display_name = models.CharField(max_length=24, primary_key=True)
    user_email = models.EmailField(unique=True)
    osm_username = models.CharField(max_length=256, unique=True)
    osm_orig_score = models.IntegerField()
    osm_current_score = models.IntegerField()
    mw_username = models.CharField(max_length=256, unique=True)
    mw_orig_score = models.IntegerField()
    mw_current_score = models.IntegerField()
    total_score = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_name']

    def __str__(self):
        return self.display_name

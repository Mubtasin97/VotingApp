from django.db import models

class VotingStatus(models.Model):
    is_voting_active = models.BooleanField(default=False)

class AdminUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)  # Plaintext for simplicity; change to hashed in production

class Voter(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Candidate(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Vote(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter', 'candidate')  # Ensure one vote per voter
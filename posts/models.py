import uuid
from django.db import models

from userprofile.models import UserProfile

class Post(models.Model):
    '''
        Model for posts
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    main_text = models.TextField(blank=False)
    votes = models.IntegerField(default=0, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        '''
            Meta class for posts
        '''

        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)


class Vote(models.Model):
    '''
        Model for votes
    '''

    UPVOTE = "up"
    DOWNVOTE = "do"

    VOTE_TYPE = [
        (UPVOTE, 'upvoted'),
        (DOWNVOTE, 'downvoted')
    ]

    owner = models.ForeignKey(UserProfile, primary_key=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, primary_key=True, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=2, choices=VOTE_TYPE, default=UPVOTE)
    ceated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        '''
            Meta class for Vote model
        '''

        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        ordering = ['-created_at']

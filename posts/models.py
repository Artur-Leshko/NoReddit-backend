import uuid
from django.contrib.auth import get_user_model
from userprofile.models import UserProfile
from django.db import models

User = get_user_model()

class Post(models.Model):
    '''
        Model for posts
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=False)
    main_text = models.TextField(blank=False)
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

    @property
    def upvotes(self):
        '''
            returns count of upvotes for post
        '''
        return Vote.objects.filter(post=self.id, vote_type='up').count()

    @property
    def downvotes(self):
        '''
            returns count of downvotes for post
        '''
        return Vote.objects.filter(post=self.id, vote_type='down').count()


class Vote(models.Model):
    '''
        Model for votes
    '''

    UPVOTE = "up"
    DOWNVOTE = "down"

    VOTE_TYPE = [
        (UPVOTE, 'upvoted'),
        (DOWNVOTE, 'downvoted')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=4, choices=VOTE_TYPE, default=UPVOTE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        '''
            Meta class for Vote model
        '''

        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        ordering = ['-created_at']

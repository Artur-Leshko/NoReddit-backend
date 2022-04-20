import uuid
from django.db import models

from posts.models import Post
from userprofile.models import UserProfile

class Comment(models.Model):
    '''
        Model for Comment
    '''

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=255, blank=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        '''
            Meta class for Comment model
        '''
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']

    def __str__(self):
        return str(self.text)

class CommentVote(models.Model):
    '''
        Model for Comment Vote
    '''

    UPVOTE = 'up'
    DOWNVOTE = 'down'

    VOTE_TYPE = [
        (UPVOTE, 'upvoted'),
        (DOWNVOTE, 'downvoted')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=4, choices=VOTE_TYPE, default=UPVOTE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        '''
            Meta class for CommentVote model
        '''
        verbose_name = 'Comment vote'
        verbose_name_plural = 'Comment votes'
        ordering = ['-created_at']

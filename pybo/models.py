from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Count

class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question')
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    bookmarks = models.ManyToManyField(User, through='Bookmark', related_name='bookmarked_questions', blank=True)

    def __str__(self):
        return self.subject

    @classmethod
    def get_recommended(cls):
        return cls.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')

    @classmethod
    def get_recent(cls):
        return cls.objects.order_by('-create_date')

    @classmethod
    def get_recommended_minvote(cls, min_votes=1):
        return cls.objects.annotate(num_voter=Count('voter')) \
                          .filter(num_voter__gte=min_votes) \
                          .order_by('-num_voter', '-create_date')

    @classmethod
    def get_recommended_auto(cls):
        qs_with_votes = cls.objects.annotate(num_voter=Count('voter')).filter(num_voter__gt=0)
        avg_votes = qs_with_votes.aggregate(avg_votes=Avg('num_voter'))['avg_votes'] or 0
        avg_votes = int(avg_votes)
        return cls.objects.annotate(num_voter=Count('voter')) \
            .filter(num_voter__gte=avg_votes)

    @classmethod
    def get_bookmarked(cls, user):
        if user.is_authentificated:
            return cls.objects.filter(bookmark__user=user).order_by('-bookmark__created_at')
        else:
            return cls.objects.none()

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    bookmarked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)


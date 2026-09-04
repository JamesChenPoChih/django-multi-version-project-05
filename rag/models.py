from django.db import models


class KnowledgeDocument(models.Model):
    title = models.CharField(max_length=200)
    source = models.CharField(max_length=300, blank=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

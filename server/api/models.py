from django.db import models


class Template(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    owner = models.ForeignKey('auth.user', related_name="templates",
                              on_delete=models.CASCADE)
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """ Return a string representation of the model.
        """
        return f"{self.title} by {self.owner.username}"

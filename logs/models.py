from django.db import models


class Backup(models.Model):
    """Implements the new model"""
    app = models.CharField(max_length=20)
    total_size = models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=40)
    total_files = models.IntegerField(default=0, blank=True, null=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    server = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    log = models.URLField()

    def __str__(self):
        return self.app + "_" + self.server + "_" + str(self.created_at.date())

    class Meta:
        ordering = ['-created_at']

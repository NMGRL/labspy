from django.db import models


# Create your models here.
class ImportRequest(models.Model):
    runlist_blob = models.BinaryField()
    experiment_identifier = models.CharField(max_length=200)
    requestor_name = models.CharField(max_length=200)
    request_date = models.DateTimeField(auto_created=True)
    imported_date = models.DateTimeField(default=None)
    is_irradiation = models.BooleanField(default=False)
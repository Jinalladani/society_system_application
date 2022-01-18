from django.db import models


class OtpSender(models.Model):
    number = models.IntegerField()
    otp_data = models.CharField(max_length=6)

    def __str__(self):
        return str(self.number)

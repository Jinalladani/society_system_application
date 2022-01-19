from django.db import models


class OtpSender(models.Model):
    number = models.CharField(max_length=50)
    otp_data = models.CharField(max_length=50)

    def __str__(self):
        return str(self.number)


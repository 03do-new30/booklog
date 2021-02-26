from django.db import models

# Create your models here.
class Account(models.Model):
    acc_id = models.CharField(max_length=20, null=True)
    acc_pw = models.CharField(max_length=30, null=True)
    acc_name = models.CharField(max_length=20, null=True)

    # 객체 생성
    def create(self, acc_id, acc_pw, acc_name):
        self.acc_id = acc_id
        self.acc_pw = acc_pw
        self.acc_name = acc_name
        self.save
    
    def __str__(self):
        return self.acc_id

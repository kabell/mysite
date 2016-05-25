from django.db import models


class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    page = models.CharField(max_length=50)
    sk = models.CharField(max_length=200)
    en = models.CharField(max_length=200)
    deleted = models.BooleanField()


class BlogPost(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    trailer = models.CharField(max_length=1000,null=True)
    content = models.CharField(max_length=20000)
    date = models.DateField()
    deleted = models.BooleanField()

class Page(models.Model):
    id = models.AutoField(primary_key=True)
    page = models.CharField(max_length=35, null=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=200)
    generator = models.CharField(max_length=50)
    date = models.DateField()
    tags = models.CharField(max_length=200)
    visible = models.BooleanField()
    deleted = models.BooleanField()

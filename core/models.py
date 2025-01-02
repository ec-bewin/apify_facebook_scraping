from django.db import models


class FBGroup(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    group_id = models.CharField(max_length=100,null=True,blank=True)
    run_id = models.CharField(max_length=100,null=True,blank=True)
    webhook_id = models.CharField(max_length=100,null=True,blank=True)
    url = models.URLField()
    defaultDatasetId = models.CharField(max_length=100,null=True,blank=True)
    is_updated = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    group = models.ForeignKey(FBGroup, on_delete=models.CASCADE, related_name='posts')
   
    content = models.TextField()
    user_id = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    post_id = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField()  
    likes_count = models.IntegerField(default=0)  
    shares_count = models.IntegerField(default=0)  
    comments_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

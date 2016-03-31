from django.db import models

# Create your models here.
class Author(models.Model):
	author_name = models.CharField(max_length=16)
	author_birth = models.CharField(max_length=8)
	author_death = models.CharField(max_length=8)
	author_desc = models.TextField()
	author_head_thumb = models.URLField()
	author_belong = models.CharField(max_length=8)
	entity_type = models.CharField(max_length=16, default="author")

class Poem(models.Model):
	poem_name = models.CharField(max_length=64)
	poem_content = models.TextField()
	poem_pinyin = models.TextField(null=True)
	poem_analysis = models.TextField()
	poem_kind = models.CharField(max_length=32,null=True)
	poem_year = models.CharField(max_length=8,null=True)
	entity_type = models.CharField(max_length=16, default="poem")

class Image(models.Model):
	image_name = models.CharField(max_length=32)
	entity_type = models.CharField(max_length=16, default="image")

class Emotion(models.Model):
	emotion_desc = models.TextField();
	entity_type = models.CharField(max_length=16, default="emotion")

class Author_Poem(models.Model):
	author_id = models.ForeignKey(Author)
	poem_id = models.ForeignKey(Poem)
	relation_type = models.CharField(max_length=16, default="author_poem")

class Poem_Image(models.Model):
	poem_id = models.ForeignKey(Poem)
	image_id = models.ForeignKey(Image)
	relation_type = models.CharField(max_length=16, default="poem_image")

class Image_Emotion(models.Model):
	image_id = models.ForeignKey(Image)
	emotion_id = models.ForeignKey(Emotion)
	relation_type = models.CharField(max_length=16, default="image_emotion")

	

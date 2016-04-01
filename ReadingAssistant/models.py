from django.db import models

# Create your models here.


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=16)
    author_belong = models.CharField(max_length=8)
    author_birth = models.CharField(max_length=8)
    author_death = models.CharField(max_length=8)
    author_desc = models.TextField()
    author_head_thumb = models.CharField(max_length=128)
    entity_type = models.CharField(max_length=16, default="author")

    class Meta:
        db_table = 'author_table'


class Poem(models.Model):
    poem_id = models.AutoField(primary_key=True)
    poem_name = models.CharField(max_length=64)
    poem_content = models.TextField()
    poem_pinyin = models.TextField(null=True)
    poem_analysis = models.TextField()
    poem_kind = models.CharField(max_length=32,null=True)
    poem_year = models.CharField(max_length=8,null=True)
    entity_type = models.CharField(max_length=16, default="poem")

    class Meta:
        db_table = 'poem_table'


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=32)
    entity_type = models.CharField(max_length=16, default="image")

    class Meta:
        db_table = 'image_table'


class Emotion(models.Model):
    emotion_id = models.AutoField(primary_key=True)
    emotion_desc = models.TextField();
    entity_type = models.CharField(max_length=16, default="emotion")

    class Meta:
        db_table = 'emotion_table'


class Author_Poem(models.Model):
    author = models.ForeignKey(Author)
    poem = models.ForeignKey(Poem)
    relation_type = models.CharField(max_length=16, default="author_poem")

    class Meta:
        db_table = 'author_poem_table'


class Poem_Image(models.Model):
    poem = models.ForeignKey(Poem)
    image = models.ForeignKey(Image)
    relation_type = models.CharField(max_length=16, default="poem_image")

    class Meta:
        db_table = 'poem_image_table'


class Image_Emotion(models.Model):
    image = models.ForeignKey(Image)
    emotion = models.ForeignKey(Emotion)
    relation_type = models.CharField(max_length=16, default="image_emotion")
    
    class Meta:
        db_table = 'image_emotion_table'
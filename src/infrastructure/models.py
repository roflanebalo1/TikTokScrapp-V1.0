from django.db import models

class TiktokHashtagsORM(models.Model):
    TYPE_CHOICES = [
        ('hashtag', 'Hashtag'),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    value = models.TextField(verbose_name="Дополнительная информация")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип данных")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления") 
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.name} ({self.type})"

    class Meta:
        verbose_name = "Хештеги"
        verbose_name_plural = "Хештеги"

class TiktokSongsORM(models.Model):
    TYPE_CHOICES = [
        ('song', 'Song'),
        ('author', 'Author'),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    author = models.CharField(max_length=255, verbose_name="Исполнитель")
    value = models.TextField(verbose_name="Дополнительная информация")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип данных")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления") 
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.name} ({self.type})"

    class Meta:
        verbose_name = "Песни"
        verbose_name_plural = "Песни"

class TiktokBreakoutSongsORM(models.Model):
    TYPE_CHOICES = [
        ('breakout_song', 'Breakout Song'),
        ('author', 'Author'),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    author = models.CharField(max_length=255, verbose_name="Исполнитель")
    value = models.TextField(verbose_name="Дополнительная информация")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип данных")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления") 
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.name} ({self.type})"

    class Meta:
        verbose_name = "Взлетающие песни"
        verbose_name_plural = "Взлетающие песни"

class TikTokSessionORM(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

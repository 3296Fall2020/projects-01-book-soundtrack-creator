# Generated by Django 3.1.2 on 2020-11-16 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='bookEmotionGraph',
            field=models.ImageField(default='bookgraphs/blank.png', upload_to='bookgraphs/', verbose_name='Book Bar Graph'),
        ),
    ]

# Generated by Django 2.2.6 on 2019-11-18 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_posts_sentiment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='post_id',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]

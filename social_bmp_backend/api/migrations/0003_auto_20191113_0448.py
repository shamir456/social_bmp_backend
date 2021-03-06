# Generated by Django 2.2.6 on 2019-11-13 04:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_posts_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='All',
            field=models.CharField(default=django.utils.timezone.now, max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='Angry',
            field=models.CharField(default='4', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='Haha',
            field=models.CharField(default='7', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='Like',
            field=models.CharField(default='66', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='Love',
            field=models.CharField(default='9k', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='Sad',
            field=models.CharField(default='8', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='Wow',
            field=models.CharField(default='7', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='num_comments',
            field=models.CharField(default='7k', max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posts',
            name='num_shares',
            field=models.CharField(default='9', max_length=6),
            preserve_default=False,
        ),
    ]

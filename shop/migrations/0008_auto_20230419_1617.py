# Generated by Django 3.2 on 2023-04-19 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='product',
        ),
        migrations.RemoveField(
            model_name='review',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
    ]

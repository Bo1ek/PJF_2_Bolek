# Generated by Django 5.0.2 on 2024-02-13 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_author_message2'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message2',
            new_name='ChatMessage',
        ),
    ]

# Generated by Django 5.0.6 on 2024-06-06 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_alter_category_sug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='sug',
            new_name='slug',
        ),
    ]

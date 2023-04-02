# Generated by Django 4.1.7 on 2023-04-02 08:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_control', '0004_remove_customuser_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ('created_at',)},
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_online',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

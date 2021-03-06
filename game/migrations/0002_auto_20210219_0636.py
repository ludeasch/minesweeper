# Generated by Django 3.1.6 on 2021-02-19 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='date_start_game',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='duration_seconds',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='total_duration_seconds',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='state',
            field=models.IntegerField(choices=[(0, 'new'), (1, 'started'), (2, 'paused'), (4, 'won'), (5, 'lost')], default=0),
        ),
    ]

# Generated by Django 4.1 on 2022-11-28 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_passes_club_passes_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='mvp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.player'),
        ),
    ]
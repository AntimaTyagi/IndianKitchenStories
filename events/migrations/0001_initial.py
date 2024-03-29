# Generated by Django 3.1.13 on 2022-01-17 02:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import events.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(upload_to=events.models.get_file_path)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('price', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackCommentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.CharField(max_length=275)),
                ('created_date', models.DateField()),
                ('modified_date', models.DateField()),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventId', to='events.eventmodel', verbose_name='eventId')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewcommenter', to=settings.AUTH_USER_MODEL, verbose_name='reviewcommenter')),
            ],
        ),
    ]

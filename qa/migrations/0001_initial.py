# Generated by Django 4.2.6 on 2023-11-18 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('added_at', models.DateField(auto_now=True)),
                ('edited_at', models.DateField(blank=True, null=True)),
                ('rating', models.IntegerField(blank=True, default=0)),
                ('author', models.ForeignKey(on_delete=models.SET('Deleted'), to=settings.AUTH_USER_MODEL)),
                ('category', models.ManyToManyField(blank=True, to='qa.category')),
                ('likes', models.ManyToManyField(blank=True, related_name='get_likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateField(auto_now=True)),
                ('text', models.TextField(null=True)),
                ('active', models.BooleanField(default=True)),
                ('best_answer', models.BooleanField(blank=True, default=False, null=True)),
                ('author', models.ForeignKey(on_delete=models.SET('Deleted'), to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='qa.answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa.question')),
            ],
        ),
    ]

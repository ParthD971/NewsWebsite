# Generated by Django 4.0.5 on 2022-06-21 05:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news_blog', '0010_alter_post_created_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('post', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='news_blog.post')),
                ('type', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='news_blog.notificationtype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
        migrations.AddField(
            model_name='applicationnotification',
            name='status',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='news_blog.notificationstatus'),
        ),
        migrations.AddField(
            model_name='applicationnotification',
            name='type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='news_blog.notificationtype'),
        ),
        migrations.AddField(
            model_name='applicationnotification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
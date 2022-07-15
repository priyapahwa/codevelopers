# Generated by Django 4.0.6 on 2022-07-13 19:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ChatRoom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("room_name", models.CharField(max_length=20, unique=True)),
                ("room_password", models.CharField(max_length=50)),
                ("is_occupied", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="ChatUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserAndRoom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "chat_room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.chatroom"
                    ),
                ),
                (
                    "chat_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="chat.chatuser"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="chatuser",
            name="chat_rooms",
            field=models.ManyToManyField(
                through="chat.UserAndRoom", to="chat.chatroom"
            ),
        ),
        migrations.AddField(
            model_name="chatuser",
            name="chat_user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="chatroom",
            name="chat_users",
            field=models.ManyToManyField(
                through="chat.UserAndRoom", to="chat.chatuser"
            ),
        ),
    ]

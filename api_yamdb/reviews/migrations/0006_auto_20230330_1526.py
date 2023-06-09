# Generated by Django 3.2 on 2023-03-30 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20230330_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.CreateModel(
            name='TitleGenre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.genre')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.title')),
            ],
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(through='reviews.TitleGenre', to='reviews.Genre', verbose_name='Жанр'),
        ),
    ]

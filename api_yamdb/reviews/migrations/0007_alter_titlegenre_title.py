# Generated by Django 3.2 on 2023-03-30 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20230330_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titlegenre',
            name='title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='reviews.title'),
        ),
    ]
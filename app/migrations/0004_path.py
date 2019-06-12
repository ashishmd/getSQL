# Generated by Django 2.1.7 on 2019-05-27 19:09

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_relations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_table_id', models.IntegerField()),
                ('final_table_id', models.IntegerField()),
                ('path', django_mysql.models.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

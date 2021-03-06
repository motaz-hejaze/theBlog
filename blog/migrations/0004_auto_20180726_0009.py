# Generated by Django 2.0.7 on 2018-07-26 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=50)),
                ('user', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('port', models.PositiveIntegerField()),
                ('use_TLC', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default='myimage', upload_to='post_images'),
            preserve_default=False,
        ),
    ]

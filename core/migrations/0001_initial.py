# Generated by Django 5.0.4 on 2024-08-07 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShopInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=500)),
                ('phone', models.CharField(max_length=11)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('image', models.ImageField(upload_to='cafe_info')),
                ('logo', models.ImageField(upload_to='logo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

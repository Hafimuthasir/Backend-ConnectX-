# Generated by Django 4.0.6 on 2022-12-24 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0016_posts_discount_price_posts_is_premium_posts_is_z_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='discount_price',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='posts',
            name='is_z',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='posts',
            name='lang',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='posts',
            name='price',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='repo',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='posts',
            name='zdescription',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='posts',
            name='zfile',
            field=models.FileField(blank=True, upload_to='C:/Users/AKAM/Desktop/React/week2/djangoproject/reactapp/src/uploads/zpostfile'),
        ),
    ]

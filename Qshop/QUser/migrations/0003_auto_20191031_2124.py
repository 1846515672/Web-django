# Generated by Django 2.1.8 on 2019-10-31 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QUser', '0002_auto_20191029_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='quser',
            name='identity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quser',
            name='gender',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='quser',
            name='picture',
            field=models.ImageField(default='image/photo.jpeg', upload_to='image'),
        ),
    ]
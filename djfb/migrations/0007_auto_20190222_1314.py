# Generated by Django 2.1.7 on 2019-02-22 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djfb', '0006_auto_20190222_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='position',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
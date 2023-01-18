# Generated by Django 3.2.16 on 2023-01-17 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0019_auto_20230116_1704'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasource',
            name='final_data_file_generate',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='datasource',
            name='project_id',
            field=models.BigIntegerField(),
        ),
    ]
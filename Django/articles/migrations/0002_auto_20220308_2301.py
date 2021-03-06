# Generated by Django 3.2.12 on 2022-03-08 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corperations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.CharField(max_length=20)),
                ('code', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='stock_analyze',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stocks',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stock_analyze',
            name='code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='stocks',
            name='date',
            field=models.DateField(),
        ),
    ]

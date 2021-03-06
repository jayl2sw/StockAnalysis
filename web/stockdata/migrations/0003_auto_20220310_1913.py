# Generated by Django 3.2.12 on 2022-03-10 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stockdata', '0002_auto_20220310_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analyzed_data',
            name='market_cap',
        ),
        migrations.RemoveField(
            model_name='analyzed_data',
            name='netincome_20',
        ),
        migrations.RemoveField(
            model_name='analyzed_data',
            name='netincome_21',
        ),
        migrations.RemoveField(
            model_name='analyzed_data',
            name='operatingincome_20',
        ),
        migrations.RemoveField(
            model_name='analyzed_data',
            name='operatingincome_21',
        ),
        migrations.RemoveField(
            model_name='analyzed_data',
            name='sales_20',
        ),
        migrations.RemoveField(
            model_name='analyzed_data',
            name='sales_21',
        ),
        migrations.AddField(
            model_name='corperations',
            name='market_cap',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='corperations',
            name='netincome_20',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='corperations',
            name='netincome_21',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='corperations',
            name='operatingincome_20',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='corperations',
            name='operatingincome_21',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='corperations',
            name='sales_20',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='corperations',
            name='sales_21',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

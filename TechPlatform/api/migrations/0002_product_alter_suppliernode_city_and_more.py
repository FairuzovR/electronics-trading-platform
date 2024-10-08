# Generated by Django 5.1.1 on 2024-09-20 13:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=50)),
                ('release_date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='suppliernode',
            name='city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='suppliernode',
            name='country',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='suppliernode',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='suppliernode',
            name='debt',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='suppliernode',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='suppliernode',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.suppliernode'),
        ),
        migrations.AddField(
            model_name='suppliernode',
            name='products',
            field=models.ManyToManyField(related_name='nodes', to='api.product'),
        ),
    ]

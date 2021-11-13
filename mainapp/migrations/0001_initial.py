# Generated by Django 3.2.9 on 2021-11-13 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('is_adult', models.BooleanField(default=False)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='mainapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('age', models.PositiveSmallIntegerField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainapp.city')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
                ('price', models.PositiveSmallIntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainapp.category')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('price', models.PositiveSmallIntegerField()),
                ('review', models.PositiveSmallIntegerField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainapp.client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='mainapp.product')),
            ],
        ),
    ]

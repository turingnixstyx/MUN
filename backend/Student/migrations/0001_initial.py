# Generated by Django 4.2.4 on 2023-08-04 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Test Name', max_length=255)),
                ('email', models.EmailField(default='sample@email.com', max_length=254, unique=True)),
                ('contact', models.CharField(default='1111111111', max_length=10)),
                ('standard', models.IntegerField(default=10)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school_student', to='Student.school')),
            ],
        ),
    ]

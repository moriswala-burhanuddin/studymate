# Generated by Django 5.1.4 on 2025-05-09 13:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_yearsemester_alter_studymaterial_year_or_semester'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.course')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.university')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('year_or_semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.yearsemester')),
            ],
        ),
    ]

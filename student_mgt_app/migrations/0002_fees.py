# Generated by Django 4.0.4 on 2022-09-21 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_mgt_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fees',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('total_fee', models.FloatField()),
                ('paid_fee', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_mgt_app.students')),
            ],
        ),
    ]

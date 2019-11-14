# Generated by Django 2.1.5 on 2019-02-04 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('username', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ride',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dest', models.CharField(max_length=20)),
                ('arrive_t', models.TimeField()),
                ('v_type', models.CharField(max_length=20)),
                ('special', models.CharField(max_length=20)),
                ('number', models.IntegerField(default=1)),
                ('s_num', models.IntegerField(default=0)),
                ('shared', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('O', 'open'), ('D', 'during'), ('C', 'completed')], max_length=20)),
                ('driver', models.CharField(blank=True, max_length=20, null=True)),
                ('owner', models.CharField(max_length=20)),
                ('sharer', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='driver',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='myUber.account')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=20)),
                ('license_number', models.CharField(max_length=20)),
                ('space', models.IntegerField(default=0)),
                ('special_info', models.CharField(default='None', max_length=20)),
            ],
        ),
    ]
# Generated by Django 5.0.6 on 2024-07-20 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_user_groups_alter_user_user_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentComparison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('investment_name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('tenor', models.IntegerField()),
                ('risk_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
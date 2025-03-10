# Generated by Django 5.1.5 on 2025-01-21 14:05

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=20)),
                ('note', models.TextField(blank=True, null=True)),
                ('user_id', models.IntegerField()),
            ],
            options={
                'db_table': 'contacts',
            },
        ),
        migrations.CreateModel(
            name='StockData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_high', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_low', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_open', models.DecimalField(decimal_places=2, max_digits=10)),
                ('week_52_high', models.DecimalField(decimal_places=2, max_digits=10)),
                ('week_52_low', models.DecimalField(decimal_places=2, max_digits=10)),
                ('previous_close_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('day_change', models.DecimalField(decimal_places=2, max_digits=10)),
                ('volume', models.BigIntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'stock_data',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='last login')),
                ('money_invested', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('money_spent', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('income_by_week', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('balance_goal', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('spent_by_week', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('spent_by_month', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('spent_by_year', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('income_by_year', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('income_by_month', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('password', models.CharField(max_length=100)),
                ('photo', models.URLField(blank=True, max_length=255, null=True)),
                ('reset_token', models.CharField(blank=True, max_length=64, null=True)),
                ('reset_token_expiry', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='custom_user_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='auth.permission')),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='CustomCashFlowInvestment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateField()),
                ('title', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tenor', models.CharField(max_length=255)),
                ('type_invest', models.CharField(max_length=255)),
                ('cash_flows', models.JSONField()),
                ('discount_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('IRR', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('NPV', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'custom_cash_flow_investments',
            },
        ),
        migrations.CreateModel(
            name='FinancialRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('record_date', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'financial_records',
            },
        ),
        migrations.CreateModel(
            name='IncomeRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('record_date', models.DateField()),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'income_records',
            },
        ),
        migrations.CreateModel(
            name='InvestingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_date', models.DateField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tenor', models.CharField(blank=True, max_length=255, null=True)),
                ('type_invest', models.CharField(blank=True, max_length=255, null=True)),
                ('amount_at_maturity', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True)),
                ('maturity_date', models.DateField(blank=True, null=True)),
                ('discount_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('yearly_income', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investing_records', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'investing_records',
            },
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('datetime', models.DateTimeField()),
                ('done', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'meetings',
            },
        ),
        migrations.CreateModel(
            name='MonthlyExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_expenses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'monthly_expenses',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('note', models.TextField()),
                ('date', models.DateField(blank=True, null=True)),
                ('priority', models.CharField(max_length=50)),
                ('done', models.BooleanField(default=False)),
                ('hide', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notes',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('new_transaction', 'New Transaction')], max_length=50)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Notifications',
            },
        ),
        migrations.CreateModel(
            name='PlaidItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=255)),
                ('item_id', models.CharField(max_length=255)),
                ('previous_item_id', models.CharField(blank=True, max_length=255, null=True)),
                ('cursor', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'PlaidItem',
            },
        ),
        migrations.CreateModel(
            name='SleepLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('sleep_time', models.DateTimeField()),
                ('wake_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'sleep_logs',
            },
        ),
        migrations.CreateModel(
            name='TrackedAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=255)),
                ('account_name', models.CharField(max_length=255)),
                ('account_mask', models.CharField(blank=True, max_length=4, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.plaiditem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'TrackedAccount',
            },
        ),
    ]

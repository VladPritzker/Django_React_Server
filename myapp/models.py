from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField('last login', default=timezone.now, blank=True, null=True)
    money_invested = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    money_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    income_by_week = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    balance_goal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    spent_by_week = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    spent_by_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    spent_by_year = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    income_by_year = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    income_by_month = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    password = models.CharField(max_length=100)
    photo = models.URLField(max_length=255, null=True, blank=True)  # URL field for storing image URLs
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)
    reset_token = models.CharField(max_length=64, blank=True, null=True)
    reset_token_expiry = models.DateTimeField(blank=True, null=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email



class FinancialRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    record_date = models.DateField()
    
    class Meta:
        db_table = 'financial_records'

    def __str__(self):
        return f"{self.title} on {self.record_date} for ${self.amount}"



class InvestingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investing_records')
    record_date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tenor = models.CharField(max_length=255, null=True, blank=True)
    type_invest = models.CharField(max_length=255, null=True, blank=True)
    amount_at_maturity = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)    
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    yearly_income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # New field


    class Meta:
        db_table = 'investing_records'

    def __str__(self):
        return f"{self.title} on {self.record_date} for ${self.amount}"
    
class CustomCashFlowInvestment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    record_date = models.DateField()
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenor = models.CharField(max_length=255)
    type_invest = models.CharField(max_length=255)
    cash_flows = models.JSONField()
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    IRR = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    NPV = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'custom_cash_flow_investments'

    def __str__(self):
        return f"{self.title} on {self.record_date} for ${self.amount}"
    



class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    note = models.TextField()
    date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=50)
    done = models.BooleanField(default=False)
    hide = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'notes'

    def __str__(self):
        return self.title

class MonthlyExpense(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='monthly_expenses'
    )
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'monthly_expenses'

    def __str__(self):
        return f"{self.title}: {self.amount}"

class IncomeRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    record_date = models.DateField()
    transaction_id = models.CharField(max_length=255, unique=True, null=True, blank=True)


    class Meta:
        db_table = 'income_records'

    def __str__(self):
        return f"{self.title} - {self.amount} - {self.record_date}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    note = models.TextField(null=True, blank=True)
    user_id = models.IntegerField()

    class Meta:
        db_table = 'contacts'

    def __str__(self):
        return self.name

class Meeting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    datetime = models.DateTimeField()
    done = models.BooleanField(default=False)

    class Meta:
        db_table = 'meetings'

    def __str__(self):
        return self.title

class SleepLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    sleep_time = models.DateTimeField()
    wake_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sleep_logs'

    def __str__(self):
        return f'{self.user.username} - {self.date}'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date,
            'sleep_time': self.sleep_time,
            'wake_time': self.wake_time,
            'created_at': self.created_at,
        }



class StockData(models.Model):
    ticker = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    day_high = models.DecimalField(max_digits=10, decimal_places=2)
    day_low = models.DecimalField(max_digits=10, decimal_places=2)
    day_open = models.DecimalField(max_digits=10, decimal_places=2)
    week_52_high = models.DecimalField(max_digits=10, decimal_places=2)
    week_52_low = models.DecimalField(max_digits=10, decimal_places=2)
    previous_close_price = models.DecimalField(max_digits=10, decimal_places=2)
    day_change = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stock_data'            
    
    def __str__(self):
        return self.ticker





class PlaidItem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    item_id = models.CharField(max_length=255)
    previous_item_id = models.CharField(max_length=255, null=True, blank=True)
    cursor = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        db_table = 'PlaidItem'

    def __str__(self):
        return f"{self.user.username}'s Plaid Item"





class TrackedAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=255)
    account_name = models.CharField(max_length=255)
    account_mask = models.CharField(max_length=4, null=True, blank=True)
    item = models.ForeignKey(PlaidItem, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'TrackedAccount'

    def __str__(self):
        return f"{self.account_name} ending with {self.account_mask}"

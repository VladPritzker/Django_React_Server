from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


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
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email


class FinancialRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='financial_records')
    record_date = models.DateField()
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'financial_records'

    def __str__(self):
        return f"{self.title} on {self.record_date} for ${self.amount}"

class InvestingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investing_records')
    record_date = models.DateField()
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenor = models.CharField(max_length=100)
    type_invest = models.CharField(max_length=100)
    amount_at_maturity = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)  # Add this line

    class Meta:
        db_table = 'investing_records'

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
    order = models.IntegerField(default=0)  # Ensure this field exists

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
    datetime = models.DateTimeField()  # Ensure no timezone conversion here
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


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, FinancialRecord, InvestingRecord, Note, MonthlyExpense, IncomeRecord, Contact, Meeting, SleepLog

class MyUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)

class MyUserAdmin(BaseUserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('email', 'username', 'is_active', 'is_staff', 'money_invested', 'money_spent', 'balance')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'money_invested', 'money_spent', 'balance')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

class InvestingRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'record_date', 'title', 'amount', 'tenor', 'type_invest', 'amount_at_maturity', 'maturity_date', 'discount_rate', 'yearly_income')
    fields = ('user', 'record_date', 'title', 'amount', 'tenor', 'type_invest', 'amount_at_maturity', 'maturity_date', 'discount_rate', 'yearly_income')


# Register the User model with the custom admin class
admin.site.register(User, MyUserAdmin)

# Register other models without custom admin classes
admin.site.register(FinancialRecord)
admin.site.register(InvestingRecord, InvestingRecordAdmin)
admin.site.register(Note)
admin.site.register(MonthlyExpense)
admin.site.register(IncomeRecord)
admin.site.register(Contact)
admin.site.register(Meeting)
admin.site.register(SleepLog)

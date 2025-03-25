from django.test import TestCase
from django.utils import timezone
from myapp.models import (
    User, FinancialRecord, InvestingRecord, CustomCashFlowInvestment, Note,
    MonthlyExpense, IncomeRecord, Contact, Meeting, SleepLog, Notification
)


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpassword123'))
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_user_string_representation(self):
        # The __str__ for User might return the email by default.
        self.assertEqual(str(self.user), 'testuser@example.com')


class FinancialRecordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            username='user',
            password='pass'
        )
        self.record = FinancialRecord.objects.create(
            user=self.user,
            transaction_id='txn_001',
            title='Salary',
            amount=5000.00,
            record_date='2024-01-01'
        )

    def test_financial_record_creation(self):
        self.assertEqual(self.record.title, 'Salary')
        self.assertEqual(self.record.amount, 5000.00)
        # Ensure the model's __str__ shows two decimal places
        self.assertEqual(str(self.record), 'Salary on 2024-01-01 for $5000.00')


class InvestingRecordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='investor@example.com',
            username='investor',
            password='pass'
        )
        self.record = InvestingRecord.objects.create(
            user=self.user,
            record_date='2024-01-01',
            title='Bond',
            amount=1000.00
        )

    def test_investing_record(self):
        self.assertEqual(self.record.title, 'Bond')
        # Again, checking the two-decimal format
        self.assertEqual(str(self.record), 'Bond on 2024-01-01 for $1000.00')


class CustomCashFlowInvestmentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='cashflow@example.com',
            username='cashflow',
            password='pass'
        )
        self.investment = CustomCashFlowInvestment.objects.create(
            user=self.user,
            record_date='2024-02-01',
            title='Real Estate',
            amount=200000.00,
            tenor='5 years',
            type_invest='Rental',
            cash_flows={"Year1": 20000, "Year2": 21000},
            discount_rate=5.00
        )

    def test_cash_flow_creation(self):
        self.assertEqual(self.investment.title, 'Real Estate')
        self.assertEqual(self.investment.cash_flows, {"Year1": 20000, "Year2": 21000})


class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='noteuser@example.com',
            username='noteuser',
            password='pass'
        )
        self.note = Note.objects.create(
            user=self.user,
            title='Test Note',
            note='This is a test note.',
            priority='High',
            done=False
        )

    def test_note_creation(self):
        self.assertEqual(self.note.title, 'Test Note')


class IncomeRecordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='income@example.com',
            username='incomeuser',
            password='pass'
        )
        self.record = IncomeRecord.objects.create(
            user=self.user,
            title='Consulting',
            amount=3000.00,
            record_date='2024-03-01'
        )

    def test_income_record(self):
        # Checking the exact string format with two decimals
        self.assertEqual(str(self.record), 'Consulting - 3000.00 - 2024-03-01')


class MonthlyExpenseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='expense@example.com',
            username='expenseuser',
            password='pass'
        )
        self.expense = MonthlyExpense.objects.create(
            user=self.user,
            title='Rent',
            amount=1200.00
        )

    def test_expense_creation(self):
        self.assertEqual(self.expense.title, 'Rent')


class ContactModelTest(TestCase):
    def test_contact_creation(self):
        contact = Contact.objects.create(name='Alice', phone_number='1234567890', user_id=1)
        self.assertEqual(contact.name, 'Alice')


class NotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='notify@example.com',
            username='notifyuser',
            password='pass'
        )
        self.notification = Notification.objects.create(
            user=self.user,
            notification_type='new_transaction',
            message='A new transaction occurred'
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.notification_type, 'new_transaction')
        self.assertEqual(
            str(self.notification),
            'Notification for notifyuser: A new transaction occurred'
        )

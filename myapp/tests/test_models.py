from django.test import TestCase
from myapp.models import (
    User, FinancialRecord, InvestingRecord, CustomCashFlowInvestment, Note,
    MonthlyExpense, IncomeRecord, Contact, Meeting, SleepLog, StockData,
    PlaidItem, TrackedAccount, Notification
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
        self.assertEqual(str(self.user), 'testuser@example.com')


class FinancialRecordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user@example.com', 'pass')
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
        self.assertEqual(str(self.record), 'Salary on 2024-01-01 for $5000.00')


class InvestingRecordTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('investor@example.com', 'pass')
        self.record = InvestingRecord.objects.create(
            user=self.user,
            record_date='2024-01-01',
            title='Bond',
            amount=1000.00
        )

    def test_investing_record(self):
        self.assertEqual(self.record.title, 'Bond')
        self.assertEqual(str(self.record), 'Bond on 2024-01-01 for $1000.00')


class CustomCashFlowInvestmentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('cashflow@example.com', 'pass')
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
        self.user = User.objects.create_user('noteuser@example.com', 'pass')
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
        self.user = User.objects.create_user('income@example.com', 'pass')
        self.record = IncomeRecord.objects.create(
            user=self.user,
            title='Consulting',
            amount=3000.00,
            record_date='2024-03-01'
        )

    def test_income_record(self):
        self.assertEqual(str(self.record), 'Consulting - 3000.00 - 2024-03-01')


class MonthlyExpenseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('expense@example.com', 'pass')
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


class MeetingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('meeting@example.com', 'pass')
        self.meeting = Meeting.objects.create(
            user=self.user,
            title='Team Sync',
            datetime='2024-04-10T10:00:00Z'
        )

    def test_meeting_creation(self):
        self.assertEqual(self.meeting.title, 'Team Sync')


class SleepLogTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('sleep@example.com', 'pass')
        self.log = SleepLog.objects.create(
            user=self.user,
            date='2024-04-10',
            sleep_time='2024-04-10T23:00:00Z',
            wake_time='2024-04-11T07:00:00Z'
        )

    def test_sleep_log_creation(self):
        self.assertEqual(str(self.log), 'sleep@example.com - 2024-04-10')


class NotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('notify@example.com', 'pass')
        self.notification = Notification.objects.create(
            user=self.user,
            notification_type='new_transaction',
            message='A new transaction occurred'
        )

    def test_notification_creation(self):
        self.assertEqual(self.notification.notification_type, 'new_transaction')

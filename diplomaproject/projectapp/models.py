from django.db import models
from django.contrib.auth.models import User




class UserIncome(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    income_choices = [
        ('Less than 150,000', 'Less than 150,000 tenge'),
        ('150,000 - 250,000', '150,000 - 250,000 tenge'),
        ('250,000 - 350,000', '250,000 - 350,000 tenge'),
        ('350,000 - 400,000', '350,000 - 400,000 tenge'),
        ('400,000 - 500,000', '400,000 - 500,000 tenge'),
        ('More than 500,000', 'More than 500,000 tenge'),
    ]
    income = models.CharField(max_length=20, choices=income_choices)

class UserSpending(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category_choices = [
        ('Groceries', 'Groceries'),
        ('Rent/Mortgage', 'Rent/Mortgage'),
        ('Utilities', 'Utilities'),
        ('Transportation', 'Transportation'),
        ('Dining out', 'Dining out'),
        ('Entertainment', 'Entertainment'),
        ('Clothing', 'Clothing'),
        ('Health/Insurance', 'Health/Insurance'),
        ('Other', 'Other'),
    ]
    category = models.CharField(max_length=20, choices=category_choices)
    spending_choices = [
        ('Less than 20,000', 'Less than 20,000 tenge'),
        ('20,000 - 60,000', '20,000 - 60,000 tenge'),
        ('60,000 - 100,000', '60,000 - 100,000 tenge'),
        ('100,000 - 150,000', '100,000 - 150,000 tenge'),
        ('More than 150,000', 'More than 150,000 tenge'),
    ]
    spending = models.CharField(max_length=20, choices=spending_choices)

class BudgetReview(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    review_choices = [
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
        ('Annually', 'Annually'),
        ('No review', 'I do not review or adjust my budget'),
    ]
    review_frequency = models.CharField(max_length=20, choices=review_choices)
    priority_choices = [
        ('Necessities', 'Necessities first, then savings, then discretionary spending'),
        ('Discretionary', 'Discretionary spending first, then necessities, then savings'),
        ('Balanced', 'Balanced approach to all categories'),
    ]
    spending_priority = models.CharField(max_length=50, choices=priority_choices)
    significant_changes = models.BooleanField(default=False)
    saving_strategies = models.BooleanField(default=False)
    irregular_expenses_handling = models.CharField(max_length=100)
    challenges = models.CharField(max_length=100)
    cash_tracking = models.CharField(max_length=100)



class Choices(models.Model):
    choice_text = models.CharField(max_length=100)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    ans = models.ManyToManyField(
        Choices,
    )


class UserResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.ForeignKey(Choices, on_delete=models.CASCADE)

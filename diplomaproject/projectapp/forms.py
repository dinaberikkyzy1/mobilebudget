# forms.py

from django import forms
from .models import UserIncome, UserSpending, BudgetReview

class IncomeForm(forms.ModelForm):
    class Meta:
        model = UserIncome
        fields = ['income', ]

class SpendingForm(forms.ModelForm):
    class Meta:
        model = UserSpending
        fields = ['category', 'spending']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = BudgetReview
        fields = ['review_frequency', 'spending_priority', 'significant_changes', 'saving_strategies', 'irregular_expenses_handling', 'challenges', 'cash_tracking']

from django import forms
from django.utils.translation import gettext_lazy as _
from .models import BookInstance
from .constants import DEFAULT_LOAN_PERIOD_WEEKS
import datetime

class BorrowBookForm(forms.Form):
    due_back = forms.DateField(
        label=_('Due date'),
        help_text=_('Enter a date between now and {} weeks (default {}).'.format(
            DEFAULT_LOAN_PERIOD_WEEKS['max'],
            DEFAULT_LOAN_PERIOD_WEEKS['default']
        )),
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        if data < datetime.date.today():
            raise forms.ValidationError(_('Invalid date - borrowing in past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=DEFAULT_LOAN_PERIOD_WEEKS['max']):
            raise forms.ValidationError(_('Invalid date - borrowing more than {} weeks ahead').format(
                DEFAULT_LOAN_PERIOD_WEEKS['max']
            ))
        return data

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        label=_("Renewal date"),  # Đảm bảo label này khớp với test
        help_text=_("Enter a date between now and 4 weeks (default 3)."),
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        today = datetime.date.today()
        
        if data < today:
            raise forms.ValidationError(_('Invalid date - renewal in past'))
        
        if data > today + datetime.timedelta(weeks=4):
            raise forms.ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        
        return data


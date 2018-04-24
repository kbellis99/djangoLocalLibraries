from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
from django import forms

class RenewBookForm(forms.Form):
    renewalDate = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def cleanRenewalDate(self):
        data = self.cleanedData['renewalDate']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid Date - Renewal in Past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid Date - Renewal more than 4 weeks ahead.'))
        return data

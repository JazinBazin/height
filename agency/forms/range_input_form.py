from django import forms


class RangeInputForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop('name')
        super().__init__(*args, **kwargs)

        self.fields[self.name + '_from'] = forms.FloatField(
            label='',
            required=False,
            widget=forms.NumberInput(attrs={'placeholder': 'От'})
        )

        self.fields[self.name + '_to'] = forms.FloatField(
            label='',
            required=False,
            widget=forms.NumberInput(attrs={'placeholder': 'До'})
        )

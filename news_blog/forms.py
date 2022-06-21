from django import forms


class ManagerApplicationForm(forms.Form):
    check = forms.BooleanField(label='I have read and agree the terms and conditions.', required=True)


class EditorApplicationForm(forms.Form):
    check = forms.BooleanField(label='I have read and agree the terms and conditions.', required=True)




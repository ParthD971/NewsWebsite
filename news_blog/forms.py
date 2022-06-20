from django import forms


class ManagerApplicationForm(forms.Form):
    check = forms.BooleanField(label='label', label_suffix='lable suff', help_text='help text')


class EditorApplicationForm(forms.Form):
    check = forms.BooleanField(label='label', label_suffix='lable suff', help_text='help text')




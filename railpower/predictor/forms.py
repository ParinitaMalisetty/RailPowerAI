from django import forms

class InputForm(forms.Form):
    Voltage = forms.FloatField()
    Current = forms.FloatField()
    Temperature = forms.FloatField()
    Vibration = forms.FloatField()
    Speed = forms.FloatField()

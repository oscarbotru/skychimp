from django import forms

from mailing.models import MailingSettings, Client, MailingMessage


class MailingSettingsForm(forms.ModelForm):

    class Meta:
        model = MailingSettings
        fields = '__all__'


class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(forms.ModelForm):

    class Meta:
        model = MailingMessage
        fields = '__all__'

from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from mailing.forms import MailingSettingsForm, ClientForm, MessageForm
from mailing.models import MailingSettings, Client, MailingClient, MailingMessage


class MailingListView(ListView):
    model = MailingSettings
    extra_context = {
        'title': 'Список рассылок'
    }


class MailingSettingsCreateView(CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingSettingsDeleteView(DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('mailing:mailing_list')


class MailingClientsListView(ListView):
    model = MailingClient

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['clients'] = Client.objects.all()
        context_data['mailing_pk'] = self.kwargs.get('pk')
        return context_data


def toggle_client(request, pk, client_pk):
    if MailingClient.objects.filter(client_id=client_pk, settings_id=pk).exists():
        MailingClient.objects.filter(client_id=client_pk, settings_id=pk).delete()
    else:
        MailingClient.objects.create(client_id=client_pk, settings_id=pk)
    return redirect(reverse('mailing:mailing_clients', args=[pk]))


class ClientListView(ListView):
    model = Client
    extra_context = {
        'title': 'Список клиентов'
    }


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:clients')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailing:clients')


class MessageListView(ListView):
    model = MailingMessage
    extra_context = {
        'title': 'Список сообщений'
    }


class MessageCreateView(CreateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')


class MessageUpdateView(UpdateView):
    model = MailingMessage
    form_class = MessageForm
    success_url = reverse_lazy('mailing:messages')


class MessageDeleteView(DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('mailing:messages')

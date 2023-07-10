import datetime

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import MailingSettings, MailingLog


def send_email(ms, mc):
    result = send_mail(
        subject=ms.message.subject,
        message=ms.message.message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[mc.client.email],
        fail_silently=False
    )

    MailingLog.objects.create(
        status=MailingLog.STATUS_OK if result else MailingLog.STATUS_FAILED,
        settings=ms,
        client=mc
    )


def send_mails():
    now = datetime.datetime.now()
    for ms in MailingSettings.objects.filter(status=MailingSettings.STATUS_STARTED):
        for mc in ms.mailingclient_set.all():
            ml = MailingLog.objects.filter(client=mc.client, settings=ms)
            if ml.exists():
                last_try_date = ml.order_by('-last_try').first()
                if ms.period == MailingSettings.PERIOD_DAILY:
                    if (now - last_try_date).days >= 1:
                        send_email(ms, mc)
                elif ms.period == MailingSettings.PERIOD_WEEKLY:
                    if (now - last_try_date).days >= 7:
                        send_email(ms, mc)
                elif ms.period == MailingSettings.PERIOD_MONTHLY:
                    if (now - last_try_date).days >= 30:
                        send_email(ms, mc)
            else:
                send_email(ms, mc)

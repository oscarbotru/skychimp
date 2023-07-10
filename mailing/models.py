from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(verbose_name='Почта для рассылки')
    first_name = models.CharField(**NULLABLE, verbose_name='Имя', max_length=150)
    last_name = models.CharField(**NULLABLE, verbose_name='Фамилия', max_length=150)
    comment = models.TextField(**NULLABLE, verbose_name='Комментарий')

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingSettings(models.Model):

    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц'),
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'
    STATUSES = (
        (STATUS_STARTED, 'Запущена'),
        (STATUS_CREATED, 'Создана'),
        (STATUS_DONE, 'Завершена'),
    )

    time = models.TimeField(verbose_name='Время')
    period = models.CharField(max_length=20, choices=PERIODS, default=PERIOD_DAILY, verbose_name='Период')
    status = models.CharField(max_length=20, choices=STATUSES, default=STATUS_CREATED, verbose_name='Статус')

    message = models.ForeignKey('MailingMessage', on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)

    def __str__(self):
        return f'{self.time} / {self.period}'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class MailingClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройка')

    def __str__(self):
        return f'{self.client} / {self.settings}'

    class Meta:
        verbose_name = 'Клиент рассылки'
        verbose_name_plural = 'Клиенты рассылки'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=250, verbose_name='Тема')
    message = models.TextField(verbose_name='Тело')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingLog(models.Model):
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    settings = models.ForeignKey(MailingSettings, on_delete=models.CASCADE, verbose_name='Настройка')

    status = models.CharField(choices=STATUSES, default=STATUS_OK, verbose_name='Статус')

    last_try = models.DateTimeField(auto_now_add=True, verbose_name='Дата последней попытки')

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

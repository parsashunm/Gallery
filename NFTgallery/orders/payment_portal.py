import logging

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from azbankgateways import (
    bankfactories,
    models as bank_models,
    default_settings as settings,
)
from azbankgateways.exceptions import AZBankGatewaysException


def go_to_gateway_view(request, amount, number):
    user_mobile_number = number

    factory = bankfactories.BankFactory()
    try:
        bank = (
            factory.auto_create()
        )  # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        bank.set_client_callback_url(reverse('orders:verify_purchase'))
        bank.set_mobile_number(user_mobile_number)
        bank_record = bank.ready()

        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e
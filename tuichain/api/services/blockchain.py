from django.conf import settings
from itertools import repeat
from statistics import median, StatisticsError
from tuichain_ethereum import Controller, LoanPhase

controller = Controller(
    provider=settings.ETHEREUM_PROVIDER,
    master_account_private_key=settings.ETHEREUM_MASTER_ACCOUNT_PRIVATE_KEY,
    contract_address=settings.ETHEREUM_CONTROLLER_ADDRESS,
)

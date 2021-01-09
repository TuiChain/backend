from django.conf import settings
from tuichain_ethereum import Controller

controller = Controller(
    provider=settings.ETHEREUM_PROVIDER,
    master_account_private_key=settings.ETHEREUM_MASTER_ACCOUNT_PRIVATE_KEY,
    contract_address=settings.ETHEREUM_CONTROLLER_ADDRESS,
)

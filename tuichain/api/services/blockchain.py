from django.conf import settings
from tuichain_ethereum import Controller


def init():
    """
    Get the Blockchain controller
    """

    if (
        settings.ETHEREUM_MASTER_ACCOUNT_PRIVATE_KEY is not None
        and settings.ETHEREUM_CONTROLLER_ADDRESS is not None
    ):

        return Controller(
            provider=settings.ETHEREUM_PROVIDER,
            master_account_private_key=settings.ETHEREUM_MASTER_ACCOUNT_PRIVATE_KEY,
            contract_address=settings.ETHEREUM_CONTROLLER_ADDRESS,
        )

    else:

        return None

from django.conf import settings
from itertools import repeat
from statistics import median, StatisticsError
from tuichain_ethereum import Controller, LoanPhase

controller = Controller(
    provider=settings.ETHEREUM_PROVIDER,
    master_account_private_key=settings.ETHEREUM_MASTER_ACCOUNT_PRIVATE_KEY,
    contract_address=settings.ETHEREUM_CONTROLLER_ADDRESS,
)


def retrieve_current_price(fetched_loan):
    loan_state = fetched_loan.get_state()

    if loan_state.phase in [
        LoanPhase.FUNDING,
        LoanPhase.CANCELED,
        LoanPhase.EXPIRED,
    ]:
        value_atto_dai = 10 ** 18

    elif loan_state.phase == LoanPhase.ACTIVE:
        try:
            value_atto_dai = median(
                repeat(sp.price_atto_dai_per_token, sp.amount_tokens)
                for sp in controller.market.get_sell_positions_by_loan(
                    fetched_loan
                )
            )
        except StatisticsError:
            value_atto_dai = None

    else:  # loan_state.phase == LoanPhase.FINALIZED
        value_atto_dai = loan_state.redemption_value_atto_dai_per_token

    return value_atto_dai

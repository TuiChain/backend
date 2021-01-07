import tuichain_ethereum as tui
import web3


def init():
    """
    Get the Blockchain controller
    """

    return tui.Controller(
        provider=web3.HTTPProvider(os.environ["ETHEREUM_PROVIDER"]),
        master_account_private_key=tui.PrivateKey(
            bytes.fromhex(os.environ["MASTER_ACCOUNT_PRIVATE_KEY"])
        ),
        contract_address=tui.Address(os.environ["CONTROLLER_ADDRESS"]),
    )

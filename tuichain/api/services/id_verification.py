import stripe


def create_verification_intent(return_url, refresh_url, id_number):

    stripe.api_key = "sk_test_51HuGjSEXQQPxxsgPzqENPS8d8oDv3aJOGDPETgSOvLjVeB92uyDTKFcO20mFvHEHqhIObyANxPTZlabKOS2s4tk1009xlf5AxD"
    stripe.api_version = "2020-08-27; identity_beta=v3"

    response = stripe.stripe_object.StripeObject().request(
        "post",
        "/v1/identity/verification_intents",
        {
            "return_url": return_url,  # Path to where we want user to end up after ID verification
            "refresh_url": refresh_url,  # Path to where user will receive new link if it expires or it's consumed
            "requested_verifications": ["identity_document", "selfie"],
            "metadata": {  # Meta_data might help us connect an ID verification ID to a specific user
                "id_number": id_number,
            },
        },
    )

    return response

import streamlit as st
import stripe
import urllib.parse
import os

testing_mode = os.environ.get("TESTING_MODE", False)
payment_provider = os.environ.get("PAYMENT_PROVIDER", "stripe")
stripe_api_key_test = os.environ.get("stripe_api_key_test")
stripe_api_key = os.environ.get("stripe_api_key")
stripe_link = os.environ.get("stripe_link")
stripe_link_test = os.environ.get("stripe_link_test")  
client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")
redirect_url_test = os.environ.get("redirect_url_test")
redirect_url = os.environ.get("redirect_url")
bmac_api_key = os.environ.get("bmac_api_key")
bmac_link = os.environ.get("bmac_link")



def get_api_key() -> str:
    testing_mode = os.environ.get("TESTING_MODE", False)
    return (
        os.environ.get("stripe_api_key_test")
        if testing_mode
        else os.environ.get("stripe_api_key")
    )


def redirect_button(
    text: str,
    customer_email: str,
    color="#FD504D",
    payment_provider: str = "stripe",
):
    testing_mode = os.environ.get("testing_mode", False)
    encoded_email = urllib.parse.quote(customer_email)
    if payment_provider == "stripe":
        stripe.api_key = get_api_key()
        stripe_link = (
            stripe_link_test
            if testing_mode
            else stripe_link
        )
        button_url = f"{stripe_link}?prefilled_email={encoded_email}"
    elif payment_provider == "bmac":
        button_url = f"{bmac_link}"
    else:
        raise ValueError("payment_provider must be 'stripe' or 'bmac'")

    st.sidebar.markdown(
        f"""
    <a href="{button_url}" target="_blank">
        <div style="
            display: inline-block;
            padding: 0.5em 1em;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 3px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """,
        unsafe_allow_html=True,
    )


def is_active_subscriber(email: str) -> bool:
    stripe.api_key = get_api_key()
    customers = stripe.Customer.list(email=email)
    try:
        customer = customers.data[0]
    except IndexError:
        return False

    subscriptions = stripe.Subscription.list(customer=customer["id"])

    return len(subscriptions) > 0

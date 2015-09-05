"""
    Credentials to connect on Whatsapp Servers.
    (phone number, whatsapp key)

    To extract key use the yowsup-cli (using a python venv with yowsup installed):

    > yowsup-cli registration -C <CountryCode> -r sms -p <Phone Number with Country Code>
    ex.:
    yowsup-cli registration -C 55 -r sms -p 554899998888

    Then whatsapp will send a key via sms to the phone.
    Get that key then run:

    > yowsup-cli registration -C 55 -R <sms-key> -p 554898603087

    INFO:yowsup.common.http.warequest:{"status":"ok","login":"554898603087","pw":"njH+QGBqGxvbPP8YOFa+Wth5riM=","type":"existing","expiration":1472404969,"kind":"free","price":"US$0.99","cost":"0.99","currency":"USD","price_expiration":1444272405}

    status: ok
    kind: free
    > pw: njH+QGBqGxvbPP8YOFa+Wth5riM=
    price: US$0.99
    price_expiration: 1444272405
    currency: USD
    cost: 0.99
    > login: 554898603087
    type: existing
    expiration: 1472404969

    Now just get the login and pw, and replace bellow. :)


    -- NOVO CHIP --

"""
auth = ("554898627861", "j1M3Ieoox0FI6WRZNlsFCr7NJvg=")

# Path to download the media requests
media_storage_path = "/tmp/"

import logging

log_format = '_%(filename)s_\t[%(levelname)s][%(asctime)-15s] %(message)s'
logging_level = logging.INFO

# Try login with code
    This function is used to login to Telegram using the code sent to the user's phone number.
    - It asks for the OTP max_tries times before giving up.

    - If the OTP is correct it returns the client object.

    - If the OTP is incorrect it returns None.
## Parameters
    - client : (TelegramClient) Client object to be used for login.

    - max_tries : (int) Maximum number of tries to enter OTP.
    
    - tries : (int) Number of tries to enter OTP
## Returns
    None - If the OTP is incorrect.

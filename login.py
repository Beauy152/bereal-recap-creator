import requests
from json import loads
from consts import PING_URL,CODE_URL,VERIFY_URL

def bereal_api_ping(base_url:str) -> bool:
    """Send a ping to the configured api endpoint (default "localhost:3000")"""
    res = requests.get(url=base_url+PING_URL)

    if not res.status_code == 200:
        raise ConnectionError(f"Unable to ping BeReal Api at {base_url}.")
    
    return res.status_code == 200

def bereal_api_send_code(base_url:str,phone_num:str) -> str:
    """Given a phone number, send a verification code. returns the otpSession"""
    res = requests.post(url=base_url+CODE_URL,
                        data={"phone":phone_num})
    
    if not res.status_code == 201:
        #TODO: Remove
        print(res.content)
        raise ConnectionError(f"Failed to send OTP code to {phone_num}.")
    
    body = loads(res.content)


    if (otpSesison := body.get('data').get('otpSession')) is None:
        raise ValueError('Unable to get OTPSession from response.')

    return otpSesison

def bereal_api_validate_code(base_url:str,otpSession:str) -> str:
    def validate_otp(code:str) -> bool:
        if not code.isnumeric():
            print("OTP must be numeric.")
            return False

        if len(code) != 6:
            print("OTP must be 6 numbers long.")
            return False
        
        return True

    token = None
    while token is None:
        otpCode = input("enter OTP Code: ")
       
        if validate_otp(otpCode):
            res = requests.post(url=base_url+VERIFY_URL,
                                data={
                                    "code":otpCode,
                                    "otpSession":otpSession
                                })
            body = loads(res.content)

            if res.status_code == 201:
                token = (body.get('data')).get('token')
                break
            elif res.status_code == 400:
                raise ValueError("Unable to verify OTP.")
            else:
                raise ConnectionError("BeReal API error.")

    return token



def handle_login(base_url:str,phone_num:str) -> str:
    """Validate OTP code & return user auth token."""
    bereal_api_ping(base_url)

    otpSession = bereal_api_send_code(base_url,phone_num)
    userToken  = bereal_api_validate_code(base_url,otpSession)

    if userToken is None:
        raise ValueError('User Token is None.')

    return userToken


    
    

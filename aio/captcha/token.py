import time

class CaptchaToken(object):
    def __init__(self, captcha_token, validity=120):
        self.token = captcha_token
        self.creation_time = time.time()
        self.validity = validity

    def is_valid(self):
        return (time.time() - self.creation_time) < self.validity

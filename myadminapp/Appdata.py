otp_url = ""

requests.get(
    "http://quicksms.highspeedsms.com/sendsms/sendsms.php?username=BREbonrix&password=sales55&type=TEXT&sender=BONRIX&mobile=" + str(
        phone_no) + "&message=Your%20OTP%20for%20login%20verification%20is%20:=%20" + str(random_otp) + "")

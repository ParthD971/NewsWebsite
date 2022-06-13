
def user_login_success(email):
    return f"You are now logged in as {email}."


WRONG_CREDENTIALS = "Invalid username or password."
INVALID_INFORMATION = "Unsuccessful registration due to invalid information."
ALREADY_USER_EXISTS = "Email is Already registered, Please verify email."
VERIFY_EMAIL = "Check Email for verification."
EMAIL_CONFIRMATION = "Thank you for your email confirmation. Now you can login your account."
INVALID_VERIFICATION_LINK = "Activation link is invalid!"
PASSWORD_RESET_INSTRUCTION = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."

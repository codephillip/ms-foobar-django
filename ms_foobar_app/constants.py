WELCOME_MESSAGE = "Dear {}, Welcome to the Foobar registration system. Please continue by utilizing any of our services."
TOKEN_MESSAGE = "Your Foobar One Time Password (OTP) code is: {}. Do not share it with anyone."

EMAIL_WELCOME_MESSAGE = "Dear {},\n\nWelcome to Foobar registration system.\n\nPlease continue by utilizing any of our services.\n\n\nRegards.\nFoobar TEAM"
EMAIL_WELCOME_SUBJECT = "Welcome to the Foobar registration system"

EMAIL_TOKEN_SUBJECT = "Foobar verification code"
EMAIL_TOKEN_MESSAGE = "Dear {},\n\nYour One Time Password (OTP) code to log into the Foobar system is {}\n\nPlease don't share this code with any one.\n\n\nRegards.\nFoobar TEAM"

# error messages
INVALID_CODE = "Invalid code. Please try logging in again"
INVALID_CREDENTIALS = "Invalid credentials. Wrong username or password"
PHONE_NUMBER_REGEX = "^\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$"
QueueGroupName = "auth-service"


class EventSubjects:
    UserScheduleCreated = "userschedule:created"
    SmsNotificationCreated = "smsnotification:created"
    UserInfoAvailed = "user:availed"
    PaymentCreated = "payment:created"

class Messages():
    def email_not_allow_because_interval(timestamp)->str:
        import time

        date = time.localtime(timestamp)

        return f"You send email recently, send other at {date.tm_hour}:{date.tm_min}"

    def email_now_allow_because_amount(timestamp)->str:
        import time

        date = time.localtime(timestamp)

        return f"You send many emails once. Plase, wait until {date.tm_hour}:{date.tm_min}"

    def email_internal_error()->str:
        return "Something goes wrong"

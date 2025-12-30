from django.core import mail


def assert_emails_in_mailbox(count: int):
    assert len(mail.outbox) == count, f"There is {len(mail.outbox)} e-mails in mailbox, expected {count}"


def assert_email(email, **kwargs):
    for key, value in kwargs.items():
        assert getattr(email, key) == value, (
            f"Email does not match criteria,  expected {key} to be {value} but it is {getattr(email, key)}"
        )


def _is_email_matching_criteria(email, **kwargs):
    for key, value in kwargs.items():
        if getattr(email, key) != value:
            return False
    return True


def assert_email_exists(**kwargs):
    for email in mail.outbox:
        print(email.body)
        if _is_email_matching_criteria(email, **kwargs):
            return
    raise AssertionError("Email matching criteria was not sent")

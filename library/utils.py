from django.core.mail import send_mail
def send_status_email( borrow_request):

    subject = f"Book Request {borrow_request.status.title()}"

    message = (
        f"Hello {borrow_request.user.username},\n\n"
        f"Your request for "
        f"'{borrow_request.book.title}' "
        f"has been "
        f"{borrow_request.status.lower()}."
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[borrow_request.user.email],
        fail_silently=False,
    )
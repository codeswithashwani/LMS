from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .models import BorrowRequest

from django.core.mail import send_mail

@receiver(pre_save, sender=BorrowRequest)
def update_book_copies(sender, instance, **kwargs):
    if not instance.pk:
        return

    previous = BorrowRequest.objects.get(pk=instance.pk)
    book = instance.book

    if (
        previous.status != BorrowRequest.Status.APPROVED
        and instance.status == BorrowRequest.Status.APPROVED
    ):

        if book.available_copies > 0:
            book.available_copies -= 1
            book.save()

    elif (
        previous.status != BorrowRequest.Status.RETURNED
        and instance.status == BorrowRequest.Status.RETURNED
    ):

        book.available_copies += 1

        book.save()





@receiver(post_save, sender=BorrowRequest)
def send_borrow_status_email(sender,instance,created,**kwargs):

    if created:
        return

    if instance.status == "APPROVED":
        send_mail(
            subject="Book Request Approved",

            message=(
                f"Hello {instance.user.username},\n\n"
                f"Your request for "
                f"'{instance.book.title}' "
                f"has been approved."
            ),

            from_email=None,

            recipient_list=[instance.user.email],

            fail_silently=False,
        )

    elif instance.status == "REJECTED":

        send_mail(
            subject="Book Request Rejected",

            message=(
                f"Hello {instance.user.username},\n\n"
                f"Your request for "
                f"'{instance.book.title}' "
                f"has been rejected."
            ),

            from_email=None,

            recipient_list=[instance.user.email],

            fail_silently=False,
        )
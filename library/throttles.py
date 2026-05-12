from rest_framework.throttling import UserRateThrottle


class BorrowRateThrottle(UserRateThrottle):

    scope = "borrow"
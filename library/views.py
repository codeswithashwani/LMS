from library.permissions import IsOwnerOrReadOnly
from library.throttles import BorrowRateThrottle
from library.serializers import BookReviewSerializer
from library.models import BorrowRequest
from rest_framework.response import Response
from library.serializers import BorrowRequestSerializer
from library.serializers import BorrowCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin,ListModelMixin
from library.serializers import GenreSerializer
from library.models import Genre
from library.serializers import AuthorSerializer
from library.models import Author
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.decorators import action
from .models import Book
from .serializers import BookSerializer,BookCreateUpdateSerializer
from .permissions import IsLibrarian
from rest_framework import status
from django.utils import timezone
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db import transaction
from .utils import send_status_email

import logging

logger = logging.getLogger(__name__)

class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related("author").prefetch_related("genres")
    permission_classes = [IsLibrarian]
    filterset_fields = ["author", "genres"]
    search_fields = ["title"]
    ordering_fields = ["title","available_copies"]

    def get_serializer_class(self):

        if self.action in ["create","update","partial_update"]:
            return BookCreateUpdateSerializer

        return BookSerializer

class AuthorListCreateAPIView(ListCreateAPIView):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarian]


class GenreListCreateAPIView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsLibrarian]


class BorrowRequestViewSet( CreateModelMixin,ListModelMixin, GenericViewSet):

    queryset = BorrowRequest.objects.select_related( "user",  "book")
    permission_classes = [IsAuthenticated]
    # throttle_classes = [BorrowRateThrottle]

    def get_throttles(self):
        if self.action == "create":
            return [BorrowRateThrottle()]

        return []

    def get_serializer_class(self):

        if self.action == "create":
            return BorrowCreateSerializer

        return BorrowRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "LIBRARIAN":
            return self.queryset

        return self.queryset.filter(user=user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch"])
    def approve(self, request, pk=None):

        if request.user.role != "LIBRARIAN":
            return Response(
                {
                    "error": "Only librarians can approve"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        # borrow_request = self.get_object()
        with transaction.atomic():
            borrow_request = BorrowRequest.objects.select_for_update().get(pk=pk)
            if borrow_request.status != BorrowRequest.Status.PENDING:

                return Response(
                    {
                        "error": "Only pending requests can be approved"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            borrow_request.status = BorrowRequest.Status.APPROVED
            borrow_request.approved_at = timezone.now()

            borrow_request.save()
            try :
                send_status_email( borrow_request)
            except Exception as e:
                logger.error(
                    f"Email sending failed: {str(e)}"
                )

        return Response(
            {
                "message": "Borrow request approved"
            }
        )

    @action(detail=True, methods=["patch"])
    def reject(self, request, pk=None):

        if request.user.role != "LIBRARIAN":
            return Response(
                {
                    "error": "Only librarians can reject"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        borrow_request = self.get_object()

        if borrow_request.status != "PENDING":
            return Response(
                {
                    "error": "Only pending requests can be rejected"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        borrow_request.status = "REJECTED"
        borrow_request.save()
        try :
            send_status_email(borrow_request)
        except Exception as e:
                logger.error(
                    f"Email sending failed: {str(e)}"
                )
        return Response(
            {
                "message": "Borrow request rejected"
            }
        )

    @action(detail=True, methods=["patch"])
    def return_book(self, request, pk=None):
        borrow_request = self.get_object()
        if borrow_request.status != "APPROVED":
            return Response(
                {
                    "error": "Only approved books can be returned"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        borrow_request.status = "RETURNED"
        borrow_request.returned_at = timezone.now()
        borrow_request.save()
        return Response(
            {
                "message": "Book returned successfully"
            }
        )


class ReviewAPIView(APIView):
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        reviews = book.reviews.select_related("user")
        serializer = BookReviewSerializer( reviews,many=True)
        return Response(serializer.data)

    def post(self, request, pk):

        book = get_object_or_404(Book, pk=pk)
        serializer = BookReviewSerializer(data=request.data )
        serializer.is_valid(raise_exception=True)
        serializer.save( user=request.user, book=book )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
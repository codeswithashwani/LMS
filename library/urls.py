from library.views import GenreListCreateAPIView
from library.views import AuthorListCreateAPIView
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import BookViewSet,ReviewAPIView,BorrowRequestViewSet


router = DefaultRouter()

router.register("books",BookViewSet,basename="books")
router.register( "borrow",BorrowRequestViewSet, basename="borrow")

urlpatterns = [
    path("authors/", AuthorListCreateAPIView.as_view(), name="authors"),
    path("genres/", GenreListCreateAPIView.as_view(),  name="genres" ),
    path("books/<int:pk>/reviews/", ReviewAPIView.as_view(), name="book-reviews")
]

urlpatterns += router.urls 

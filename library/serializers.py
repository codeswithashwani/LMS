from rest_framework import serializers

from .models import (
    Author,
    Genre,
    Book,
    BorrowRequest,
    BookReview,
)


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = "__all__"

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(read_only=True)

    genres = GenreSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Book
        fields = "__all__"

class BookCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"


class BorrowRequestSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True )
    book = serializers.StringRelatedField( read_only=True)

    class Meta:
        model = BorrowRequest
        fields = "__all__"

# class BookReviewSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = BookReview
#         fields = "__all__"

class BookReviewSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    rating = serializers.IntegerField( min_value=1,max_value=5)

    class Meta:
        model = BookReview
        fields = "__all__"


class BorrowCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = BorrowRequest
        fields = ["id", "book"]

    def validate_book(self, value):

        if value.available_copies <= 0:
            raise serializers.ValidationError(
                "Book is not available"
            )

        return value
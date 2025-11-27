from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.http import Http404
from django.db import transaction
from django.contrib.auth import get_user_model


from post_management.models import NewsPost, Tag
from .serializers import NewsPostSerializer, TagSerializer
from .utils import success_response, error_response, verify_signature

User = get_user_model()


class NewsPostCreateView(APIView):
    """
    POST /api/news/
    Create a new NewsPost
    """

    def post(self, request):
        try:
            # ok, error = verify_signature(request)
            # if not ok:
            #     return Response({"error": error}, status=status.HTTP_401_UNAUTHORIZED)
            serializer = NewsPostSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            with transaction.atomic():
                news_post = serializer.save()

            return Response(
                success_response(NewsPostSerializer(news_post).data),
                status=status.HTTP_201_CREATED,
            )

        except Http404 as e:
            return Response(
                error_response(str(e)),
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            return Response(
                error_response(e.detail),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                error_response(str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PortalUserCheckAPIView(APIView):
    """
    GET /api/portal-users/check-username/?username=<username>
    """

    def get(self, request):
        username = request.query_params.get("username")
        if not username:
            return Response(error_response("Username is required"), status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": getattr(user, "full_name", None),
                "status": "active" if user.is_active else "inactive"
            }
            return Response(success_response(user_data, "User found"), status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(error_response("User not found"), status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(error_response(str(e)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TagListAPIView(APIView):
    """
    GET /api/tags/
    Returns a list of all active tags.
    """
    def get(self, request):
        try:
            tags = Tag.objects.all().order_by('name')
            print('tags', tags)
            serializer = TagSerializer(tags, many=True)
            return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

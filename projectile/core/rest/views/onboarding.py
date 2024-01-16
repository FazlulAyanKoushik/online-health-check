import logging

from django.http import Http404

from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from common.tokens import decode_jwt_for_user

from ...models import User

logger = logging.getLogger(__name__)


class GlobalUserActivation(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        try:
            token = request.data["token"]
            if token:
                payload = decode_jwt_for_user(token)
                if "slug" in payload:
                    user = get_object_or_404(
                        User, slug=payload["slug"], is_active=False
                    )
                    user.activate()
                    logger.debug(f"Activated user: {user.email}")
                    return Response(True)
        except KeyError:
            pass
        raise Http404

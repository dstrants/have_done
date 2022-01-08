import base64
import hmac
import hashlib
import logging
from typing import Optional

from django.conf import settings
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from sync.integrations.todoist.validators import TodoistWebhook as TodoistWebhookModel


logger = logging.getLogger(__name__)


class IsTodoistRequest(permissions.BasePermission):
    """
    Checks that the calls are orginated from Todoist
    """

    @property
    def todoist_secret(self) -> Optional[bytes]:
        return settings.SOCIAL_AUTH_TODOIST_SECRET.encode() or None

    def has_permission(self, request, _) -> bool:
        calculated_hmac = base64.b64encode(
            hmac.new(self.todoist_secret, msg=request.body, digestmod=hashlib.sha256).digest()
            ).decode()
        incoming_hmac = request.headers.get('X-Todoist-Hmac-SHA256')

        return calculated_hmac == incoming_hmac


class TodoistWebhook(APIView):
    """
    Creates new todoist item
    """

    permission_classes = [IsTodoistRequest]

    @staticmethod
    def post(request, format=None):
        if request.data:
            logger.info("New webhook from todoist with ID: %s", request.headers['X-Todoist-Delivery-ID'])
            webhook = TodoistWebhookModel(**request.data)
            webhook.event_data.save_to_mongo()
            webhook.event_data.save()
            return Response({'status': 'Item saved'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'No request data found'}, status=status.HTTP_406_NOT_ACCEPTABLE)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from myapp.models import Notification

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from myapp.models import Notification

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, is_read=False).order_by('-created_at')

    # Manually construct the response data
    notifications_data = []
    for notification in notifications:
        notifications_data.append({
            'id': notification.id,
            'notification_type': notification.notification_type,
            'message': notification.message,
            'created_at': notification.created_at.isoformat(),
            'is_read': notification.is_read,
        })

    return Response(notifications_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notifications_as_read(request):
    user = request.user
    notification_ids = request.data.get('notification_ids', [])
    Notification.objects.filter(user=user, id__in=notification_ids).update(is_read=True)
    return Response({'status': 'success'})
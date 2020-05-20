from django.core.management.base import BaseCommand
from django.conf import settings

from src.dj_asana.models import AsanaUser, asana_client


class Command(BaseCommand):
    help = 'Loads users from a given Asana workspace'

    def handle(self, *args, **options):
        users = asana_client.users.get_users(workspace=settings.ASANA_WORKSPACE_GID)
        for user in users:
            a_user = AsanaUser.objects.filter(gid=user['gid']).first()
            if not a_user:
                AsanaUser.objects.create(
                    gid=user['gid'],
                    name=user['name']
                )
            elif a_user.name != user['name']:
                a_user.name = user['name']
                a_user.save()

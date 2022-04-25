from django.dispatch import receiver
from django.db.models.signals import post_save
from permissions.models import Permission, PermissionTargetKey

from users.models import UserProfile

@receiver(post_save, sender=UserProfile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        defaultUserPermissions = Permission.getDefaultPermissions(instance.role)
        createdPermissions = Permission.createDefaultPermissions(instance.user, defaultUserPermissions)
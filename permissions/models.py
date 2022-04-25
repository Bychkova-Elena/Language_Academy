from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from education.models import Course
from users.models import User, UserProfile, UserRole


class PermissionKey(models.TextChoices):
    READ_USER_PROFILE_SPECIFIC_USERS = 'READ_USER_PROFILE_SPECIFIC_USERS'
    READ_USER_PROFILE_ANY_USERS_SPECIFIC_COURSES = 'READ_USER_PROFILE_ANY_USERS_SPECIFIC_COURSES'
    UPDATE_USER_PROFILE_SPECIFIC_USERS = 'UPDATE_USER_PROFILE_SPECIFIC_USERS'
    DELETE_USER_PROFILE_SPECIFIC_USERS = 'DELETE_USER_PROFILE_SPECIFIC_USERS'

    CREATE_HOMEWORK_SPECIFIC_COURSES = 'CREATE_HOMEWORK_SPECIFIC_COURSES'
    READ_ASSIGNED_HOMEWORK_SPECIFIC_USERS = 'READ_ASSIGNED_HOMEWORK_SPECIFIC_USERS'
    READ_CREATED_HOMEWORK_SPECIFIC_USERS = 'READ_CREATED_HOMEWORK_SPECIFIC_USERS'
    UPDATE_HOMEWORK_SPECIFIC_COURSES = 'UPDATE_HOMEWORK_SPECIFIC_COURSES'
    UPDATE_HOMEWORK_DONE_STATUS_SPECIFIC_USERS = 'UPDATE_HOMEWORK_DONE_STATUS_SPECIFIC_USERS'
    DELETE_HOMEWORK_SPECIFIC_COURSES = 'DELETE_HOMEWORK_SPECIFIC_COURSES'

    CREATE_COURSES = 'CREATE_COURSES'
    READ_SPECIFIC_COURSES = 'READ_SPECIFIC_COURSES'
    UPDATE_SPECIFIC_COURSES = 'UPDATE_SPECIFIC_COURSES'
    UPDATE_SPECIFIC_COURSES_MEMBERS = 'UPDATE_SPECIFIC_COURSES_MEMBERS'
    DELETE_SPECIFIC_COURSES = 'DELETE_SPECIFIC_COURSES'

class PermissionTargetKey(models.TextChoices):
    OWN_ID = 'OWN_ID'
    STUDY_COURSES_IDS = 'STUDY_COURSES_IDS'
    TEACH_COURSES_IDS = 'TEACH_COURSES_IDS'

    @staticmethod
    def GetTargetsIds(user, key):
        match key:
            case PermissionTargetKey.OWN_ID:
                return [user.id]

            case PermissionTargetKey.STUDY_COURSES_IDS:
                return list(
                    map(
                        lambda course: course.id,
                        Course.objects.filter(student__user=user)
                    )
                )

            case PermissionTargetKey.TEACH_COURSES_IDS:
                return list(
                    map(
                        lambda course: course.id,
                        Course.objects.filter(teacher__user=user)
                    )
                )

        return []


class Permission(models.Model):
    class Meta:
        verbose_name = 'Права'
        verbose_name_plural = 'Права'

    DEFAULT_USER_PERMISSIONS = [
        {
            'key': PermissionKey.READ_USER_PROFILE_SPECIFIC_USERS,
            'targetUserIdKey': PermissionTargetKey.OWN_ID
        },
        {
            'key': PermissionKey.UPDATE_USER_PROFILE_SPECIFIC_USERS,
            'targetUserIdKey': PermissionTargetKey.OWN_ID
        },
        {
            'key': PermissionKey.DELETE_USER_PROFILE_SPECIFIC_USERS,
            'targetUserIdKey': PermissionTargetKey.OWN_ID
        },
    ]

    DEFAULT_STUDENT_PERMISSIONS = [
        {
            'key': PermissionKey.READ_USER_PROFILE_ANY_USERS_SPECIFIC_COURSES,
            'targetCourseIdKey': PermissionTargetKey.STUDY_COURSES_IDS
        },

        {
            'key': PermissionKey.READ_ASSIGNED_HOMEWORK_SPECIFIC_USERS,
            'targetUserIdKey': PermissionTargetKey.OWN_ID},
        {
            'key': PermissionKey.UPDATE_HOMEWORK_DONE_STATUS_SPECIFIC_USERS,
            'targetUserIdKey': PermissionTargetKey.OWN_ID
        },

        {
            'key': PermissionKey.READ_SPECIFIC_COURSES,
            'targetCourseIdKey': PermissionTargetKey.STUDY_COURSES_IDS
        },
    ]

    DEFAULT_TEACHER_PERMISSIONS = [
        {
            'key': PermissionKey.READ_USER_PROFILE_ANY_USERS_SPECIFIC_COURSES,
            'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS
        },

        {
            'key': PermissionKey.CREATE_HOMEWORK_SPECIFIC_COURSES,
            'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS
        },
        {
            'key': PermissionKey.READ_CREATED_HOMEWORK_SPECIFIC_USERS,
            'targetUserIdKey': PermissionTargetKey.OWN_ID
        },
        {
            'key': PermissionKey.UPDATE_HOMEWORK_SPECIFIC_COURSES,
            'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS
        },
        {
            'key': PermissionKey.DELETE_HOMEWORK_SPECIFIC_COURSES,
            'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS
        },

        {
            'key': PermissionKey.CREATE_COURSES},
        {
            'key': PermissionKey.READ_SPECIFIC_COURSES,
            'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS
        },
        {
            'key': PermissionKey.UPDATE_SPECIFIC_COURSES,
            'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS
        },
        {
            'key': PermissionKey.UPDATE_SPECIFIC_COURSES_MEMBERS,
            'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS
        },
        {
            'key': PermissionKey.DELETE_SPECIFIC_COURSES,
            'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS
        },
    ]

    user = models.ForeignKey(
        verbose_name="Пользователь",
        to=User, related_name="owner",
        on_delete=models.CASCADE
    )
    key = models.CharField(
        verbose_name="Ключ",
        choices=PermissionKey.choices,
        max_length=255
    )

    targetUserId = models.ForeignKey(
        verbose_name="User ID цели доступа",
        to=User,
        related_name="target",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    targetUserIdKey = models.CharField(
        verbose_name="Ключ user ID цели доступа",
        choices=PermissionTargetKey.choices,
        max_length=255,
        blank=True,
        null=True
    )

    targetCourseId = models.ForeignKey(
        verbose_name="Course ID цели доступа",
        to=Course,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    targetCourseIdKey = models.CharField(
        verbose_name="Ключ course ID цели доступа",
        choices=PermissionTargetKey.choices,
        max_length=255,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.user.username)

    @staticmethod
    @receiver(post_save, sender=UserProfile)
    def CreatePermissions(instance, created, **kwargs):
        if created:
            defaultUserPermissions = Permission.GetDefaultPermissions(
                role=instance.role
            )
            Permission.CreateDefaultPermissions(
                user=instance.user,
                defaultPermissions=defaultUserPermissions
            )

    @staticmethod
    def GetDefaultPermissions(role):
        defaultRoles = []
        defaultRoles.extend(Permission.DEFAULT_USER_PERMISSIONS)

        if role == UserRole.STUDENT:
            defaultRoles.extend(Permission.DEFAULT_STUDENT_PERMISSIONS)

        if role == UserRole.TEACHER:
            defaultRoles.extend(Permission.DEFAULT_TEACHER_PERMISSIONS)

        return defaultRoles

    @staticmethod
    def CreateDefaultPermissions(user, defaultPermissions):
        createdPermissions = []

        for defaultPermission in defaultPermissions:
            createdPermission = Permission.objects.create(
                user=user,
                key=defaultPermission['key'],
                targetUserId=defaultPermission.get('targetUserId', None),
                targetUserIdKey=defaultPermission.get('targetUserIdKey', None),
                targetCourseId=defaultPermission.get('targetCourseId', None),
                targetCourseIdKey=defaultPermission.get(
                    'targetCourseIdKey', None
                ),
            )

            createdPermissions.append(createdPermission)

        return createdPermissions

    @staticmethod
    def CanUserAccessByExistence(user, permissionKey):
        if Permission.objects.filter(user=user, key=permissionKey).exists():
            return True

        return False

    @staticmethod
    def CanUserAccessByUserId(user, permissionKey, targetUserId):
        if Permission.objects.filter(
            user=user,
            key=permissionKey,
            targetUserId=targetUserId
        ).exists():
            return True

        permissions = Permission.objects.filter(user=user, key=permissionKey)

        if not permissions.exists():
            return False

        availableUsersIds = []

        for permission in permissions:
            permissionTargetUserId = getattr(permission, 'targetUserId', None)
            permissionTargetUserIdKey = getattr(permission, 'targetUserIdKey', None)

            if permissionTargetUserId:
                availableUsersIds.append(permissionTargetUserId)

            if permissionTargetUserIdKey:
                availableUsersIds.extend(PermissionTargetKey.GetTargetsIds(
                    user=user, key=permissionTargetUserIdKey))

        if targetUserId in availableUsersIds:
            return True

        return False

    @staticmethod
    def CanUserAccessByCourseId(user, permissionKey, targetCourseId):
        if Permission.objects.filter(
            user=user,
            key=permissionKey,
            targetCourseId=targetCourseId
        ).exists():
            return True

        permissions = Permission.objects.filter(user=user, key=permissionKey)

        if not permissions.exists():
            return False

        availableCoursesIds = []

        for permission in permissions:
            permissionTargetCourseId = getattr(permission, 'targetCourseId', None)
            permissionTargetCourseIdKey = getattr(permission, 'targetCourseIdKey', None)

            if permissionTargetCourseId:
                availableCoursesIds.append(permissionTargetCourseId)

            if permissionTargetCourseIdKey:
                availableCoursesIds.extend(PermissionTargetKey.GetTargetsIds(user=user, key=permissionTargetCourseIdKey))

        if targetCourseId in availableCoursesIds:
            return True

        return False

    # User Profile Access

    @staticmethod
    def CanReadUserProfileSpecificUsers(user, targetUserId):
        return Permission.CanUserAccessByUserId(
            user=user,
            permissionKey=PermissionKey.READ_USER_PROFILE_SPECIFIC_USERS,
            targetUserId=targetUserId
        )

    @staticmethod
    def CanReadUserProfileAnyUsersSpecificCourses(user, targetCourseId):
        return Permission.CanUserAccessByCourseId(
            user=user,
            permissionKey=PermissionKey.READ_USER_PROFILE_ANY_USERS_SPECIFIC_COURSES,
            targetCourseId=targetCourseId
        )

    @staticmethod
    def CanUpdateUserProfileSpecificUsers(user, targetUserId):
        return Permission.CanUserAccessByUserId(
            user=user,
            permissionKey=PermissionKey.UPDATE_USER_PROFILE_SPECIFIC_USERS,
            targetUserId=targetUserId
        )

    @staticmethod
    def CanDeleteUserProfileSpecificUsers(user, targetUserId):
        return Permission.CanUserAccessByUserId(
            user=user,
            permissionKey=PermissionKey.DELETE_USER_PROFILE_SPECIFIC_USERS,
            targetUserId=targetUserId
        )

    # Homework Access

    @staticmethod
    def CanCreateHomeworkSpecificCourses(user, targetCourseId):
        return Permission.CanUserAccessByCourseId(
            user=user,
            permissionKey=PermissionKey.CREATE_HOMEWORK_SPECIFIC_COURSES,
            targetCourseId=targetCourseId
        )

    @staticmethod
    def CanReadAssignedHomeworkSpecificUsers(user, targetUserId):
        return Permission.CanUserAccessByUserId(
            user=user,
            permissionKey=PermissionKey.READ_ASSIGNED_HOMEWORK_SPECIFIC_USERS,
            targetUserId=targetUserId
        )

    @staticmethod
    def CanReadCreatedHomeworkSpecificUsers(user, targetUserId):
        return Permission.CanUserAccessByUserId(
            user=user,
            permissionKey=PermissionKey.READ_CREATED_HOMEWORK_SPECIFIC_USERS,
            targetUserId=targetUserId
        )

    @staticmethod
    def CanUpdateHomeworkSpecificCourses(user, targetCourseId):
        return Permission.CanUserAccessByCourseId(
            user=user,
            permissionKey=PermissionKey.UPDATE_HOMEWORK_SPECIFIC_COURSES,
            targetCourseId=targetCourseId
        )

    @staticmethod
    def CanUpdateHomeworkDoneStatusSpecificUsers(user, targetUserId):
        return Permission.CanUserAccessByUserId(
            user=user,
            permissionKey=PermissionKey.UPDATE_HOMEWORK_DONE_STATUS_SPECIFIC_USERS,
            targetUserId=targetUserId
        )

    @staticmethod
    def CanDeleteHomeworkSpecificCourses(user, targetCourseId):
        return Permission.CanUserAccessByCourseId(
            user=user,
            permissionKey=PermissionKey.DELETE_HOMEWORK_SPECIFIC_COURSES,
            targetCourseId=targetCourseId
        )

    # Courses Access

    @staticmethod
    def CanCreateCourse(user):
        return Permission.CanUserAccessByExistence(user, PermissionKey.CREATE_COURSES)

    @staticmethod
    def CanReadSpecificCourses(user, targetCourseId):
        return Permission.CanUserAccessByCourseId(
            user=user,
            permissionKey=PermissionKey.READ_SPECIFIC_COURSES,
            targetCourseId=targetCourseId
        )

    @staticmethod
    def CanUpdateSpecificCourses(user, targetCourseId):
        return Permission.CanUserAccessByCourseId(
            user=user,
            permissionKey=PermissionKey.UPDATE_SPECIFIC_COURSES,
            targetCourseId=targetCourseId
        )

    @staticmethod
    def CanUpdateSpecificCoursesMembers(user, targetCourseId):
        return Permission.CanUserAccessByCourseId(
            user=user,
            permissionKey=PermissionKey.UPDATE_SPECIFIC_COURSES_MEMBERS,
            targetCourseId=targetCourseId
        )

    @staticmethod
    def CanDeleteSpecificCourses(user, targetCourseId):
        return Permission.CanUserAccessByCourseId(
            user=user,
            permissionKey=PermissionKey.DELETE_SPECIFIC_COURSES,
            targetCourseId=targetCourseId
        )

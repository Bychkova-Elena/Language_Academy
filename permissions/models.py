from django.db import models
from users.models import User, UserProfile
from education.models import Course

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

    def getTargetsIds(user, key):
        match key:
            case PermissionTargetKey.OWN_ID:
                return [user.id]

            case PermissionTargetKey.STUDY_COURSES_IDS:
                return list(map(lambda course: course.id, Course.objects.filter(student__user=user)))

            case PermissionTargetKey.TEACH_COURSES_IDS:
                return list(map(lambda course: course.id, Course.objects.filter(teacher__user=user)))

        return []

class Permission(models.Model):
    class Meta:
        verbose_name = 'Права'
        verbose_name_plural = 'Права'

    DEFAULT_USER_PERMISSIONS = [
        { 'key': PermissionKey.READ_USER_PROFILE_SPECIFIC_USERS, 'targetUserIdKey': PermissionTargetKey.OWN_ID },
        { 'key': PermissionKey.UPDATE_USER_PROFILE_SPECIFIC_USERS, 'targetUserIdKey': PermissionTargetKey.OWN_ID },
        { 'key': PermissionKey.DELETE_USER_PROFILE_SPECIFIC_USERS, 'targetUserIdKey': PermissionTargetKey.OWN_ID },
    ]

    DEFAULT_STUDENT_PERMISSIONS = [
        { 'key': PermissionKey.READ_USER_PROFILE_ANY_USERS_SPECIFIC_COURSES, 'targetCourseIdKey': PermissionTargetKey.STUDY_COURSES_IDS },

        { 'key': PermissionKey.READ_ASSIGNED_HOMEWORK_SPECIFIC_USERS, 'targetUserIdKey': PermissionTargetKey.OWN_ID },
        { 'key': PermissionKey.UPDATE_HOMEWORK_DONE_STATUS_SPECIFIC_USERS, 'targetUserIdKey': PermissionTargetKey.OWN_ID },
        
        { 'key': PermissionKey.READ_SPECIFIC_COURSES, 'targetCourseIdKey': PermissionTargetKey.STUDY_COURSES_IDS },
    ]

    DEFAULT_TEACHER_PERMISSIONS = [
        { 'key': PermissionKey.READ_USER_PROFILE_ANY_USERS_SPECIFIC_COURSES, 'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS },

        { 'key': PermissionKey.CREATE_HOMEWORK_SPECIFIC_COURSES, 'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS },
        { 'key': PermissionKey.READ_CREATED_HOMEWORK_SPECIFIC_USERS, 'targetUserIdKey': PermissionTargetKey.OWN_ID },
        { 'key': PermissionKey.UPDATE_HOMEWORK_SPECIFIC_COURSES, 'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS },
        { 'key': PermissionKey.DELETE_HOMEWORK_SPECIFIC_COURSES, 'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS },

        { 'key': PermissionKey.CREATE_COURSES },
        { 'key': PermissionKey.READ_SPECIFIC_COURSES, 'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS },
        { 'key': PermissionKey.UPDATE_SPECIFIC_COURSES, 'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS },
        { 'key': PermissionKey.UPDATE_SPECIFIC_COURSES_MEMBERS, 'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS },
        { 'key': PermissionKey.DELETE_SPECIFIC_COURSES, 'targetCourseIdKey': PermissionTargetKey.TEACH_COURSES_IDS },
    ]

    user = models.ForeignKey(verbose_name="Пользователь", to=User, related_name="owner", on_delete=models.CASCADE)
    permissionKey = models.CharField(verbose_name="Права", choices=PermissionKey.choices, max_length=255)

    targetUserId = models.ForeignKey(verbose_name="User ID цели доступа", to=User, related_name="target", on_delete=models.CASCADE, blank=True, null=True)
    targetUserIdKey = models.CharField(verbose_name="Ключ user ID цели доступа", choices=PermissionTargetKey.choices, max_length=255, blank=True, null=True)

    targetCourseId = models.ForeignKey(verbose_name="Course ID цели доступа", to=Course, on_delete=models.CASCADE, blank=True, null=True)
    targetCourseIdKey = models.CharField(verbose_name="Ключ course ID цели доступа", choices=PermissionTargetKey.choices, max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.user.username)

    def getDefaultPermissions(role):
        defaultRoles = []
        
        defaultRoles.extend(Permission.DEFAULT_USER_PERMISSIONS)

        if role == UserProfile.STUDENT:
            defaultRoles.extend(Permission.DEFAULT_STUDENT_PERMISSIONS)

        if role == UserProfile.TEACHER:
            defaultRoles.extend(Permission.DEFAULT_TEACHER_PERMISSIONS)

        return defaultRoles

    def createDefaultPermissions(user, defaultRoles):
        createdRoles = []

        for defaultRole in defaultRoles:
            createdRole = Permission.objects.create(
                user=user,
                permissionKey=defaultRole['key'],
                targetUserId=defaultRole.get('targetUserId', None),
                targetUserIdKey=defaultRole.get('targetUserIdKey', None),
                targetCourseId=defaultRole.get('targetCourseId', None),
                targetCourseIdKey=defaultRole.get('targetCourseIdKey', None),
            )

            createdRoles.append(createdRole)

        return createdRoles

    def canUserAccessByExistence(user, permissionKey):
        if Permission.objects.filter(user=user, permissionKey=permissionKey).exists():
            return True

        return False

    def canUserAccessByUserId(user, permissionKey, targetUserId):
        if Permission.objects.filter(user=user, permissionKey=permissionKey, targetUserId=targetUserId).exists():
            return True

        permissions = Permission.objects.filter(user=user, permissionKey=permissionKey)

        if not permissions.exists():
            return False

        availableUsersIds = []

        for permission in permissions:
            permissionTargetUserId = getattr(permission, 'targetUserId', None)
            permissionTargetUserIdKey = getattr(permission, 'targetUserIdKey', None)

            if permissionTargetUserId:
                availableUsersIds.append(permissionTargetUserId)

            if permissionTargetUserIdKey:
                availableUsersIds.extend(PermissionTargetKey.getTargetsIds(user=user, key=permissionTargetUserIdKey))

        if targetUserId in availableUsersIds:
            return True

        return False

    def canUserAccessByCourseId(user, permissionKey, targetCourseId):
        if Permission.objects.filter(user=user, permissionKey=permissionKey, targetCourseId=targetCourseId).exists():
            return True

        permissions = Permission.objects.filter(user=user, permissionKey=permissionKey)

        if not permissions.exists():
            return False

        availableCoursesIds = []

        for permission in permissions:
            permissionTargetCourseId = getattr(permission, 'targetCourseId', None)
            permissionTargetCourseIdKey = getattr(permission, 'targetCourseIdKey', None)

            if permissionTargetCourseId:
                availableCoursesIds.append(permissionTargetCourseId)

            if permissionTargetCourseIdKey:
                availableCoursesIds.extend(PermissionTargetKey.getTargetsIds(user=user, key=permissionTargetCourseIdKey))

        if targetCourseId in availableCoursesIds:
            return True

        return False

    # User Profile Access

    def canReadUserProfileSpecificUsers(user, targetUserId):
        return Permission.canUserAccessByUserId(user, PermissionKey.READ_USER_PROFILE_SPECIFIC_USERS, targetUserId)

    def canReadUserProfileAnyUsersSpecificCourses(user, targetCourseId):
        return Permission.canUserAccessByCourseId(user, PermissionKey.READ_USER_PROFILE_ANY_USERS_SPECIFIC_COURSES, targetCourseId)

    def canUpdateUserProfileSpecificUsers(user, targetUserId):
        return Permission.canUserAccessByUserId(user, PermissionKey.UPDATE_USER_PROFILE_SPECIFIC_USERS, targetUserId)

    def canDeleteUserProfileSpecificUsers(user, targetUserId):
        return Permission.canUserAccessByUserId(user, PermissionKey.DELETE_USER_PROFILE_SPECIFIC_USERS, targetUserId)

    # Homework Access

    def canCreateHomeworkSpecificCourses(user, targetCourseId):
        return Permission.canUserAccessByCourseId(user, PermissionKey.CREATE_HOMEWORK_SPECIFIC_COURSES, targetCourseId)

    def canReadAssignedHomeworkSpecificUsers(user, targetUserId):
        return Permission.canUserAccessByUserId(user, PermissionKey.READ_ASSIGNED_HOMEWORK_SPECIFIC_USERS, targetUserId)

    def canReadCreatedHomeworkSpecificUsers(user, targetUserId):
        return Permission.canUserAccessByUserId(user, PermissionKey.READ_CREATED_HOMEWORK_SPECIFIC_USERS, targetUserId)

    def canUpdateHomeworkSpecificCourses(user, targetCourseId):
        return Permission.canUserAccessByCourseId(user, PermissionKey.UPDATE_HOMEWORK_SPECIFIC_COURSES, targetCourseId)

    def canUpdateHomeworkDoneStatusSpecificUsers(user, targetUserId):
        return Permission.canUserAccessByUserId(user, PermissionKey.UPDATE_HOMEWORK_DONE_STATUS_SPECIFIC_USERS, targetUserId)

    def canDeleteHomeworkSpecificCourses(user, targetCourseId):
        return Permission.canUserAccessByCourseId(user, PermissionKey.DELETE_HOMEWORK_SPECIFIC_COURSES, targetCourseId)

    # Courses Access

    def canCreateCourse(user):
        return Permission.canUserAccessByExistence(user, PermissionKey.CREATE_COURSES)

    def canReadSpecificCourses(user, targetCourseId):
        return Permission.canUserAccessByCourseId(user, PermissionKey.READ_SPECIFIC_COURSES, targetCourseId)

    def canUpdateSpecificCourses(user, targetCourseId):
        return Permission.canUserAccessByCourseId(user, PermissionKey.UPDATE_SPECIFIC_COURSES, targetCourseId)

    def canUpdateSpecificCoursesMembers(user, targetCourseId):
        return Permission.canUserAccessByCourseId(user, PermissionKey.UPDATE_SPECIFIC_COURSES_MEMBERS, targetCourseId)

    def canDeleteSpecificCourses(user, targetCourseId):
        return Permission.canUserAccessByCourseId(user, PermissionKey.DELETE_SPECIFIC_COURSES, targetCourseId)
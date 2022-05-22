from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Teacher, UserProfile, UserRole
from permissions.models import Permission, PermissionTargetKey

from .models import Course, Homework, TimeTable
from .serializers import (TimeTableByCourseSerializer, CourseSerializer,
                AddCourseSerializer, UpdateCourseSerializer, HomeworkSerializer,
                AddHomeworkSerializer, UpdateHomeworkSerializer)


class CoursesView(APIView):
    @staticmethod
    def get(request):
        try:
            user = request.user
            userprofile = UserProfile.objects.get(user=user)

            params = request.query_params

            skip = params.get('skip', None)
            limit = params.get('limit', None)

            if userprofile.role == UserRole.STUDENT:
                accessableCoursesIds = PermissionTargetKey.GetTargetsIds(
                    user=user,
                    key=PermissionTargetKey.STUDY_COURSES_IDS
                )
            else:
                accessableCoursesIds = PermissionTargetKey.GetTargetsIds(
                    user=user,
                    key=PermissionTargetKey.TEACH_COURSES_IDS
                )

            courses = Course.objects.filter(pk__in=accessableCoursesIds)

            if skip:
                courses = courses[int(skip):]

            if limit:
                courses = courses[:int(limit)]

            courses = CourseSerializer(courses, many=True)

            return Response(
                data=courses.data,
                status=status.HTTP_200_OK
            )

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    def post(request):
        try:
            user = request.user

            if not Permission.CanCreateCourse(user=user):
                return Permission.GetNoPermissionResponse()

            teacher = Teacher.objects.get(user=user)

            data = {
                'name': request.data['name'],
                'level': request.data['levelId'],
                'language': request.data['languageId'],
                'teacher': teacher.id
            }

            course = AddCourseSerializer(data=data)

            if not course.is_valid():
                return Response(
                    data=course.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            course.save()

            return Response(
                data=course.data,
                status=status.HTTP_201_CREATED
            )

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CourseView(APIView):
    @staticmethod
    def put(request, courseId=None):
        try:
            user = request.user

            if (
                not Permission.CanUpdateSpecificCourses(user=user, targetCourseId=courseId) or
                not Permission.CanUpdateSpecificCoursesMembers(user=user, targetCourseId=courseId)
            ):
                return Permission.GetNoPermissionResponse()

            course = Course.objects.get(pk=courseId)

            updateData = {
                'name': request.data['name'],
                'level': request.data['levelId'],
                'language': request.data['languageId'],
                'students': request.data['students'],
                'teacher': course.teacher.id
            }

            updatedCourse = UpdateCourseSerializer(instance=course, data=updateData)

            if not updatedCourse.is_valid():
                return Response(
                    data=updatedCourse.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            updatedCourse.save()

            return Response(data=updatedCourse.data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    def delete(request, courseId=None):
        try:
            user = request.user

            if not Permission.CanDeleteSpecificCourses(user=user, targetCourseId=courseId):
                return Permission.GetNoPermissionResponse()

            course = Course.objects.get(pk=courseId)
            course.delete()

            return Response(status=status.HTTP_200_OK)

        except Exception as error:
            return Response(
                data={'error': str(error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HomeworksView(APIView):
    @staticmethod
    def get(request, courseId=None):
        '''Вывод дз группы'''
        try:
            user = request.user

            if (not Permission.CanReadAssignedHomeworkSpecificUsers(user=user, targetUserId=user.id)
                and not Permission.CanReadCreatedHomeworkSpecificUsers(
                    user=user, targetUserId=user.id)):
                return Permission.GetNoPermissionResponse()

            homeworks = Homework.objects.filter(course=courseId)

            homeworks = HomeworkSerializer(homeworks, many=True)

            return Response(homeworks.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def post(request, courseId=None):
        '''Добавление дз группы учителем'''
        try:
            user = request.user

            if not Permission.CanCreateHomeworkSpecificCourses(user=user, targetCourseId=courseId):
                return Permission.GetNoPermissionResponse()

            data = {
            'name': request.data['name'],
            'link': request.data['link'],
            'description': request.data['description'],
            'deadline': request.data['deadline'],
            'onEveryLesson': request.data['onEveryLesson'],
            'course': courseId,
            'draft': request.data['draft']
            }

            homework = AddHomeworkSerializer(data = data)
            if homework.is_valid():
                homework.save()
            return Response(homework.data, status=status.HTTP_201_CREATED)

        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HomeworkView(APIView):
    @staticmethod
    def put(request, courseId=None, homeworkId=None):
        '''Редактирование дз учителем'''
        try:
            user = request.user

            if not Permission.CanUpdateHomeworkSpecificCourses(user=user, targetCourseId=courseId):
                return Permission.GetNoPermissionResponse()

            homework = Homework.objects.get(pk=homeworkId)
            homework = UpdateHomeworkSerializer(instance=homework, data=request.data)
            if homework.is_valid():
                homework.save()
            return Response(homework.data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def delete(request, courseId=None, homeworkId=None):
        '''Удаление дз учителем'''
        try:
            user = request.user
            if not Permission.CanDeleteHomeworkSpecificCourses(user=user, targetCourseId=courseId):
                return Permission.GetNoPermissionResponse()

            homework = Homework.objects.get(pk=homeworkId)
            homework.delete()
            return Response(status=status.HTTP_200_OK)

        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetTimeTableView(APIView):
    @staticmethod
    def get(request, courseId):
        '''Вывод расписания группы'''
        try:

            timetable = TimeTable.objects.filter(course=courseId)

            serializer = TimeTableByCourseSerializer(timetable, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

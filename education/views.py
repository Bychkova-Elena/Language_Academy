from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Teacher, UserProfile
from .permissions import TeachersOnly
from .models import Course, Homework, TimeTable
from .serializers import (TimeTableByCourseSerializer, CourseSerializer,
                AddCourseSerializer, UpdateCourseSerializer, HomeworkSerializer,
                AddHomeworkSerializer, UpdateHomeworkSerializer)

class GetCourseView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request):
        '''Вывод групп'''

        try:

            user = self.request.user
            userprofile = UserProfile.objects.get(user=user)
            params = self.request.query_params

            limit = params.get('limit', None)
            skip = params.get('skip', None)

            if userprofile.role == "STUDENT":
                courses = Course.objects.filter(student__user=user)
            else:
                courses = Course.objects.filter(teacher__user=user)

            if skip:
                courses = courses[int(skip):]

            if limit:
                courses = courses[:int(limit)]

            courses = CourseSerializer(courses, many=True)

            return Response(courses.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        '''Добавление группы учителем'''

        try:

            user = self.request.user
            teacher = Teacher.objects.get(user=user)
            data = {
            'name': request.data['name'],
            'language': request.data['language'],
            'level': request.data['level'],
            'price': request.data['price'],
            'teacher': teacher.id
            }

            course = AddCourseSerializer(data = data)
            if course.is_valid():
                course.save()
            return Response(course.data, status=status.HTTP_201_CREATED)

        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateDeleteCorseView(APIView):
    permission_classes=[permissions.IsAuthenticated, TeachersOnly]

    def put(self, request, courseId=None):
        '''Редактирование групп учителем'''

        try:
            courses = Course.objects.get(pk=courseId)
            course = UpdateCourseSerializer(instance=courses, data=request.data)
            if course.is_valid():
                course.save()
            return Response(course.data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, courseId=None):
        '''Удаление групп учителем'''

        try:
            course = Course.objects.get(pk=courseId)
            course.delete()
            return Response(status=status.HTTP_200_OK)

        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetHomeworkView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, courseId=None):
        '''Вывод дз группы'''

        try:

            homeworks = Homework.objects.filter(course=courseId)

            homeworks = HomeworkSerializer(homeworks, many=True)

            return Response(homeworks.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddHomeworkView(APIView):
    permission_classes=[permissions.IsAuthenticated, TeachersOnly]

    def post(self, request, courseId=None):
        '''Добавление дз группы учителем'''

        try:

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


class UpdateDeleteHomeworkView(APIView):
    permission_classes=[permissions.IsAuthenticated, TeachersOnly]

    def put(self, request, homeworkId=None):
        '''Редактирование дз учителем'''

        try:
            homework = Homework.objects.get(pk=homeworkId)
            homework = UpdateHomeworkSerializer(instance=homework, data=request.data)
            if homework.is_valid():
                homework.save()
            return Response(homework.data, status=status.HTTP_200_OK)

        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, homeworkId=None):
        '''Удаление дз учителем'''

        try:
            homework = Homework.objects.get(pk=homeworkId)
            homework.delete()
            return Response(status=status.HTTP_200_OK)

        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetTimeTableView(APIView):

    def get(self, request, pk):
        '''Вывод расписания группы'''

        try:

            timetable = TimeTable.objects.filter(course=pk)
            serializer = TimeTableByCourseSerializer(timetable, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response(data={ 'error': str(error) },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
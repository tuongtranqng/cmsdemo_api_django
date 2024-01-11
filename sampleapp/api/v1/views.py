import io
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from reportlab.lib import colors

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from django.http import FileResponse

from .serializers import ClassSerializer, TeacherSerializer, StudentSerializer
from sampleapp.models import Class, Teacher, Student


class ClassViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Classes to be viewed or edited."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClassSerializer
    queryset = Class.objects.all()


class TeacherViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Teachers to be viewed or edited."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class StudentViewSet(viewsets.ModelViewSet):
    """API endpoint that allows Students to be viewed or edited."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()


class ExportToPDFView(APIView):
    """API endpoint to export all Classes to PDF file."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """API endpoint to export all Classes to PDF file."""
        buffer = io.BytesIO()

        cm = 2.54
        doc = SimpleDocTemplate(buffer, rightMargin=0, leftMargin=6.5 * cm, topMargin=0, bottomMargin=0)

        data = [('Class', 'Students')]
        for c in Class.objects.all():
            class_info = f'{c.name}\nTeacher: {c.teacher.name}' 
            student_info = '\n'.join([('- ' + stu.name) for stu in c.student_set.all()])
            data.append((class_info, student_info))
        table = Table(
            data,
            colWidths=270,
            style=[
                ('VALIGN',(0, 0),(-1, -1),'MIDDLE'),
                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                ('BOX', (0, 0), (-1, -1), 0.25, colors.black),   
            ]
        )

        elements = []
        elements.append(table)
        doc.build(elements) 

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename="classes.pdf")

from rest_framework import serializers

from sampleapp.models import Class, Teacher, Student


class ClassSerializer(serializers.HyperlinkedModelSerializer):
    teacher_name = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()
    students = serializers.HyperlinkedRelatedField(
        many=True,
        write_only=True,
        view_name='student-detail',
        queryset=Student.objects.all()
    )

    class Meta:
        model = Class
        fields = ['url', 'id', 'name', 'teacher', 'teacher_name', 'student_count', 'students']

    def get_teacher_name(self, obj):
        return obj.teacher.name
    
    def get_student_count(self, obj):
        return obj.student_set.count()
    
    def validate_students(self, students):
        if len(students) == 0:
            raise serializers.ValidationError('There must be at least one student in a class')
        return students
    
    def create(self, validated_data):
        students = validated_data['students']
        del validated_data['students']
        new_class = super().create(validated_data)

        # Add students into class
        for stu in students:
            stu.cclass = new_class
            stu.save()

        return new_class
    
    def update(self, instance, validated_data):
        students = validated_data['students']
        del validated_data['students']
        updated_class = super().update(instance, validated_data)

        # Update students
        Student.objects.filter(cclass=updated_class).update(cclass=None)
        for stu in students:
            stu.cclass = updated_class
            stu.save()

        return updated_class


class TeacherSerializer(serializers.HyperlinkedModelSerializer):
    class_count = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ['url', 'id', 'name', 'class_count']

    def get_class_count(self, obj):
        return Class.objects.filter(teacher=obj).count()


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['url', 'id', 'name', 'cclass', 'class_name']

    def get_class_name(self, obj):
        return obj.cclass.name if obj.cclass else ''

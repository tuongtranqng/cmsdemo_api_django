from unittest.mock import ANY
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from sampleapp.models import Class, Teacher, Student

User = get_user_model()


class ClassTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='ABCD1234')
        self.client.login(username='user1', password='ABCD1234')
        
        self.teacher1 = Teacher.objects.create(name='Mrs. Kim')
        self.class1 = Class.objects.create(name='Class 1', teacher=self.teacher1)
        self.student1 = Student.objects.create(name='Adam', cclass=self.class1)

    def test_user_can_create_class(self):
        """Ensure an authenticated user can create a new Class."""
        url = '/api/classes/'
        data = {
            'name': 'New Class',
            'teacher': f'/api/teachers/{self.teacher1.pk}/'
        }
        self.client.post(url, data)
        self.assertEqual(Class.objects.count(), 2)
    
    def test_user_can_read_classes(self):
        """Ensure an authenticated user can read Classes."""
        # List all classes
        url = '/api/classes/'
        response = self.client.get(url)
        expected_result = [
            {
                'url': ANY,
                'name': self.class1.name,
                'teacher': ANY
            }
        ]
        self.assertEqual(response.data, expected_result)

        # Retrieve a class
        url = f'/api/classes/{self.class1.pk}/'
        response = self.client.get(url)
        expected_result = {
            'url': ANY,
            'name': self.class1.name,
            'teacher': ANY
        }
        self.assertEqual(response.data, expected_result)

    def test_user_can_update_class(self):
        """Ensure an authenticated user can update a Class."""
        url = f'/api/classes/{self.class1.pk}/'
        data = {
            'name': 'Class 1 Updated',
            'teacher': f'/api/teachers/{self.teacher1.pk}/'
        }
        self.client.put(url, data)
        self.assertEqual(Class.objects.get().name, 'Class 1 Updated')

        data = {
            'name': 'Class 1 Updated Final'
        }
        self.client.patch(url, data)
        self.assertEqual(Class.objects.get().name, 'Class 1 Updated Final')

    def test_user_can_delete_class(self):
        """Ensure an authenticated user can delete a Class."""
        url = f'/api/classes/{self.class1.pk}/'
        self.client.delete(url)
        self.assertEqual(Class.objects.count(), 0)

    def test_user_can_assign_new_student_to_an_existing_class(self):
        """Ensure an authenticated user can assign new student to an existing class."""
        new_student = Student.objects.create(name='Eve')
        url = f'/api/students/{new_student.pk}/'
        data = {
            'cclass': f'/api/classes/{self.class1.pk}/'
        }

        self.assertEqual(self.class1.student_set.count(), 1)
        self.client.patch(url, data)
        self.assertEqual(self.class1.student_set.count(), 2)

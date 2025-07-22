from django.test import TestCase
from ..models import Author
from django.urls import reverse

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Tạo dữ liệu test và lưu vào class attribute
        cls.author = Author.objects.create(
            first_name='Big',
            last_name='Bob',
            date_of_birth='2000-01-01',
            date_of_death='2020-01-01'
        )

    def test_first_name_label(self):
        field_label = self.author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_date_of_death_label(self):
        field_label = self.author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'mất năm')

    def test_first_name_max_length(self):
        max_length = self.author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        expected_object_name = f'{self.author.last_name}, {self.author.first_name}'
        self.assertEqual(expected_object_name, str(self.author))

    def test_get_absolute_url(self):
        expected_url = reverse('catalog:author-detail', kwargs={'pk': self.author.id}) 
        self.assertEqual(self.author.get_absolute_url(), expected_url)


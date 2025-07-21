from django.test import TestCase
from django.urls import reverse
from ..models import Author

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Tạo 15 authors để test phân trang (10 items/page)
        number_of_authors = 15
        for author_id in range(number_of_authors):
            Author.objects.create(
                first_name=f'First {author_id}',
                last_name=f'Last {author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/catalog/authors/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('catalog:authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('catalog:authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('catalog:authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['author_list']), 10)

    def test_lists_all_authors(self):
        # Trang 2 phải có 5 items còn lại (15 - 10 = 5)
        response = self.client.get(reverse('catalog:authors') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['author_list']), 5)


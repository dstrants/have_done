import json

import pytest
from django.http import JsonResponse
from django.test import RequestFactory

from factories.productivity import CategoryFactory
from factories.user import AdminUser
from productivity.models import Category
from productivity.views import (CategoryFastUpdateListView, create_category,
                                find_category)


@pytest.mark.django_db
class TestCategory:
    """Tests for the `productivity.models.Category` model and its views."""
    @staticmethod
    def test_create_category(rf: RequestFactory):
        """Tests the category creation view."""
        request = rf.post("/prod/category/create?name=testing&emoji=😀")
        request.user = AdminUser()
        response = create_category(request)

        cat = Category.objects.get(name='testing', emoji='😀')
        assert cat
        assert cat.name == 'testing'
        assert cat.emoji == '😀'

        assert response.status_code == 200
        assert isinstance(response, JsonResponse)
        content = json.loads(response.content)
        assert {"success": "Category @testing created"} == content

    @staticmethod
    def test_get_create_category_rejection(rf: RequestFactory):
        """Creating category with get should fail."""
        request = rf.get('/prod/category/create?name=testing&emoji=😀')
        request.user = AdminUser()
        response = create_category(request)

        assert response
        assert response.status_code == 400

    @staticmethod
    def test_create_category_with_missing_title(rf: RequestFactory):
        """Creating category with missing title should fail."""
        request = rf.post("/prod/category/create?emoji=😀")
        request.user = AdminUser()
        response = create_category(request)

        assert response.status_code == 400

    @staticmethod
    def test_create_category_with_missing_emoji(rf: RequestFactory):
        """Creating category with missing emoji should fail."""
        request = rf.post("/prod/category/create?title=testing")
        request.user = AdminUser()
        response = create_category(request)

        assert response.status_code == 400

    @staticmethod
    def test_find_category(rf: RequestFactory):
        """Test finding category with title view."""
        cat = CategoryFactory(name='testing')
        request = rf.get('/prod/category/find?cat=testing')
        request.user = AdminUser()
        response = find_category(request)

        assert response
        assert response.status_code == 200
        content = json.loads(response.content)
        assert cat.name == content[0]['fields']['name']
        assert cat.emoji == content[0]['fields']['emoji']

    @staticmethod
    def test_find_missing_category(rf: RequestFactory):
        """Tests finding a non-existing category."""
        request = rf.get('/prod/category/find?cat=testing')
        request.user = AdminUser()
        response = find_category(request)

        assert response
        assert response.status_code == 200
        assert 'Not Found' in response.content.decode()

    @staticmethod
    def test_category_str():
        """Validates `Category.__str__`."""
        cat = CategoryFactory()
        assert cat
        assert cat.__str__() == f"{cat.emoji} {cat.name}"

    @staticmethod
    def test_task_fast_update_category_list_view(rf):
        """Tests listing categories endpoint."""
        request = rf.get("categorie/list")
        request.user = AdminUser()
        response = CategoryFastUpdateListView.as_view()(request)

        assert response
        assert response.status_code == 200

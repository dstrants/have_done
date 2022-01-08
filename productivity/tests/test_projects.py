import json

import pytest
from django.test import RequestFactory

from factories.productivity import ProjectFactory
from factories.user import AdminUser
from productivity.models import Project
from productivity.views import (ProjectFastUpdateListView, create_project,
                                find_project)


@pytest.mark.django_db
class TestProjects:
    """Tests of the views and model of `productivity.models.Project`."""
    @staticmethod
    def test_create_project(rf: RequestFactory):
        """Tests project creation view."""
        request = rf.post("/prod/project/create?name=testing&color=123456")
        request.user = AdminUser()
        response = create_project(request)

        pro = Project.objects.get(name='testing', color='123456')
        assert pro
        assert pro.name == 'testing'
        assert pro.color == '123456'

        assert response.status_code == 200
        content = json.loads(response.content)
        assert {"success": "Project #testing created"} == content

    @staticmethod
    def test_get_create_project_rejection(rf: RequestFactory):
        """Projection creation using `GET` should fail."""
        request = rf.get('/prod/project/create?name=testing&color=789456')
        request.user = AdminUser()
        response = create_project(request)

        assert response
        assert response.status_code == 400

    @staticmethod
    def test_create_project_with_missing_title(rf: RequestFactory):
        """Createing project without title shoudl fail."""
        request = rf.post("/prod/project/create?color=#456789")
        request.user = AdminUser()
        response = create_project(request)

        assert response.status_code == 400

    @staticmethod
    def test_create_project_with_missing_color(rf: RequestFactory):
        """Creating a project without a color should fail."""
        request = rf.post("/prod/project/create?title=testing")
        request.user = AdminUser()
        response = create_project(request)

        assert response.status_code == 400

    @staticmethod
    def test_find_project(rf: RequestFactory):
        """Project quickfind method."""
        pro = ProjectFactory(name='testing')
        request = rf.get('/prod/project/find?pro=testing')
        request.user = AdminUser()
        response = find_project(request)

        assert response
        assert response.status_code == 200
        content = json.loads(response.content)
        assert pro.name == content[0]['fields']['name']
        assert pro.color == content[0]['fields']['color']

    @staticmethod
    def test_find_missing_project(rf: RequestFactory):
        """Finding a non existing project should fail."""
        request = rf.get('/prod/project/find?pro=testing')
        request.user = AdminUser()
        response = find_project(request)

        assert response
        assert response.status_code == 200
        assert 'Not Found' in response.content.decode()

    @staticmethod
    def test_project_color_prefix_removal():
        """If color has `#` prefix it should be removed."""
        project = ProjectFactory(color="#f4f4f4")

        assert project
        assert project.color == 'f4f4f4'

    @staticmethod
    def test_task_fast_update_project_list_view(rf):
        """Tests the task fast update project listing view."""
        request = rf.get("projects/list")
        request.user = AdminUser()
        response = ProjectFastUpdateListView.as_view()(request)

        assert response
        assert response.status_code == 200

    @staticmethod
    def test_project_model_str():
        """Validates `Project.__str__`."""
        project = ProjectFactory()
        assert project.__str__() == "#" + project.name

from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.http import HttpRequest

# Create your tests here.
from django.test import TestCase
from django.test.client import RequestFactory

from Student.models import Students

from .models import AllTracker, ImpactChallengeTable, MUNChallengeTable
from .views import Login_View


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

    def test_check_team_and_return_response(self):
        # Create and setup a mock request
        request = HttpRequest()
        request.user = self.user

        # Simulate the Students queryset result
        students_mock = Mock()
        students_mock.filter.return_value.values.return_value = [
            {"name": "StudentName", "team": 1}
        ]
        with patch("Student.models.Students.objects", students_mock):
            view = Login_View()
            response = view.check_team_and_return_response(
                request, self.user, "testuser"
            )

        self.assertEqual(
            response.status_code, 200
        )  # Assuming a successful response

    def test_create_response_for_team(self):
        # Create and setup a mock request
        request = HttpRequest()

        # Simulate the AllTracker queryset result
        alltracker_mock = Mock()
        alltracker_mock.filter.return_value.exists.return_value = True
        alltracker_mock.filter.return_value.first.return_value.challenge = (
            "ChallengeName"
        )
        with patch("Core.models.AllTracker.objects", alltracker_mock):
            view = Login_View()
            response = view.create_response_for_team(request, "StudentName", 1)

        self.assertEqual(
            response.status_code, 200
        )  # Assuming a successful response

    def test_get_challenge_status(self):
        # Simulate the MUNChallengeTable queryset result
        munchallenge_mock = Mock()
        munchallenge_mock.filter.return_value.exists.return_value = True
        munchallenge_mock.filter.return_value.values.return_value = [
            {"status": "Completed"}
        ]
        with patch("Core.models.MUNChallengeTable.objects", munchallenge_mock):
            view = Login_View()
            status = view.get_challenge_status("StudentName")

        self.assertEqual(status, [{"status": "Completed"}])

    def test_login_failed_response(self):
        # Create and setup a mock request
        request = HttpRequest()

        view = Login_View()
        response = view.login_failed_response(request)

        self.assertEqual(
            response.status_code, 200
        )  # Assuming a successful response

    def test_get(self):
        request = self.factory.get("/login/")
        view = Login_View.as_view()
        response = view(request)

        self.assertEqual(
            response.status_code, 200
        )  # Assuming a successful response

    def test_post(self):
        request = self.factory.post(
            "/login/", {"username": "testuser", "password": "testpassword"}
        )
        view = Login_View.as_view()
        response = view(request)

        self.assertEqual(
            response.status_code, 200
        )  # Assuming a successful response

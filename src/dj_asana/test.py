from unittest import mock

from django.conf import settings
from django.test import TestCase

from .models import AsanaProject, AsanaTask, AsanaUser, asana_client


class AsanaProjectTestCase(TestCase):

    def test_create(self):
        with mock.patch.object(asana_client.projects, 'create_project', return_value={'gid': '12345'}) as mock_create:
            AsanaProject.objects.create(name='Test project')
        mock_create.assert_called_once_with(
            workspace=settings.ASANA_WORKSPACE_GID,
            name='Test project'
        )

    def test_update(self):
        with mock.patch.object(asana_client.projects, 'create_project', return_value={'gid': '12345'}):
            project = AsanaProject.objects.create(name='Test project')
        with mock.patch.object(asana_client.projects, 'update_project') as mock_update:
            project.name = 'New name'
            project.save()
        mock_update.assert_called_once_with(
            gid='12345',
            name='New name'
        )

    def test_no_update(self):
        with mock.patch.object(asana_client.projects, 'create_project', return_value={'gid': '12345'}):
            project = AsanaProject.objects.create(name='Test project')
        with mock.patch.object(asana_client.projects, 'update_project') as mock_update:
            project.save()
        # Ensure that no API calls was made if object wasn't changed
        mock_update.assert_not_called()


class AsanaTaskTestCase(TestCase):
    def setUp(self) -> None:
        with mock.patch.object(asana_client.projects, 'create_project', return_value={'gid': '12345'}):
            self.project = AsanaProject.objects.create(name='Test project')
        self.user = AsanaUser.objects.create(gid='54321', name='Test User')

    def test_create(self):
        with mock.patch.object(asana_client.tasks, 'create_task', return_value={'gid': '23456'}) as mock_create:
            AsanaTask.objects.create(
                name='Test task',
                project=self.project,
                assignee=self.user
            )
        mock_create.assert_called_once_with(
            workspace=settings.ASANA_WORKSPACE_GID,
            name='Test task',
            projects=[self.project.gid],
            assignee=self.user.gid
        )

    def test_create_no_assignee(self):
        with mock.patch.object(asana_client.tasks, 'create_task', return_value={'gid': '23456'}) as mock_create:
            AsanaTask.objects.create(
                name='Test task',
                project=self.project
            )
        mock_create.assert_called_once_with(
            workspace=settings.ASANA_WORKSPACE_GID,
            name='Test task',
            projects=[self.project.gid],
            assignee=None
        )

    def test_update_name(self):
        with mock.patch.object(asana_client.tasks, 'create_task', return_value={'gid': '23456'}):
            task = AsanaTask.objects.create(
                name='Test task',
                project=self.project,
                assignee=self.user
            )
        with mock.patch.object(asana_client.tasks, 'update_task') as mock_update:
            task.name = 'New name'
            task.save()
        mock_update.assert_called_once_with(
            task_gid='23456',
            name='New name'
        )

    def test_update_project(self):
        with mock.patch.object(asana_client.tasks, 'create_task', return_value={'gid': '23456'}):
            task = AsanaTask.objects.create(
                name='Test task',
                project=self.project,
                assignee=self.user
            )
        with mock.patch.object(asana_client.projects, 'create_project', return_value={'gid': '99999'}):
            other_project = AsanaProject.objects.create(name='New project')
        with mock.patch.object(asana_client.tasks, 'update_task') as mock_update:
            task.project = other_project
            task.save()
        mock_update.assert_called_once_with(
            task_gid='23456',
            project=other_project.gid
        )

    def test_update_assignee(self):
        with mock.patch.object(asana_client.tasks, 'create_task', return_value={'gid': '23456'}):
            task = AsanaTask.objects.create(
                name='Test task',
                project=self.project,
                assignee=self.user
            )
        other_user = AsanaUser.objects.create(gid='723123', name='Some Other User')
        with mock.patch.object(asana_client.tasks, 'update_task') as mock_update:
            task.assignee = other_user
            task.save()
        mock_update.assert_called_once_with(
            task_gid='23456',
            assignee=other_user.gid
        )

    def test_no_update(self):
        with mock.patch.object(asana_client.tasks, 'create_task', return_value={'gid': '23456'}):
            task = AsanaTask.objects.create(
                name='Test task',
                project=self.project,
                assignee=self.user
            )
        with mock.patch.object(asana_client.tasks, 'update_task') as mock_update:
            task.save()
        # Ensure that no API calls was made if object wasn't changed
        mock_update.assert_not_called()

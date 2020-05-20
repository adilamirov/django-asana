import asana
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


asana_client = asana.Client.access_token(settings.ASANA_ACCESS_TOKEN)


class AsanaUser(models.Model):
    gid = models.CharField(
        primary_key=True,
        max_length=settings.ASANA_GID_MAX_LENGTH,
        verbose_name=_('Globally unique identifier')
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_('Full name')
    )

    def __str__(self):
        return self.name


class AsanaProject(models.Model):
    gid = models.CharField(
        primary_key=True,
        max_length=settings.ASANA_GID_MAX_LENGTH,
        verbose_name=_('Globally unique identifier')
    )

    name = models.CharField(
        max_length=255,
        verbose_name=_('Project name')
    )

    def __str__(self):
        return self.name

    def _create_project(self):
        project = asana_client.projects.create_project(workspace=settings.ASANA_WORKSPACE_GID, name=self.name)
        self.gid = project['gid']

    def _update_project(self):
        old = AsanaProject.objects.get(pk=self.pk)
        if old.name != self.name:
            asana_client.projects.update_project(gid=self.gid, name=self.name)

    def save(self, *args, **kwargs):
        if not self.gid:
            self._create_project()
        else:
            self._update_project()
        return super().save(*args, **kwargs)


class AsanaTask(models.Model):
    gid = models.CharField(
        primary_key=True,
        max_length=settings.ASANA_GID_MAX_LENGTH,
        verbose_name=_('Globally unique identifier')
    )

    project = models.ForeignKey(
        AsanaProject,
        related_name='tasks',
        on_delete=models.CASCADE,
        verbose_name=_('Project')
    )

    name = models.TextField(
        verbose_name=_('Task name')
    )

    assignee = models.ForeignKey(
        AsanaUser,
        related_name='tasks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Assignee')
    )

    def __str__(self):
        return f'[{self.project}] {self.name}'

    def _create_task(self):
        task = asana_client.tasks.create_task(
            workspace=settings.ASANA_WORKSPACE_GID,
            name=self.name,
            projects=[self.project.gid],
            assignee=self.assignee.gid if self.assignee else None
        )
        self.gid = task['gid']

    def _update_task(self):
        old = AsanaTask.objects.get(pk=self.pk)
        update_dict = {}
        if old.name != self.name:
            update_dict['name'] = self.name
        if old.assignee != self.assignee:
            update_dict['assignee'] = self.assignee.gid
        if old.project != self.project:
            update_dict['project'] = self.project.gid
        if update_dict:
            asana_client.tasks.update_task(task_gid=self.gid, **update_dict)

    def save(self, *args, **kwargs):
        if not self.gid:
            self._create_task()
        else:
            self._update_task()
        return super().save(*args, **kwargs)

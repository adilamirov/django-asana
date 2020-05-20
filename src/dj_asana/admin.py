from django.contrib import admin

from src.dj_asana.models import AsanaProject, AsanaTask, AsanaUser


class AsanaObjectAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return self.readonly_fields
        return ('gid',) + self.readonly_fields

    def get_fields(self, request, obj=None):
        if not obj:
            return self.fields
        return ('gid',) + self.fields


@admin.register(AsanaProject)
class AsanaProjectAdmin(AsanaObjectAdmin):
    search_fields = ('name',)
    list_display = ('gid', 'name')
    fields = ('name',)


@admin.register(AsanaTask)
class AsanaTaskAdmin(AsanaObjectAdmin):
    search_fields = ('name', 'project__name', 'assignee__name')
    list_display = ('name', 'project', 'assignee')
    fields = ('name', 'project', 'assignee')


@admin.register(AsanaUser)
class AsanaTaskAdmin(AsanaObjectAdmin):
    search_fields = ('name',)
    list_display = ('name',)
    readonly_fields = fields = ('name',)

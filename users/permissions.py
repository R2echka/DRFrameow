from rest_framework import permissions


class Moderator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="modemeowers").exists()

class Owner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

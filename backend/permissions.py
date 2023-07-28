from rest_framework import permissions


class SemdPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        if view.action in ['list', 'create', 'retrieve', 'update', 'destroy']:
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'OPTIONS':
            return True
        if view.action in ['list', 'create', 'retrieve', 'update', 'destroy']:
            return request.user.is_authenticated
        else:
            return False


class MedicalServicePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        if view.action in ['list']:
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'OPTIONS':
            return True
        if view.action in ['list']:
            return request.user.is_authenticated
        else:
            return False


class DiagnosisPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        if view.action in ['list']:
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'OPTIONS':
            return True
        if view.action in ['list']:
            return request.user.is_authenticated
        else:
            return False


class MedicalOrganizationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        if view.action in ['list']:
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'OPTIONS':
            return True
        if view.action in ['list']:
            return request.user.is_authenticated
        else:
            return False


class LaboratoryTestPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'OPTIONS':
            return True
        if view.action in ['list']:
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'OPTIONS':
            return True
        if view.action in ['list']:
            return request.user.is_authenticated
        else:
            return False


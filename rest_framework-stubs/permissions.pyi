from typing import Any, Dict, List, Sequence, Type

from django.db.models import Model, QuerySet
from django.http import HttpRequest
from django.views import View

SAFE_METHODS: Sequence[str] = ("GET", "HEAD", "OPTIONS")

class OperationHolderMixin:
    def __and__(self, other: Any) -> OperandHolder: ...
    def __or__(self, other: Any) -> OperandHolder: ...
    def __rand__(self, other: Any) -> OperandHolder: ...
    def __ror__(self, other: Any) -> OperandHolder: ...

class OperandHolder(OperationHolderMixin):
    operator_class: Type[Any]
    op1_class: Type[Any]
    op2_class: Type[Any]
    def __init__(self, operator_class: Type[Any], op1_class: Type[Any], op2_class: Type[Any]): ...
    def __call__(self, *args, **kwargs) -> Any: ...

class AND:
    def __init__(self, op1: BasePermission, op2: BasePermission) -> None: ...
    def has_permission(self, request: HttpRequest, view: View) -> bool: ...
    def has_object_permission(self, request: HttpRequest, view: View, obj: Any) -> bool: ...

class OR:
    def __init__(self, op1: BasePermission, op2: BasePermission) -> None: ...
    def has_permission(self, request: HttpRequest, view: View) -> bool: ...
    def has_object_permission(self, request: HttpRequest, view: View, obj: Any) -> bool: ...

class BasePermissionMetaclass(OperationHolderMixin, type): ...

class BasePermission(object):
    def has_permission(self, request: HttpRequest, view: View) -> bool: ...
    def has_object_permission(self, request: HttpRequest, view: View, obj: Any) -> bool: ...

class AllowAny(BasePermission): ...
class IsAuthenticated(BasePermission): ...
class IsAdminUser(BasePermission): ...
class IsAuthenticatedOrReadOnly(BasePermission): ...

class DjangoModelPermissions(BasePermission):
    perms_map: Dict[str, List[str]] = ...

    authenticated_users_only: bool = ...
    def get_required_permissions(self, method: str, model_cls: Type[Model]) -> List[str]: ...
    def _queryset(self, view: View) -> QuerySet[Any]: ...

class DjangoModelPermissionsOrAnonReadOnly(DjangoModelPermissions): ...

class DjangoObjectPermissions(DjangoModelPermissions):
    def get_required_object_permissions(self, method: str, model_cls: Type[Model]) -> List[str]: ...
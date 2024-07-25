from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class SupervisorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_supervisor

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to access this page.")

class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_student

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to access this page.")

class UnitCoordinatorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_unit_coordinator

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to access this page.")
    
class SupervisorOrUnitCoordinatorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_supervisor or self.request.user.is_unit_coordinator

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to access this page.")
    
class SupervisorOrStudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_supervisor or self.request.user.is_student

    def handle_no_permission(self):
        raise PermissionDenied("You do not have permission to access this page.")
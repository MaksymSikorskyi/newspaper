from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView


class ProfileView(LoginRequiredMixin, DetailView):
    context_object_name = "current_user"
    template_name = "users/profile.html"

    def get_object(self, queryset=None):
        return self.request.user

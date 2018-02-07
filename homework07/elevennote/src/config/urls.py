from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='notes/'), name='index'),
    path('notes/', include('notes.urls', namespace='notes')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('api/', include('api.urls', namespace='api')),
    path('admin/', admin.site.urls),
]

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('notes/', include('notes.urls', namespace='notes')),
    path('admin/', admin.site.urls),
]

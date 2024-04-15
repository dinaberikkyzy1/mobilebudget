from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path("", include("diplomaproject.urls")),
    path('admin/', admin.site.urls),
    path('convert/',views.convert_pdf_to_json, name='convert_pdf_to_json'),
    path('export_pdf/', views.export_to_pdf, name='export_to_pdf'),
    path('onboarding/step1/', views.onboarding_step1, name='onboarding_step1'),
    path('onboarding/step2/', views.onboarding_step2, name='onboarding_step2'),
    path('onboarding/step3/', views.onboarding_step3, name='onboarding_step3'),
    path('onboarding/complete/', views.onboarding_complete, name='onboarding_complete'),
]

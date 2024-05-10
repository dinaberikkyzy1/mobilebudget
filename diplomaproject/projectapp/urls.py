from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path('convert/',views.convert_pdf_to_json, name='convert_pdf_to_json'),
    path('export_pdf/', views.export_to_pdf, name='export_to_pdf'),
    path('onboarding_step1/', views.onboarding_step1, name='onboarding_step1'),
    path('onboarding_step2/', views.onboarding_step2, name='onboarding_step2'),
    path('onboarding_step3/', views.onboarding_step3, name='onboarding_step3'),
    path('onboarding_complete/', views.onboarding_complete, name='onboarding_complete'),
    path('api/question', views.QuestionView.as_view(), name='question_view'),
    path('api/answer', views.UserResponseView.as_view(), name='response_view'),

]

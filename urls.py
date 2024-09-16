from django.urls import path
from .views import (
    IndexView,
    add_employee,
    edit_employee,
    delete_employee,
    search_employee,
    index_dpt,
    employee_detail,
    dpt_detail,
    add_department,
    edit_department,
    delete_department,
    dashboard,
    index_pst,
    index_nt,
    add_pst,
    add_nt,
    advanced_search,
    edit_pst,
    delete_pst,
    edit_nt,
    delete_nt,
    export,
    schedule,
)
from django.conf import settings
from django.conf.urls.static import static

app_name = 'employee'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add/', add_employee, name='add_employee'),
    path('<int:pk>/edit/', edit_employee, name='edit_employee'),
    path('<int:pk>/delete/', delete_employee, name='delete_employee'),
    path('search/', search_employee, name='search_employee'),
    path('index_dpt/', index_dpt, name='index_dpt'),
    path('<int:pk>/detail', employee_detail, name='employee_detail'),
    path('<int:pk>/department_detail', dpt_detail, name='department_detail'),
    path('add_department/', add_department, name='add_department'),
    path('<int:pk>/edit_department', edit_department, name='edit_department'),
    path('<int:pk>/delete_department', delete_department, name='delete_department'),
    path('dashboard', dashboard, name='dashboard'),
    path('index_pst', index_pst, name='index_pst'),
    path('index_nt', index_nt, name='index_nt'),
    path('add_pst', add_pst, name='add_pst'),
    path('add_nt', add_nt, name='add_nt'),
    path('advanced_search', advanced_search, name='advanced_search'),
    path('<int:pk>/edit_pst', edit_pst, name='edit_pst'),
    path('<int:pk>/delete_pst', delete_pst, name='delete_pst'),
    path('<int:pk>/edit_nt', edit_nt, name='edit_nt'),
    path('<int:pk>/delete_nt', delete_nt, name='delete_nt'),
    path('export', export, name='export'),
    path('schedule', schedule, name='schedule'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

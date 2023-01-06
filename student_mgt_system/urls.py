"""student_mgt_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from student_mgt_app import views, HodViews, StaffViews, StudentViews, WardenViews
from student_mgt_app.EditViewResultClass import EditViewResultClass
from student_mgt_system import settings

urlpatterns = [
    path('demo', views.showDemoPage),
    path('', views.ShowLoginPage, name="show_login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('get_user_details', views.getUserDetails),
    path('logout_user', views.logout_user, name="logout"),
    path('admin/', admin.site.urls),
    path('doLogin', views.doLogin, name="do_login"),
    path('admin_home', HodViews.admin_home, name="admin_home"),
    path('add_staff', HodViews.add_staff, name="add_staff"),
    path('add_staff_save', HodViews.add_staff_save, name="add_staff_save"),
    path('add_warden', HodViews.add_warden, name="add_warden"),
    path('add_warden_save', HodViews.add_warden_save, name="add_warden_save"),
    path('add_course', HodViews.add_course, name="add_course"),
    path('add_course_save', HodViews.add_course_save, name="add_course_save"),
    path('add_student', HodViews.add_student, name="add_student"),
    path('add_student_save', HodViews.add_student_save, name="add_student_save"),
    path('add_hostel', HodViews.add_hostel, name="add_hostel"),
    path('add_hostel_save', HodViews.add_hostel_save, name="add_hostel_save"),
    path('add_subject', HodViews.add_subject, name="add_subject"),
    path('add_subject_save', HodViews.add_subject_save, name="add_subject_save"),
    path('manage_staff', HodViews.manage_staff, name="manage_staff"),
    path('manage_student', HodViews.manage_student, name="manage_student"),
    path('manage_warden', HodViews.manage_warden, name="manage_warden"),
    path('staff_profile/<str:staff_id>', HodViews.staff_profile, name="staff_profile"),
    path('student_profile/<str:student_id>', HodViews.student_profile, name="student_profile"),
    path('warden_profile/<str:warden_id>', HodViews.warden_profile, name="warden_profile"),
    path('edit_staff_profile/<str:staff_id>', HodViews.edit_staff_profile, name="edit_staff_profile"),
    path('edit_student_profile/<str:student_id>', HodViews.edit_student_profile, name="edit_student_profile"),
    path('manage_courses', HodViews.manage_courses, name="manage_courses"),
    path('edit_course/<str:course_id>', HodViews.edit_course, name="edit_course"),
    path('manage_subjects', HodViews.manage_subjects, name="manage_subjects"),
    path('edit_subjects/<str:subject_id>', HodViews.edit_subjects, name="edit_subjects"),
    path('manage_hostel', HodViews.manage_hostel, name="manage_hostel"),
    path('edit_hostel/<str:hostel_id>', HodViews.edit_hostel, name="edit_hostel"),
    path('add_item_inventory', HodViews.add_item_inventory, name="add_item_inventory"),
    path('add_item_inventory_save', HodViews.add_item_inventory_save, name="add_item_inventory_save"),
    path('manage_inventory', HodViews.manage_inventory, name="manage_inventory"),
    path('shopping', HodViews.shopping, name="shopping"),
    path('add_student_bill', HodViews.add_student_bill, name="add_student_bill"),
    path('edit_staff_save', HodViews.edit_staff_save, name="edit_staff_save"),
    path('edit_student_save', HodViews.edit_student_save, name="edit_student_save"),
    path('edit_course_save', HodViews.edit_course_save, name="edit_course_save"),
    path('edit_subject_save', HodViews.edit_subject_save, name="edit_subject_save"),
    path('edit_hostel_save', HodViews.edit_hostel_save, name="edit_hostel_save"),
    path('manage_session', HodViews.manage_session, name="manage_session"),
    path('add_session_save', HodViews.add_session_save, name="add_session_save"),
    path('view_session', HodViews.view_session, name="view_session"),
    path('delete_session/<str:session_year_id>', HodViews.delete_session, name="delete_session"),
    path('check_email_exist', HodViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist', HodViews.check_username_exist, name="check_username_exist"),
    path('student_feedback_message', HodViews.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_replied', HodViews.student_feedback_message_replied, name="student_feedback_message_replied"),
    path('staff_feedback_message_replied', HodViews.staff_feedback_message_replied, name="staff_feedback_message_replied"),
    path('staff_feedback_message', HodViews.staff_feedback_message, name="staff_feedback_message"),
    path('student_leave_view', HodViews.student_leave_view, name="student_leave_view"),
    path('student_approve_leave/<str:leave_id>', HodViews.student_approve_leave, name="student_approve_leave"),
    path('student_reject_leave/<str:leave_id>', HodViews.student_reject_leave, name="student_reject_leave"),
    path('staff_leave_view', HodViews.staff_leave_view, name="staff_leave_view"),
    path('staff_approve_leave/<str:leave_id>', HodViews.staff_approve_leave, name="staff_approve_leave"),
    path('staff_reject_leave/<str:leave_id>', HodViews.staff_reject_leave, name="staff_reject_leave"),
    path('admin_view_attendance', HodViews.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates', HodViews.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_student', HodViews.admin_get_attendance_student, name="admin_get_attendance_student"),
    path('admin_profile', HodViews.admin_profile, name="admin_profile"),
    path('edit_profile_save', HodViews.edit_profile_save, name="edit_profile_save"),
    path('send_notification_staff', HodViews.send_notification_staff, name="send_notification_staff"),
    path('send_notification_staff_save', HodViews.send_notification_staff_save, name="send_notification_staff_save"),
    path('delete_notification_staff/<str:notification_id>', HodViews.delete_notification_staff, name="delete_notification_staff"),
    path('send_notification_student', HodViews.send_notification_student, name="send_notification_student"),
    path('send_notification_student_save', HodViews.send_notification_student_save, name="send_notification_student_save"),
    path('delete_notification_student/<str:notification_id>', HodViews.delete_notification_student, name="delete_notification_student"),
    path('generate_bonafide_certi/<str:student_id>', HodViews.generate_bonafide_certi, name="generate_bonafide_certi"),
    path('generate_leaving_certi/<str:student_id>', HodViews.generate_leaving_certi, name="generate_leaving_certi"),
    path('add_transport_route', HodViews.add_transport_route, name="add_transport_route"),
    path('add_transport_route_save', HodViews.add_transport_route_save, name="add_transport_route_save"),
    path('view_added_routes', HodViews.view_added_routes, name="view_added_routes"),
    path('fees_management', HodViews.fees_management, name="fees_management"),


    #Staff URL Paths

    path('staff_home', StaffViews.staff_home, name="staff_home"),
    path('staff_take_attendance', StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path('staff_update_attendance', StaffViews.staff_update_attendance, name="staff_update_attendance"),
    path('get_students', StaffViews.get_students, name="get_students"),
    path('get_attendance_dates', StaffViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student', StaffViews.get_attendance_student, name="get_attendance_student"),
    path('save_attendance_data', StaffViews.save_attendance_data, name="save_attendance_data"),
    path('save_updateattendance_data', StaffViews.save_updateattendance_data, name="save_updateattendance_data"),
    path('staff_apply_leave', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback', StaffViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save', StaffViews.staff_feedback_save, name="staff_feedback_save"),
    path('staff_add_result', StaffViews.staff_add_result, name="staff_add_result"),
    path('save_student_result', StaffViews.save_student_result, name="save_student_result"),
    path('edit_student_result', EditViewResultClass.as_view(), name="edit_student_result"),
    path('fetch_result_student', StaffViews.fetch_result_student, name="fetch_result_student"),

    # Student URL Paths

    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_view_attendance', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_view_result', StudentViews.student_view_result, name="student_view_result"),
    path('student_book_transport', StudentViews.student_book_transport, name="student_book_transport"),

    # Warden URL Paths

    path('warden_home', WardenViews.warden_home, name="warden_home"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

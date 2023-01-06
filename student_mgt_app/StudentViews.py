import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from student_mgt_app.models import *


def student_home(request):
    students = Students.objects.get(admin=request.user.id)
    attendance_total = AttendanceReport.objects.filter(student_id=students).count()
    attendance_present = AttendanceReport.objects.filter(student_id=students, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(student_id=students, status=False).count()
    course = Courses.objects.get(id=students.course_id.id)
    subjects = Subjects.objects.filter(course_id=course).count()
    notifications = NotificationStudent.objects.all()

    subject_name=[]
    data_present=[]
    data_absent=[]
    subject_data = Subjects.objects.filter(course_id=students.course_id)
    for subject in subject_data:
        attendance = Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=students.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=students.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
    return render(request, "student_template/student_home_template.html", {"students": students,
                                                                           "attendance_total": attendance_total,
                                                                           "attendance_present": attendance_present,
                                                                           "attendance_absent": attendance_absent,
                                                                           "subjects": subjects,
                                                                           "data_name": subject_name,
                                                                           "notifications": notifications,
                                                                           "data1":data_present, "data2": data_absent})


def student_view_attendance(request):
    students = Students.objects.get(admin=request.user.id)
    course = Courses.objects.get(id=students.course_id.id)
    subjects = Subjects.objects.filter(course_id=course)
    return render(request, "student_template/student_view_attendance.html", {"students": students, "subjects": subjects})


def student_view_attendance_post(request):
    subject_id = request.POST.get("subject")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    start_date_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
    subject_obj = Subjects.objects.get(id=subject_id)
    user_object = CustomUser.objects.get(id=request.user.id)
    students = Students.objects.get(admin=user_object)

    attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse), subject_id=subject_obj)
    attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=students)
    return render(request, "student_template/student_attendance_data.html", {"attendance_reports": attendance_reports, "students": students})


def student_apply_leave(request):
    students = Students.objects.get(admin=request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id=students)
    return render(request, "student_template/student_apply_leave.html", {"students": students, "leave_data": leave_data})


def student_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_reason = request.POST.get("leave_reason")

        try:
            students = Students.objects.get(admin=request.user.id)
            leave_report = LeaveReportStudent(student_id=students, leave_date=leave_date, leave_message=leave_reason,
                                            leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))
        except:
            messages.error(request, "Failed to Apply for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))


def student_feedback(request):
    students = Students.objects.get(admin=request.user.id)
    feedback_data = FeedbackStudent.objects.filter(student_id=students)
    return render(request, "student_template/student_feedback.html", {"students": students, "feedback_data": feedback_data})


def student_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        try:
            students = Students.objects.get(admin=request.user.id)
            feedback = FeedbackStudent(student_id=students, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Submitted Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed to Submit Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))


def student_view_result(request):
    students = Students.objects.get(admin=request.user.id)
    studentresult = StudentResult.objects.filter(student_id=students.id)
    return render(request, "student_template/student_result.html", {"studentresult": studentresult, "students": students})


def student_book_transport(request):
    students = Students.objects.get(admin=request.user.id)
    routes = TransportAddRoute.objects.all()
    return render(request, "student_template/transport_booking_template.html", {"students": students, "routes": routes})

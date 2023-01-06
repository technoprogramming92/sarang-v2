import json
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import inflect


from student_mgt_app.models import *


def admin_home(request):
    student_count = Students.objects.all().count()
    staff_count = Staffs.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()

    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []

    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subjects_all:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    return render(request, "hod_template/home_content.html", {"student_count": student_count, "staff_count": staff_count,
                                                              "subject_count": subject_count, "course_count": course_count,
                                                              "course_name_list": course_name_list,
                                                              "subject_count_list": subject_count_list,
                                                              "student_count_list_in_course": student_count_list_in_course,
                                                              "student_count_list_in_subject": student_count_list_in_subject,
                                                              "subject_list": subject_list})


def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed!")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")
        address = request.POST.get("address")
        contact_number = request.POST.get("contact_number")
        qualification = request.POST.get("qualification")

        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  first_name=first_name, last_name=last_name, user_type=2)
            user.staffs.address = address
            user.staffs.contact_number = contact_number
            user.staffs.qualification = qualification
            user.staffs.profile_pic = profile_pic_url
            user.save()
            messages.success(request, "Staff Added Successfully")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request, "Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))


def add_warden(request):
    hostels = Hostel.objects.all()
    return render(request, "hod_template/add_warden_template.html", {"hostels": hostels})


def add_warden_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed!")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")
        address = request.POST.get("address")
        contact_number = request.POST.get("contact_number")
        hostel_id = request.POST.get("hostel")

        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                                  first_name=first_name, last_name=last_name, user_type=4)
            hostel_obj = Hostel.objects.get(id=hostel_id)
            user.warden.address = address
            user.warden.contact_number = contact_number
            user.warden.profile_pic = profile_pic_url
            user.warden.hostel_id = hostel_obj
            user.save()
            messages.success(request, "Warden Added Successfully")
            return HttpResponseRedirect(reverse("add_warden"))
        except:
            messages.error(request, "Failed to Add Warden")
            return HttpResponseRedirect(reverse("add_warden"))


def add_course(request):
    return render(request, "hod_template/add_course_template.html")


def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course = request.POST.get("course")
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request, "Standard Added Successfully")
            return HttpResponseRedirect(reverse("add_course"))
        except:
            messages.error(request, "Failed to Add Standard")
            return HttpResponseRedirect(reverse("add_course"))


def add_student(request):
    hostels = Hostel.objects.all()
    courses = Courses.objects.all()
    sessions = SessionYearModel.objects.all()
    return render(request, "hod_template/add_student_template.html",
                  {"hostels": hostels, "courses": courses, "sessions": sessions})


def add_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed!")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        unique_id = request.POST.get("unique_id")
        password = request.POST.get("password")
        username = request.POST.get("username")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        contact_number_primary = request.POST.get("contact_number_primary")
        contact_number_parents = request.POST.get("contact_number_parents")
        contact_number_whatsapp = request.POST.get("contact_number_whatsapp")
        contact_number_relative = request.POST.get("contact_number_relative")
        father_name = request.POST.get("father_name")
        mother_name = request.POST.get("mother_name")
        gr_number = request.POST.get("gr_number")
        birth_place = request.POST.get("birth_place")
        birth_date = request.POST.get("birth_date")
        uid = request.POST.get("uid")
        religion = request.POST.get("religion")
        last_school = request.POST.get("last_school")
        admission_date = request.POST.get("admission_date")
        course_id = request.POST.get("course")
        session_year_id = request.POST.get("session")
        hostel_id = request.POST.get("hostel")
        room_number = request.POST.get("room_number")
        locker_number = request.POST.get("locker_number")
        bedding_provided = request.POST.get("bedding_provided")
        dish_provided = request.POST.get("dish_provided")
        bank_balance = float(request.POST.get("bank_balance"))

        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        user = CustomUser.objects.create_user(username=username, password=password, email=email,
                                              first_name=first_name, last_name=last_name,
                                              user_type=3)

        try:
            course_obj = Courses.objects.get(id=course_id)
            hostel_obj = Hostel.objects.get(id=hostel_id)
            session_obj = SessionYearModel.objects.get(id=session_year_id)
            birth_d = birth_date
            adm_date = admission_date
            user.students.unique_id = unique_id
            user.students.address1 = address1
            user.students.address2 = address2
            user.students.city = city
            user.students.state = state
            user.students.pincode = pincode
            user.students.contact_number_primary = contact_number_primary
            user.students.contact_number_parents = contact_number_parents
            user.students.contact_number_whatsapp = contact_number_whatsapp
            user.students.contact_number_relative = contact_number_relative
            user.students.father_name = father_name
            user.students.mother_name = mother_name
            user.students.gr_number = gr_number
            user.students.uid = uid
            user.students.admission_date = adm_date
            user.students.birth_date = birth_d
            user.students.profile_pic = profile_pic_url
            user.students.religion = religion
            user.students.last_school = last_school
            user.students.course_id = course_obj
            user.students.hostel_id = hostel_obj
            user.students.session_year_id = session_obj
            user.students.room_number = room_number
            user.students.locker_number = locker_number
            user.students.bedding_provided = bedding_provided
            user.students.dish_provided = dish_provided
            user.students.birth_place = birth_place
            user.students.bank_balance = bank_balance
            user.save()
            messages.success(request, "Student Added Successfully")
            return HttpResponseRedirect(reverse("add_student"))
        except:
            messages.error(request, "Failed to Add Student")
            return HttpResponseRedirect(reverse("add_student"))


def add_hostel(request):
    return render(request, "hod_template/add_hostel_template.html")


def add_hostel_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        name = request.POST.get("name")
        rooms = request.POST.get("rooms")
        try:
            hostel_model = Hostel(name=name, rooms=rooms)
            hostel_model.save()
            messages.success(request, "Hostel Added Successfully")
            return HttpResponseRedirect(reverse("add_hostel"))
        except:
            messages.error(request, "Failed to Add Hostel")
            return HttpResponseRedirect(reverse("add_hostel"))


def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type="2")
    return render(request, "hod_template/add_subject_template.html", {"courses": courses, "staffs": staffs})


def add_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        course = Courses.objects.get(id=course_id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)
        try:
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            messages.success(request, "Subject Added Successfully")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request, "Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))


def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, "hod_template/manage_staff_template.html", {"staffs": staffs})


def manage_student(request):
    students = Students.objects.all()
    return render(request, "hod_template/manage_student_template.html", {"students": students})


def manage_warden(request):
    wardens = Warden.objects.all()
    return render(request, "hod_template/manage_warden_template.html", {"wardens": wardens})

def staff_profile(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request, "hod_template/staff_profile_template.html", {"staff": staff, "id": staff_id})


def student_profile(request, student_id):
    student = Students.objects.get(admin=student_id)
    return render(request, "hod_template/student_profile_template.html", {"student": student, "id": student_id})


def warden_profile(request, warden_id):
    warden = Warden.objects.get(admin=warden_id)
    return render(request, "hod_template/warden_profile_template.html", {"warden": warden, "id": warden_id})

def edit_student_profile(request, student_id):
    hostels = Hostel.objects.all()
    courses = Courses.objects.all()
    sessions = SessionYearModel.objects.all()
    student = Students.objects.get(admin=student_id)
    return render(request, "hod_template/edit_student_profile_template.html", {"student": student, "id": student_id,
                                                                               "hostels": hostels, "courses": courses, "sessions": sessions})


def edit_staff_profile(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request, "hod_template/edit_staff_profile_template.html", {"staff": staff, "id": staff_id})


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        contact_number = request.POST.get("contact_number")
        address = request.POST.get("address")
        qualification = request.POST.get("qualification")

        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.get(id=staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.contact_number = contact_number
            staff_model.profile_pic = profile_pic_url
            staff_model.qualification = qualification
            staff_model.save()

            messages.success(request, "Staff Updated Successfully")
            return HttpResponseRedirect(reverse("edit_staff_profile", kwargs={"staff_id": staff_id}))
        except:
            messages.error(request, "Failed to Update")
            return HttpResponseRedirect(reverse("edit_staff_profile", kwargs={"staff_id": staff_id}))


def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        student_id = request.POST.get("student_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        unique_id = request.POST.get("unique_id")
        username = request.POST.get("username")
        contact_number_primary = request.POST.get("contact_number_primary")
        contact_number_parents = request.POST.get("contact_number_parents")
        contact_number_whatsapp = request.POST.get("contact_number_whatsapp")
        contact_number_relative = request.POST.get("contact_number_relative")
        address1 = request.POST.get("address1")
        address2 = request.POST.get("address2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        father_name = request.POST.get("father_name")
        mother_name = request.POST.get("mother_name")
        session_year_id = request.POST.get("session")
        admission_date = request.POST.get("admission_date")
        hostel_id = request.POST.get("hostel")
        room_number = request.POST.get("room_number")
        locker_number = request.POST.get("locker_number")
        course_id = request.POST.get("course")
        last_school = request.POST.get("last_school")
        religion = request.POST.get("religion")
        birth_date = request.POST.get("birth_date")
        birth_place = request.POST.get("birth_place")
        uid = request.POST.get("uid")
        gr_number = request.POST.get("gr_number")
        bank_balance = float(request.POST.get("bank_balance"))

        if request.FILES.get('profile_pic', False):
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        else:
            profile_pic_url = None

        try:
            user = CustomUser.objects.get(id=student_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            student_model = Students.objects.get(admin=student_id)
            student_model.address1 = address1
            student_model.address2 = address2
            student_model.city = city
            student_model.state = state
            student_model.unique_id = unique_id
            student_model.pincode = pincode
            student_model.contact_number_primary = contact_number_primary
            student_model.contact_number_whatsapp = contact_number_whatsapp
            student_model.contact_number_relative = contact_number_relative
            student_model.father_name = father_name
            student_model.mother_name = mother_name
            student_model.gr_number = gr_number
            student_model.religion = religion
            student_model.birth_date = birth_date
            student_model.birth_place = birth_place
            if profile_pic_url != None:
                student_model.profile_pic = profile_pic_url
            session = SessionYearModel.objects.get(id=session_year_id)
            student_model.session_year_id = session
            student_model.admission_date = admission_date
            student_model.uid = uid
            hostel = Hostel.objects.get(id=hostel_id)
            student_model.hostel_id = hostel
            student_model.room_number = room_number
            student_model.locker_number = locker_number
            student_model.last_school = last_school
            course = Courses.objects.get(id=course_id)
            student_model.course_id = course
            student_model.course = course
            student_model.bank_balance = bank_balance
            student_model.contact_number_parents = contact_number_parents
            student_model.save()

            messages.success(request, "Student Updated Successfully")
            return HttpResponseRedirect(reverse("edit_student_profile", kwargs={"student_id": student_id}))
        except:
            messages.error(request, "Failed to Update Student")
            return HttpResponseRedirect(reverse("edit_student_profile", kwargs={"student_id": student_id}))


def manage_courses(request):
    courses = Courses.objects.all()
    return render(request, "hod_template/manage_course_template.html", {"courses": courses})


def edit_course(request, course_id):
    courses = Courses.objects.get(id=course_id)
    return render(request, "hod_template/edit_course_template.html", {"courses": courses, "id": course_id})


def edit_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course_name")

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, "Standard Updated Successfully")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id": course_id}))
        except:
            messages.error(request, "Failed to Update Standard")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id": course_id}))


def manage_subjects(request):
    subjects = Subjects.objects.all()
    return render(request, "hod_template/manage_subject_template.html", {"subjects": subjects})


def edit_subjects(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, "hod_template/edit_subject_template.html", {"subject": subject, "id": subject_id,
                                                                       "courses": courses, "staffs": staffs})


def edit_subject_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        course_id = request.POST.get("course")
        staff_id = request.POST.get("staff")

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course = Courses.objects.get(id=course_id)
            subject.course_id = course
            subject.save()
            messages.success(request, "Subject Updated Successfully")
            return HttpResponseRedirect("/edit_subjects/" + subject_id)
        except:
            messages.error(request, "Failed to Update Subject")
            return HttpResponseRedirect("/edit_subjects/" + subject_id)


def manage_hostel(request):
    hostels = Hostel.objects.all()
    return render(request, "hod_template/manage_hostel_template.html", {"hostels": hostels})


def edit_hostel(request, hostel_id):
    hostels = Hostel.objects.get(id=hostel_id)
    return render(request, "hod_template/edit_hostel_template.html", {"hostels": hostels, "id": hostel_id})


def edit_hostel_save(request):
    hostel_id = request.POST.get("hostel_id")
    hostel_name = request.POST.get("name")
    rooms = request.POST.get("rooms")

    try:
        hostel = Hostel.objects.get(id=hostel_id)
        hostel.name = hostel_name
        hostel.rooms = rooms
        hostel.save()
        messages.success(request, "Hostel Updated Successfully")
        return HttpResponseRedirect("/edit_hostel/" + hostel_id)
    except:
        messages.error(request, "Failed to Update Hostel")
        return HttpResponseRedirect("/edit_hostel/" + hostel_id)


def add_item_inventory(request):
    return render(request, "hod_template/add_item_retail_store.html")


def add_item_inventory_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        serial_number = request.POST.get("serial_number")
        item_name = request.POST.get("item_name")
        quantity = int(request.POST.get("quantity"))
        price = float(request.POST.get("price"))

    try:
        item = RetailStore(serial_number=serial_number, item_name=item_name, price=price, quantity=quantity)
        item.save()
        messages.success(request, "Item Added Successfully")
        return HttpResponseRedirect("/add_item_inventory")
    except:
        messages.error(request, "Failed to Add Item")
        return HttpResponseRedirect("/add_item_inventory")


def manage_inventory(request):
    items = RetailStore.objects.all()
    return render(request, "hod_template/manage_retail_store.html", {"items": items})


def shopping(request):
    serial = request.POST.get("serial_number")
    quantity = int(request.POST.get("quantity"))
    stemp = ShoppingTemp.objects.all()
    retails = RetailStore.objects.filter(serial_number=serial)
    #total = (quantity * int(retails.price))
    try:
        stemp.item_name = retails.item_name
        stemp.serial = serial
        stemp.qty = quantity
        stemp.price = retails.price
        stemp.save()
        return render(request, "hod_template/shopping_template.html", {"retails": retails, "quantity": quantity, "stemp":stemp})
    except:
        return render(request, "hod_template/shopping_template.html",
                      {"retails": retails, "quantity": quantity, "stemp": stemp})


def add_student_bill(request):
    student_from_form = request.POST.get("student_number_form")
    return render(request, "hod_template/shopping_template.html", {"student_from_form": student_from_form})


def manage_session(request):
    return render(request, "hod_template/manage_session_template.html")


def view_session(request):
    sessions = SessionYearModel.objects.all()
    return render(request, "hod_template/view_session.html", {"sessions": sessions})


def delete_session(request, session_year_id):
    session_data = SessionYearModel.objects.get(id=session_year_id)
    session_data.delete()
    return HttpResponseRedirect(reverse("view_session"))


def add_session_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")

        try:
            sessionyear = SessionYearModel(session_start_year=session_start_year, session_end_year=session_end_year)
            sessionyear.save()
            messages.success(request, "Session Added Successfully")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


def student_feedback_message(request):
    feedbacks = FeedbackStudent.objects.all()
    return render(request, "hod_template/student_feedback_template.html", {"feedbacks": feedbacks})


@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:
        feedback = FeedbackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_feedback_message(request):
    feedbacks = FeedbackStaff.objects.all()
    return render(request, "hod_template/staff_feedback_template.html", {"feedbacks": feedbacks})


@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:
        feedback = FeedbackStaff.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def student_leave_view(request):
    leaves = LeaveReportStudent.objects.all()
    return render(request, "hod_template/student_leave_view.html", {"leaves": leaves})


def student_approve_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def student_reject_leave(request, leave_id):
    leave = LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view"))


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    return render(request, "hod_template/staff_leave_view.html", {"leaves": leaves})


def staff_approve_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def staff_reject_leave(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("staff_leave_view"))


def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_year_id = SessionYearModel.objects.all()
    return render(request, "hod_template/admin_view_attendance.html", {"subjects": subjects, "session_year_id": session_year_id})


@csrf_exempt
def admin_get_attendance_dates(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.objects.get(id=session_year_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj, session_year_id=session_year_obj)
    attendance_obj = []

    for attendance_single in attendance:
        data = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                "session_year_id": attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)

    list_data = []
    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id, "name": student.student_id.admin.first_name + " " +
                                                                 student.student_id.admin.last_name,
                      "status": student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "hod_template/admin_profile.html", {"user": user})


def edit_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.save()
            messages.success(request, "Profile Saved Successfully")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Save Profile")
            return HttpResponseRedirect(reverse("admin_profile"))


def send_notification_staff(request):
    staff_notification = NotificationStaff.objects.all()
    return render(request, "hod_template/send_notification_staff.html", {"staff_notification": staff_notification})


def send_notification_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed!")
    else:
        notification_msg = request.POST.get("message")
        try:
            notification_staff = NotificationStaff(message=notification_msg)
            notification_staff.save()
            messages.success(request, "Notification Sent Successfully")
            return HttpResponseRedirect(reverse("send_notification_staff"))
        except:
            messages.error(request, "Failed to Send Notification")
            return HttpResponseRedirect(reverse("send_notification_staff"))


def delete_notification_staff(request, notification_id):
    try:
        notification_data = NotificationStaff.objects.get(id=notification_id)
        notification_data.delete()
        messages.success(request, "Notification Deleted Successfully")
        return HttpResponseRedirect(reverse("send_notification_staff"))
    except:
        messages.error(request, "Failed to Delete Notification")
        return HttpResponseRedirect(reverse("send_notification_staff"))


def send_notification_student(request):
    student_notification = NotificationStudent.objects.all()
    return render(request, "hod_template/send_notification_student.html", {"student_notification": student_notification})


def send_notification_student_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed!")
    else:
        notification_msg = request.POST.get("message")
        try:
            notification_student = NotificationStudent(message=notification_msg)
            notification_student.save()
            messages.success(request, "Notification Sent Successfully")
            return HttpResponseRedirect(reverse("send_notification_student"))
        except:
            messages.error(request, "Failed to Send Notification")
            return HttpResponseRedirect(reverse("send_notification_student"))


def delete_notification_student(request, notification_id):
    try:
        notification_data = NotificationStudent.objects.get(id=notification_id)
        notification_data.delete()
        messages.success(request, "Notification Deleted Successfully")
        return HttpResponseRedirect(reverse("send_notification_student"))
    except:
        messages.error(request, "Failed to Delete Notification")
        return HttpResponseRedirect(reverse("send_notification_student"))


def generate_bonafide_certi(request, student_id):
    num2words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', \
                 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', \
                 11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', \
                 15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', \
                 19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', \
                 50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', \
                 90: 'Ninety', 0:''}
    month2words = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                   7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    student = Students.objects.get(admin=student_id)
    b_date = student.birth_date
    updated_b_day = datetime.strptime(b_date, "%Y-%m-%d")
    formatted_bday = datetime.strftime(updated_b_day, "%d-%m-%Y")
    b_day_word = num2words[updated_b_day.day-updated_b_day.day % 10] + num2words[updated_b_day.day % 10].lower()
    b_month_word = month2words[updated_b_day.month].lower()
    inf_engine = inflect.engine()
    b_year_word = inf_engine.number_to_words(updated_b_day.year)
    return render(request, "hod_template/bonafide_certi.html", {"student": student, "id": student_id,
                                                                "bday": formatted_bday, "b_day_word": b_day_word,
                                                                "b_month_word": b_month_word, "b_year_word": b_year_word})


def generate_leaving_certi(request, student_id):
    num2words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', \
                 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', \
                 11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', \
                 15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', \
                 19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', \
                 50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', \
                 90: 'Ninety', 0: ''}
    month2words = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                   7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    student = Students.objects.get(admin=student_id)
    b_date = student.birth_date
    admission_date = student.admission_date
    updated_admission_date = datetime.strptime(admission_date, "%Y-%m-%d")
    formatted_admission_date = datetime.strftime(updated_admission_date, "%d-%m-%Y")
    updated_b_day = datetime.strptime(b_date, "%Y-%m-%d")
    formatted_bday = datetime.strftime(updated_b_day, "%d-%m-%Y")
    b_day_word = num2words[updated_b_day.day - updated_b_day.day % 10] + num2words[updated_b_day.day % 10].title()
    b_month_word = month2words[updated_b_day.month].title()
    inf_engine = inflect.engine()
    b_year_word = inf_engine.number_to_words(updated_b_day.year).title()
    return render(request, "hod_template/leaving_certi.html", {"student": student, "id": student_id,
                                                                "bday": formatted_bday, "b_day_word": b_day_word,
                                                                "b_month_word": b_month_word, "b_year_word": b_year_word,
                                                               "final_admission_date": formatted_admission_date})


def add_transport_route(request):
    return render(request, "hod_template/add_transport_route_template.html")


def add_transport_route_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        route_number = request.POST.get("route_number")
        city_name = request.POST.get("city_name")
        departure_date = request.POST.get("departure_date")
        departure_time = request.POST.get("departure_time")
        arrival_date = request.POST.get("arrival_date")
        arrival_time = request.POST.get("arrival_time")
        remark = request.POST.get("remark")

        try:
            route_info = TransportAddRoute()
            route_info.root_number = route_number
            route_info.city_name = city_name
            route_info.departure_date = departure_date
            route_info.departure_time = departure_time
            route_info.arrival_date = arrival_date
            route_info.arrival_time = arrival_time
            route_info.remark = remark
            route_info.save()
            messages.success(request, "Route Added Successfully")
            return HttpResponseRedirect(reverse("add_transport_route"))
        except:
            messages.error(request, "Failed to Add Route")
            return HttpResponseRedirect(reverse("add_transport_route"))


def view_added_routes(request):
    routes = TransportAddRoute.objects.all()
    return render(request, "hod_template/admin_view_added_routes.html", {"routes": routes})


def fees_management(request):
    pass



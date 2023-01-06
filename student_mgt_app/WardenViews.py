from django.shortcuts import render

from student_mgt_app.models import *


def warden_home(request):
    student_count = Students.objects.all().count()
    hostel_count = Hostel.objects.all().count()
    hostel_room_count = HostelRoom.objects.all().count()
    warden = Warden.objects.get(admin=request.user.id)

    return render(request, "warden_template/warden_home_template.html", {"warden": warden})

from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from LEC_RMSapp.models import Course, Session_year, Student, Staff, Subject,Year_Part, Staff_Notification, Staff_Feedback, Student_Notification,Student_Feedback,StudentResult,Regular_board_exam,Back_board_exam
from django.contrib import messages
from LEC_RMSapp.models import CustomUser


@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    staff_count  = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count =  Subject.objects.all().count()

    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()

    context = {
        'student_count':student_count,
        'staff_count':staff_count,
        'course_count':course_count,
        'subject_count':subject_count,
        'student_gender_male':student_gender_male,
        'student_gender_female':student_gender_female,
    }
    return render(request,'Hod/home.html',context)

@login_required(login_url='/')
def ADD_STUDENT(request):
    course = Course.objects.all()
    session_year = Session_year.objects.all()

    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id = request.POST.get('id')
        RollNo = request.POST.get('RollNo')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        mobile_number= request.POST.get('mobile_number')

        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_number = request.POST.get('father_number')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_number = request.POST.get('mother_number')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        if CustomUser.objects.filter(email=email).exists():
           messages.warning(request, 'Email Is Already Taken')
           return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
           messages.warning(request, 'Username Is Already Taken')
           return redirect('add_student')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                profile_pic=profile_pic,
                user_type=3
            )
            user.set_password(password)
            user.save()

            course = Course.objects.get(id = course_id)
            session_year = Session_year.objects.get(id = session_year_id)

            student = Student(
                admin=user,
                id=id,
                RollNo=RollNo,
                dob=dob,
                mobile_number=mobile_number,
                gender=gender,
                session_year_id=session_year,
                course_id=course,
                father_name=father_name,
                father_occupation=father_occupation,
                father_number=father_number,
                mother_name=mother_name,
                mother_occupation=mother_occupation,
                mother_number=mother_number,
                present_address=present_address,
                permanent_address=permanent_address,
            )
            student.save()
            messages.success(request, user.first_name + "  " + user.last_name + " Is Successfully Added !")
            return redirect('add_student')

    context = {
        'course': course,
        'session_year': session_year,
    }
    return render(request, 'Hod/add_student.html', context)

@login_required(login_url='/')
def VIEW_STUDENT(request):
    student = Student.objects.all()

    context ={
        'student':student,
    }
    return render(request,'Hod/view_student.html',context)

@login_required(login_url='/')
def EDIT_STUDENT(request,id):
    student = Student.objects.filter(id = id)
    course = Course.objects.all()
    session_year = Session_year.objects.all()

    context = {
        'student': student,
        'course': course,
        'session_year':session_year,

    }
    return render(request,'Hod/edit_student.html',context)

@login_required(login_url='/')
def UPDATE_STUDENT(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id = request.POST.get('id')
        RollNo = request.POST.get('RollNo')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        mobile_number = request.POST.get('mobile_number')

        father_name = request.POST.get('father_name')
        father_occupation = request.POST.get('father_occupation')
        father_number = request.POST.get('father_number')
        mother_name = request.POST.get('mother_name')
        mother_occupation = request.POST.get('mother_occupation')
        mother_number = request.POST.get('mother_number')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        user = CustomUser.objects.get(id = id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username

        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic

        user.save()
        student = Student.objects.get(admin = id)
        student.RollNo = RollNo
        student.gender = gender
        student.dob = dob
        student.mobile_number= mobile_number
        student.father_name= father_name
        student.father_occupation= father_occupation
        student.father_number= father_number
        student.mother_name= mother_name
        student.mother_occupation= mother_occupation
        student.mother_number= mother_number
        student.present_address= present_address
        student.permanent_address= permanent_address

        course = Course.objects.get(id = course_id)
        student.course_id = course

        session_year = Session_year.objects.get(id = session_year_id)
        student.session_year_id = session_year
        student.save()
        messages.success(request,'Record Are Successfully Updated !')
        return redirect('view_student')

    return render(request,'Hod/edit_student.html')

@login_required(login_url='/')
def DELETE_STUDENT(request,admin):
    student = CustomUser.objects.get(id=admin)
    student.delete()
    messages.success(request,'Record Are Successfully Deleted!')
    return redirect('view_student')

@login_required(login_url='/')
def ADD_COURSE(request):
    if request.method == "POST":
        course_name = request.POST.get('course_name')

        course = Course(
            name= course_name,
        )
        course.save()
        messages.success(request,'Course Are Successfully Created')
        return redirect('add_course')
    return render(request,'Hod/add_course.html')

@login_required(login_url='/')
def VIEW_COURSE(request):
    course = Course.objects.all()
    context = {
        'course':course,
    }
    return render(request,'Hod/view_course.html',context)

@login_required(login_url='/')
def EDIT_COURSE(request,id):
    course = Course.objects.get(id = id)

    context = {
        'course':course,
    }
    return render(request,'Hod/edit_course.html',context)

@login_required(login_url='/')
def UPDATE_COURSE(request):
    if request.method == "POST":
        name = request.POST.get('name')
        course_id = request.POST.get('course_id')

        course = Course.objects.get(id = course_id)
        course.name = name
        course.save()
        messages.success(request,'Course Are Successfully Updated')
        return redirect('view_course')

    return render(request,'Hod/edit_course.html')

@login_required(login_url='/')
def DELETE_COURSE(request,id):
    course = Course.objects.get(id = id)
    course.delete()
    messages.success(request,'Course Are Successfully Deleted')
    return redirect('view_course')

@login_required(login_url='/')
def ADD_STAFF(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        id = request.POST.get('id')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        number = request.POST.get('number')
        address = request.POST.get('address')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request,'Email Is Already Taken!')
            return redirect('add_staff')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username Is Already Taken!')
            return redirect('add_staff')
        else:
            user = CustomUser(username =username,first_name =first_name,last_name = last_name, email= email, profile_pic=profile_pic, user_type=2)
            user.set_password(password)
            user.save()
            staff = Staff(
                admin=user,
                address=address,
                gender = gender, number=number, dob = dob,
                id = id,
            )
            staff.save()
            messages.success(request,'Staff Are Successfully Added!')
            return redirect('add_staff')

    return render(request,'Hod/add_staff.html')

@login_required(login_url='/')
def VIEW_STAFF(request):
    staff = Staff.objects.all()
    context = {
        'staff':staff,
    }
    return render(request,'Hod/view_staff.html',context)

@login_required(login_url='/')
def EDIT_STAFF(request,id):
    staff = Staff.objects.get(id = id)

    context = {
        'staff':staff,
    }
    return render(request,'Hod/edit_staff.html',context)

@login_required(login_url='/')
def UPDATE_STAFF(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        staff_id = request.POST.get('staff_id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        number = request.POST.get('number')
        address = request.POST.get('address')

        user= CustomUser.objects.get(id = staff_id)
        user.username = username
        user.first_name = first_name
        user.last_name= last_name
        user.email= email
        if password != None and password != "":
            user.set_password(password)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.save()
        staff = Staff.objects.get(admin = staff_id)
        staff.gender = gender
        staff.address = address
        staff.dob = dob
        staff.number = number

        staff.save()
        messages.success(request,'Faculty Is Successfully Updated')
        return redirect('view_staff')

    return render(request,'Hod/edit_staff.html')

@login_required(login_url='/')
def DELETE_STAFF(request,admin):
    staff = CustomUser.objects.get(id = admin)
    staff.delete()
    messages.success(request,'Record Are Successfully Deleted ! ')
    return redirect('view_staff')

@login_required(login_url='/')
def ADD_SUBECT(request):
    course = Course.objects.all()
    session_year = Session_year.objects.all()
    staff = Staff.objects.all()

    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')
        session_year_id = request.POST.get('session_year_id')
        semester = request.POST.get('semester')

        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)
        session_year = Session_year.objects.get(id = session_year_id)
        subject = Subject(
            name = subject_name,
            course = course,
            staff = staff,
            session_year = session_year,
            semester = semester,
        )
        subject.save()
        messages.success(request,'Subjects Are Successfully Added !')
        return redirect('add_subject')

    context={
        'course':course,
        'staff':staff,
        'session_year':session_year,
    }
    return render(request,'Hod/add_subject.html',context)

@login_required(login_url='/')
def VIEW_SUBJECT(request):
    subject = Subject.objects.all().order_by('-id')[0:10]

    context = {
        'subject':subject,
    }
    return render(request,'Hod/view_subject.html',context)

@login_required(login_url='/')
def EDIT_SUBJECT(request, id):
    subject = Subject.objects.get(id = id)
    course = Course.objects.all()
    staff = Staff.objects.all()
    session_year = Session_year.objects.all()

    context = {
        'subject': subject,
        'course':course,
        'staff':staff,
        'session_year':session_year,
    }
    return render(request,'Hod/edit_subject.html',context)

@login_required(login_url='/')
def UPDATE_SUBJECT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')
        session_year_id = request.POST.get('session_year_id')
        semester = request.POST.get('semester')

        course = Course.objects.get(id = course_id)
        staff = Staff.objects.get(id = staff_id)
        session_year = Session_year.objects.get(id = session_year_id)
        subject = Subject(
            id = subject_id,
            name = subject_name,
            course = course,
            staff = staff,
            session_year = session_year,
            semester = semester,
        )
        subject.save()
        messages.success(request,'Subject Are Successfully Updated !')
        return redirect('view_subject')

@login_required(login_url='/')
def DELETE_SUBJECT(request,id):
    subject = Subject.objects.filter(id=id)
    subject.delete()
    messages.success(request,'Subjects Are Successfully Deleted!')
    return redirect('view_subject')

@login_required(login_url='/')
def ADD_SESSION(request):
    if request.method == "POST":
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_year(
            session_start = session_year_start,
            session_end = session_year_end,
        )
        session.save()
        messages.success(request,'Session Are Successfully Created')
        return redirect('add_session')
    return render(request,'Hod/add_session.html')

@login_required(login_url='/')
def VIEW_SESSION(request):
    session = Session_year.objects.all()


    context = {
        'session':session,
    }
    return render(request,'Hod/view_session.html',context)

@login_required(login_url='/')
def EDIT_SESSION(request,id):
    session = Session_year.objects.filter(id = id)

    context = {
        'session':session,
    }
    return render (request,'Hod/edit_session.html',context)

@login_required(login_url='/')
def UPDATE_SESSION(request):
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_year(
            id = session_id,
            session_start = session_year_start,
            session_end = session_year_end,
        )
        session.save()
        messages.success(request,'Session Are Successfully Updated !')
        return redirect('view_session')

@login_required(login_url='/')
def DELETE_SESSION(request,id):
    session = Session_year.objects.get(id = id)
    session.delete()
    messages.success(request,'Session IS Successfully Deleted !')
    return redirect('view_session')

@login_required(login_url='/')
def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')[0:5]

    context = {
        'staff':staff,
        'see_notification': see_notification,
    }
    return render(request,'Hod/staff_notification.html',context)

@login_required(login_url='/')
def SAVE_STAFF_NOTIFICATION(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')

        staff = Staff.objects.get(admin = staff_id)
        notification = Staff_Notification(
            staff_id = staff,
            message = message,
        )
        notification.save()
        messages.success(request,'Notification Are Successfully Send')
        return redirect('staff_send_notification')

@login_required(login_url='/')
def STAFF_FEEDBACK(request):
    feedback = Staff_Feedback.objects.all()
    feedback_history = Staff_Feedback.objects.all().order_by('-id')[0:5]

    context = {
        'feedback':feedback,
        'feedback_history':feedback_history,
    }
    return render(request,'Hod/staff_feedback.html',context)

@login_required(login_url='/')
def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Staff_Feedback.objects.get(id = feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()

        return redirect('staff_feedback_reply')

    return None

@login_required(login_url='/')
def STUDENT_FEEDBACK(request):
    feedback = Student_Feedback.objects.all()
    feedback_history = Student_Feedback.objects.all().order_by('-id')[0:5]

    context = {
        'feedback':feedback,
        'feedback_history':feedback_history,
    }
    return render(request,'Hod/student_feedback.html',context)

@login_required(login_url='/')
def REPLY_STUDENT_FEEDBACK(request):
    if request.method == "POST":
        feedback_id= request.POST.get('feedback_id')
        feedback_reply = request.POST.get ('feedback_reply')

        feedback = Student_Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()
        return redirect('get_student_feedback')

@login_required(login_url='/')
def STUDENT_SEND_NOTIFICATION(request):
    student = Student.objects.all()
    notification = Student_Notification.objects.all()
    context = {
        'student':student,
        'notification':notification,
    }
    return render(request,'Hod/student_notification.html',context)

@login_required(login_url='/')
def SAVE_STUDENT_NOTIFICATION(request):
    if request.method == "POST":
        message = request.POST.get('message')
        student_id = request.POST.get('student_id')

        student = Student.objects.get(admin = student_id)
        stud_notification = Student_Notification(
            student_id = student,
            message = message,
        )
        stud_notification.save()
        messages.success(request,'Student Notification Are Successfully Sent')
        return redirect('student_send_notification')


def STUDENT_DETAILS(request,id):
    student = Student.objects.filter(id = id)
    context = {
        'student': student,
        #'course':course,
    }
    return render(request,'Hod/student_details.html',context)


def STAFF_DETAILS(request,id):
    staff = Staff.objects.filter(id=id)
    context = {
        'staff': staff,
    }
    return render(request,'Hod/staff_details.html',context)


##  REGULAR BOARD RESULT ##
@login_required(login_url='/')
def add_regular_board_result(request):
    courses = Course.objects.all()
    session_years = Session_year.objects.all()
    year_part = Year_Part.objects.all()
    action = request.GET.get('action')
    
    get_course = None
    get_session_year = None
    get_year_part = None
    students = None
    if action is not None:
        if request.method == "POST":
           
            course_id = request.POST.get('course_id')
            session_year = request.POST.get('session_year')
            year_part = request.POST.get('year_part')

            
            get_course = Course.objects.get(id=course_id)
            get_session_year = Session_year.objects.get(id=session_year)
            get_year_part = Year_Part.objects.get(id=year_part)

            course = Course.objects.filter(id=course_id)
            
            for i in course:
                student_id = i.id
                students = Student.objects.filter(course_id = student_id,session_year_id = get_session_year)
    context = {
        "courses": courses,
        "session_years": session_years,
        "year_part":year_part,
        "get_course":get_course,
        "get_session_year":get_session_year,
        "get_year_part":get_year_part,
        'action':action,
        "students":students,
    }
    return render(request, "Hod/add_regular_board_result.html", context)


def regular_board_result_save(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year')
        student_id = request.POST.get('student_id')
        exam_held_date = request.POST.get('exam_held_date')
        year_part = request.POST.get('year_part')
        marksheet = request.FILES.get('marksheet')
        result = request.POST.get('result')
        obtained_marks= request.POST.get('obtained_marks')
        full_marks = request.POST.get('full_marks')

        get_student = Student.objects.get(admin=student_id)
        get_course = Course.objects.get(id=course_id)
        get_session_year = Session_year.objects.get(id=session_year_id)
        get_year_part = Year_Part.objects.get(id=year_part)
        # Check if Students Result Already Exists or not
        check_exists = Regular_board_exam.objects.filter(course=get_course, session_year=get_session_year,student_id=get_student,year_part=get_year_part).exists()
        if check_exists:
            regular_result = Regular_board_exam.objects.get(course=get_course, session_year=get_session_year,student_id=get_student,year_part=get_year_part)
            regular_result.exam_held_date = exam_held_date,
            regular_result.marksheet = marksheet,
            regular_result.obtained_marks = obtained_marks,
            regular_result.full_marks = full_marks,
            regular_result.result = result,
            regular_result.save()
            messages.success(request,'Result updated succesfully!')
            return redirect('add_regular_board_result')
        else:
            regular_result = Regular_board_exam(
                course=get_course,
                session_year=get_session_year,
                year_part=get_year_part,
                student_id=get_student,
                exam_held_date=exam_held_date,
                marksheet=marksheet,
                result=result,
                full_marks = full_marks,
                obtained_marks = obtained_marks,

            )
        regular_result.save()
        messages.success(request, 'Result added succesfully!')
        return redirect('add_regular_board_result')


def view_regular_board_result(request):
    courses = Course.objects.all()
    session_years = Session_year.objects.all()
    year_parts = Year_Part.objects.all()
    
    action = request.GET.get('action')
    get_course = None
    get_session_year = None
    get_year_part = None
    regular_result = None
    if action is not None:
        if request.method == "POST":
            courses = request.POST.get('courses')
            session_years = request.POST.get('session_years')
            year_part = request.POST.get('year_part')
            
            get_course = Course.objects.get(id=courses)
            get_session_year = Session_year.objects.get(id=session_years)
            get_year_part = Year_Part.objects.get(id=year_part)
            regular_result = Regular_board_exam.objects.filter(course=get_course,session_year=get_session_year,year_part=get_year_part)
    context = {
        'courses':courses,
        'session_years':session_years,
        'year_parts':year_parts,
        'action':action,
        'get_course':get_course,
        'get_session_year':get_session_year,
        'get_year_part':get_year_part,
        'regular_result':regular_result,
    }
    return render(request,'Hod/view_regular_board_result.html',context)


@login_required(login_url='/')
def edit_regular_board_result(request, id):
    regular_board_exam = Regular_board_exam.objects.get(id = id)
    course = Course.objects.get(id = regular_board_exam.course.id)
    session_year = Session_year.objects.get(id = regular_board_exam.session_year.id)
    student = Student.objects.get(id = regular_board_exam.student_id.id)
    year_part = Year_Part.objects.get(id = regular_board_exam.year_part.id)
    context = {
        'regular_board_exam':regular_board_exam,
        'course':course,
        'session_year':session_year,
        'year_part':year_part,
        'student':student
        
    }
    return render(request,'Hod/edit_regular_board_result.html',context)


def update_regular_board_result(request):
    if request.method == "POST":
        id = request.POST.get('id')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        exam_held_date = request.POST.get('exam_held_date')
        year_part_id = request.POST.get('year_part_id')
        marksheet = request.FILES.get('marksheet')
        result = request.POST.get('result')
        full_marks = request.POST.get('full_marks')
        obtained_marks = request.POST.get('obtained_marks')

        course = Course.objects.get(id=course_id)
        session_year = Session_year.objects.get(id=session_year_id)
        year_part = Year_Part.objects.get(id=year_part_id)
        student_id = Student.objects.get(id=student_id)

        regular_result = Regular_board_exam(
            id=id,
            course=course,
            session_year=session_year,
            student_id=student_id,
            exam_held_date=exam_held_date,
            year_part=year_part,
            marksheet=marksheet,
            result=result,
            obtained_marks = obtained_marks,
            full_marks = full_marks,
        )
        regular_result.save()
        messages.success(request, 'Results Are Successfully Updated !')
        return redirect('view_regular_board_result')


def delete_regular_board_result(request, id):
    regular_board_exam = Regular_board_exam.objects.filter(id=id)
    regular_board_exam.delete()
    messages.success(request, 'Results Are Successfully Deleted!')
    return redirect('view_regular_board_result')


## BACK BOARD RESULT ##
@login_required(login_url='/')
def add_back_board_result(request):
    courses = Course.objects.all()
    session_years = Session_year.objects.all()
    year_part = Year_Part.objects.all()
    action = request.GET.get('action')
    
    get_course = None
    get_session_year = None
    get_year_part = None
    students = None
    if action is not None:
        if request.method == "POST":
            year_part = request.POST.get('year_part')
            course_id = request.POST.get('course_id')
            session_year = request.POST.get('session_year')

            get_year_part = Year_Part.objects.get(id=year_part)
            get_course = Course.objects.get(id=course_id)
            get_session_year = Session_year.objects.get(id=session_year)

            regular_result = Regular_board_exam.objects.filter(year_part=year_part,course=course_id,result='fail')
            
            for i in regular_result:
                student_id = i.course.id
                students = Student.objects.filter(course_id = student_id,session_year_id = get_session_year)
    context = {
        "courses": courses,
        "session_years": session_years,
        "year_part":year_part,
        "get_course":get_course,
        "get_session_year":get_session_year,
        "get_year_part":get_year_part,
        'action':action,
        "students":students,
    }
    return render(request, "Hod/add_back_board_result.html", context)


def back_board_result_save(request):
    if request.method == "POST":
        course_id = request.POST.get('course_id')
        year_part = request.POST.get('year_part')
        session_year_id = request.POST.get('session_year')
        student_id = request.POST.get('student_id')
        exam_held_date = request.POST.get('exam_held_date')
        marksheet = request.FILES.get('marksheet')
        b_result = request.POST.get('b_result')
        full_marks = request.POST.get('full_marks')
        obtained_marks = request.POST.get('obtained_marks')


        get_student = Student.objects.get(admin=student_id)
        get_course = Course.objects.get(id=course_id)
        get_session_year = Session_year.objects.get(id=session_year_id)
        get_year_part=Year_Part.objects.get(id=year_part)
        # Check if Students Result Already Exists or not
        check_exists = Back_board_exam.objects.filter(course=get_course,student_id=get_student,session_year=get_session_year,year_part=get_year_part,).exists()
        if check_exists:
            back_result = Back_board_exam.objects.get(course=get_course, session_year=get_session_year,
                                                      student_id=get_student,year_part=get_year_part)
            back_result.exam_held_date = exam_held_date,
            back_result.marksheet = marksheet,
            back_result.b_result = b_result,
            back_result.full_marks= full_marks,
            back_result.obtained_marks = obtained_marks,
            back_result.save()
            messages.success(request, 'Result updated succesfully!')
            return redirect('add_back_board_result')
        else:
            back_result = Back_board_exam(
                course=get_course,
                session_year=get_session_year,
                year_part = get_year_part,
                student_id=get_student,
                exam_held_date=exam_held_date,
                marksheet=marksheet,
                b_result=b_result,
                full_marks = full_marks,
                obtained_marks =obtained_marks,
            )
        back_result.save()
        messages.success(request, 'Result added succesfully!')
        return redirect('add_back_board_result')


def view_back_board_result(request):
    year_part = Year_Part.objects.all()
    courses = Course.objects.all()
    session_years = Session_year.objects.all()
    
    action = request.GET.get('action')
    get_course = None
    get_session_year = None
    get_year_part = None
    back_result = None
    if action is not None:
        if request.method == "POST":
            courses = request.POST.get('courses')
            session_years = request.POST.get('session_years')
            year_part = request.POST.get('year_part')
            
            get_course = Course.objects.get(id=courses)
            get_session_year = Session_year.objects.get(id=session_years)
            get_year_part = Year_Part.objects.get(id=year_part)
            back_result = Back_board_exam.objects.filter(course=get_course,year_part=get_year_part,session_year = get_session_year)
    context = {
        'courses':courses,
        'session_years':session_years,
        'year_part':year_part,
        'action':action,
        'get_course':get_course,
        'get_session_year':get_session_year,
        'get_year_part':get_year_part,
        'back_result':back_result,
    }
    return render(request,'Hod/view_back_board_result.html',context)


@login_required(login_url='/')
def edit_back_board_result(request, id):
    back_board_exam = Back_board_exam.objects.get(id=id)
    course = Course.objects.get(id=back_board_exam.course.id)
    session_year = Session_year.objects.get(id=back_board_exam.session_year.id)
    student_id = Student.objects.get(id=back_board_exam.student_id.id)
    year_part = Year_Part.objects.get(id = back_board_exam.year_part.id)

    context = {
        'back_board_exam': back_board_exam,
        'course': course,
        'session_year': session_year,
        'student_id': student_id,
        'year_part':year_part,

    }
    return render(request, 'Hod/edit_back_board_result.html', context)


def update_back_board_result(request):
    if request.method == "POST":
        id = request.POST.get('id')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        year_part_id = request.POST.get('year_part_id')
        student_id = request.POST.get('student_id')
        exam_held_date = request.POST.get('exam_held_date')
        marksheet = request.FILES.get('marksheet')
        b_result = request.POST.get('b_result')
        full_marks = request.POST.get('full_marks')
        obtained_marks = request.POST.get('obtained_marks')

        course = Course.objects.get(id=course_id)
        session_year = Session_year.objects.get(id=session_year_id)
        student_id = Student.objects.get(id=student_id)
        year_part = Year_Part.objects.get(id=year_part_id)


        back_result = Back_board_exam(
            id=id,
            course=course,
            session_year=session_year,
            student_id=student_id,
            exam_held_date=exam_held_date,
            year_part=year_part,
            marksheet=marksheet,
            b_result=b_result,
            obtained_marks = obtained_marks,
            full_marks = full_marks,
        )
        back_result.save()
        messages.success(request, 'Results are successfully updated !')
        return redirect('view_back_board_result')

def delete_back_board_result(request,id):
    back_board_exam = Back_board_exam.objects.filter(id=id)
    back_board_exam.delete()
    messages.success(request,'Results are successfully deleted!')
    return redirect('view_back_board_result')




## INTERNAL MARK ##
@login_required(login_url='/')
def view_internal_mark(request):
    subjects = Subject.objects.all()
    session_years = Session_year.objects.all()

    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    internal_mark = None
    if action is not None:
        if request.method == "POST":
            subjects = request.POST.get('subjects')
            session_years = request.POST.get('session_years')

            get_subject = Subject.objects.get(id=subjects)
            get_session_year = Session_year.objects.get(id=session_years)
            internal_mark = StudentResult.objects.filter(subject_id=get_subject)
    context = {
        'subjects': subjects,
        'session_years': session_years,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'internal_mark': internal_mark,
    }
    return render(request, 'Hod/view_internal_mark.html', context)

@login_required(login_url='/')
def edit_internal_mark(request, id):
    internal_mark = StudentResult.objects.get(id=id)
    session_year = Session_year.objects.get(id=internal_mark.session_year_id.id)
    student_id = Student.objects.get(id=internal_mark.student_id.id)
    subject = Subject.objects.get(id=internal_mark.subject_id.id)

    context = {
        'internal_mark': internal_mark,
        'subject': subject,
        'session_year': session_year,
        'student_id': student_id,
    }
    return render(request, 'Hod/edit_internal_mark.html', context)


def update_internal_mark(request):
    if request.method == "POST":
        id = request.POST.get('id')
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_marks = request.POST.get('assignment_marks')
        exam_marks = request.POST.get('exam_marks')

        subject = Subject.objects.get(id=subject_id)
        session_year = Session_year.objects.get(id=session_year_id)
        student_id = Student.objects.get(id=student_id)


        internal_result = StudentResult(
            id=id,
            subject_id=subject,
            session_year_id=session_year,
            student_id=student_id,
            assignment_marks = assignment_marks,
            exam_marks = exam_marks,
        )
        internal_result.save()
        messages.success(request, 'Results is successfully updated !')
        return redirect('view_internal_mark')

def delete_internal_mark(request,id):
    internal_mark = StudentResult.objects.filter(id=id)
    internal_mark.delete()
    messages.success(request,'Result is successfully deleted!')
    return redirect('view_internal_mark')



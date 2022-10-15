from django.shortcuts import render,redirect,HttpResponse
from LEC_RMSapp.models import Staff,Student,Staff_Notification,Staff_Feedback,Subject,Session_year,StudentResult,Course,StudentReport,Internal_mark
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import math
from django.db.models.lookups import Transform

@login_required(login_url='/')
def HOME(request):
    # Fetching All Students under Staff

    staff = Staff.objects.get(admin = request.user.id)
    subjects = Subject.objects.filter(staff_id=staff)
    course_list = []
    for subject in subjects:
        courses = Course.objects.get(id=subject.course.id)
        course_list.append(courses.id)

    final_course = []
    result_count1 = None
    # Removing Duplicate Course Id
    for course in course_list:
        if course not in final_course:
            final_course.append(course)

    students_count = Student.objects.filter(course_id__in=final_course).count()
    subject_count = subjects.count()

    InternalResult_count = StudentResult.objects.filter(subject_id__in=subjects).count()
    subject_list = []
    internalresult_list = []
    for subject in subjects:
        result_count1 = StudentResult.objects.filter(subject_id=subject.id).count()

        subject_list.append(subject.name)
        internalresult_list.append(result_count1)

    students_internalresult = Student.objects.filter(course_id__in=final_course)
    #print(students_internalresult)
    student_list = []
    student_list_passed = []
    student_list_failed = []
    InternalResult_pass_count = StudentResult.objects.filter(exam_marks__range=(32, 80)).count()
  
    #print(InternalResult_pass_count)
    InternalResult_fail_count = StudentResult.objects.filter(exam_marks__range=(0, 31)).count()
    #print(InternalResult_fail_count)
    '''
        #for student in students_internalresult:
        #    InternalResult_pass_count = StudentResult.objects.filter(exam_marks__range=(0, 31), student_id=student.id).count()
        #    InternalResult_fail_count = StudentResult.objects.filter(exam_marks__range=(32, 80),student_id=student.id).count()
        #    print(InternalResult_pass_count)
    '''

    for student in students_internalresult:
        student_list.append(student.admin.first_name+" "+ student.admin.last_name)
    student_list_passed.append(InternalResult_pass_count)
    student_list_failed.append(InternalResult_fail_count)
    #print(student_list_passed)
    #print(student_list_failed)

    perc_list =[]
    cnt = StudentResult.objects.filter(exam_marks__range=(32, 80)).count()

    print(result_count1)

    if (InternalResult_count!=0):
        perc = (cnt * 100 / InternalResult_count)
    else:
        perc=(cnt*100/1)
    rounded_number = round(perc, 2)
    perc_list.append(rounded_number)


    #print(rounded_number)

    context = {
        "result_count1":result_count1,
        "rounded_number":rounded_number,
        "perc_list":perc_list,
        "students_count": students_count,
        "subject_count": subject_count,
        "InternalResult_count": InternalResult_count,
        "subject_list":subject_list,
        "internalresult_list": internalresult_list,
        "student_list": student_list,
        "InternalResult_pass_count":InternalResult_pass_count,
        "InternalResult_fail_count":InternalResult_fail_count,
        "student_list_passed":student_list_passed,
        "student_list_failed":student_list_failed,
    }
    return render(request,'Staff/home.html',context)

@login_required(login_url='/')
def NOTIFICATIONS(request):
    staff = Staff.objects.filter(admin = request.user.id)
    for i in staff:
        staff_id = i.id

        notification = Staff_Notification.objects.filter(staff_id = staff_id)

        context = {
            'notification':notification,
        }
        return render(request,'Staff/notification.html',context)

@login_required(login_url='/')
def STAFF_NOTIFICATION_MARK_AS_DONE(request,status):
    notification = Staff_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('notifications')


def STAFF_FEEDBACK(request):
    staff_id = Staff.objects.get(admin = request.user.id)

    feedback_history = Staff_Feedback.objects.filter(staff_id = staff_id)

    context = {
        'feedback_history':feedback_history,
    }
    return render(request,'Staff/feedback.html',context)


def STAFF_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')

        staff = Staff.objects.get(admin = request.user.id)
        feedback = Staff_Feedback(
            staff_id = staff,
            feedback = feedback,
            feedback_reply = "",
        )
        feedback.save()
        return redirect('staff_feedback')



def STAFF_ADD_RESULT(request):
    staff = Staff.objects.get(admin = request.user.id)

    subjects = Subject.objects.filter(staff_id = staff)
    session_year = Session_year.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session = None
    students = None
    if action is not None:
        if request.method == "POST":
           subject_id = request.POST.get('subject_id')
           session_year_id = request.POST.get('session_year_id')

           get_subject = Subject.objects.get(id = subject_id)
           get_session = Session_year.objects.get(id = session_year_id)

           subjects = Subject.objects.filter(id = subject_id)
           for i in subjects:
                subject_id = i.course.id
                students = Student.objects.filter(course_id = subject_id)

    context = {
        'subjects':subjects,
        'session_year':session_year,
        'action':action,
        'get_subject':get_subject,
        'get_session':get_session,
        'students':students,
    }
    return render(request,'Staff/add_internal_result.html',context)


def STAFF_SAVE_RESULT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        Exam_mark = request.POST.get('exam_mark')

        get_student = Student.objects.get(admin = student_id)
        get_subject = Subject.objects.get(id=subject_id)
        get_session = Session_year.objects.get(id = session_year_id )

        check_exist = StudentResult.objects.filter(subject_id=get_subject, student_id=get_student , session_year_id=get_session ).exists()
        if check_exist:
            result = StudentResult.objects.get(subject_id=get_subject, student_id=get_student, session_year_id=get_session)
            result.subject_assignment_marks = assignment_mark
            result.subject_exam_marks = Exam_mark
            result.save()
            messages.success(request, "Successfully Updated Result")
            return redirect('staff_view_internal_result')
        else:
            result = StudentResult(student_id=get_student, subject_id=get_subject, exam_marks=Exam_mark,
                                   assignment_marks=assignment_mark, session_year_id=get_session)
            result.save()
            messages.success(request, "Successfully Added Result")
            return redirect('staff_internal_result')


def STAFF_VIEW_INTERNALRESULT(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    subjects = Subject.objects.filter(staff_id=staff_id)
    session_years = Session_year.objects.all()

    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    internal_mark = None
    if action is not None:
        if request.method == "POST":
            subjects = request.POST.get('subject_id')
            session_years = request.POST.get('session_year_id')

            get_subject = Subject.objects.get(id=subjects)
            get_session_year = Session_year.objects.get(id=session_years)
            internal_mark = StudentResult.objects.filter(subject_id=get_subject )
    context = {
        'subjects': subjects,
        'session_years': session_years,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'internal_mark': internal_mark,
    }
    return render(request, 'Staff/view_internal_result.html', context)


   # student_id = Student.objects.filter(session_year_id=session_year)
'''
    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    student_marks_report = None
    if action is not None:
        if request.method == 'POST':
            subject_id = request.POST.get('subject_id')
            student_id =request.POST.get('student_id')

            get_subject = Subject.objects.get(id=subject_id)
            get_students = Student.objects.all()

            student_result = StudentResult.objects.filter(subject_id = get_subject, student_id=get_students)
            for i in student_result:
                internalresult_id = i.id
                student_marks_report = StudentReport.objects.filter(internalresult_id=internalresult_id)
'''


def STAFF_EDIT_INTERNALRESULT(request,id):
    staff = Staff.objects.get(id=id)
    student_result = StudentResult.objects.get(id=staff)

    context = {
        'student_result' : student_result,
    }
    return render(request,'Staff/edit_internal_result.html',context)



'''
def add_internal_mark(request):
    subjects = Subject.objects.filter(staff_id=request.user.id)
    session_years = Session_year.objects.all()
    action = request.GET.get('action')

    get_subject = None
    get_session_year = None
    students = None
    if action is not None:
        if request.method == "POST":

            subject_id = request.POST.get('subject_id')
            session_year = request.POST.get('session_year')

            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_year.objects.get(id=session_year)

            subject = Subject.objects.filter(id=subject_id)

            for i in subject:
                student_id = i.course.id
                students = Student.objects.filter(course_id=student_id, session_year_id=get_session_year)
    context = {
        "subjects": subjects,
        "session_years": session_years,
        "get_subject": get_subject,
        "get_session_year": get_session_year,
        'action': action,
        "students": students,
    }
    return render(request, "Staff/add_internal_mark.html", context)


def internal_mark_save(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        # session_year_id = request.POST.get('session_year')
        student_id = request.POST.get('student_id')
        subject_full_marks = request.POST.get('subject_full_marks')
        subject_obtained_marks = request.POST.get('subject_obtained_marks')

        get_student = Student.objects.get(admin=student_id)
        get_subject = Subject.objects.get(id=subject_id)
        # Check if Students Result Already Exists or not
        check_exists = Internal_mark.objects.filter(subject_id=get_subject, student_id=get_student).exists()

        if check_exists:
            internal_mark = Internal_mark.objects.get(subject_id=get_subject, student_id=get_student)
            internal_mark.subject_full_marks = subject_full_marks,
            internal_mark.subject_obtained_marks = subject_obtained_marks,
            internal_mark.save()
            messages.success(request, 'Result updated succesfully!')
            return redirect('add_internal_mark')
        else:
            internal_mark = Internal_mark(
                subject_id=get_subject,
                student_id=get_student,
                subject_full_marks=subject_full_marks,
                subject_obtained_marks=subject_obtained_marks,
            )
        internal_mark.save()
        messages.success(request, 'Result added succesfully!')
        return redirect('add_internal_mark')


def view_internal_mark(request):
    subjects = Subject.objects.filter(staff_id=request.user.id)
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
            internal_mark = Internal_mark.objects.filter(subject_id=get_subject, )
    context = {
        'subjects': subjects,
        'session_years': session_years,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'internal_mark': internal_mark,
    }
    return render(request, 'Staff/view_internal_mark.html', context)
'''

def DELETE_STAFF_INTERNALRESULT(request,id):
    internal_result = StudentResult.objects.get(id=id)
    internal_result.delete()
    messages.success(request, 'Result Is Successfully Deleted !')
    return redirect('staff_view_internal_result')
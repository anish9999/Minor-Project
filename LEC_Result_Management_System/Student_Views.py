from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from LEC_RMSapp.models import Student,Student_Notification,Student_Feedback,Subject,StudentResult,Course,Session_year,Year_Part,Regular_board_exam,Back_board_exam
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import math
from django.db.models.lookups import Transform

def home(request):
    student = Student.objects.get(admin = request.user.id)
    course = Course.objects.filter(id = student.course_id.id)
    course_count = Course.objects.filter(id=student.course_id.id).count()
    subject_count = Subject.objects.filter(session_year=student.session_year_id.id , course = student.course_id.id).count()
    subjects = Subject.objects.filter(session_year=student.session_year_id.id, course=student.course_id.id)


    course_list = []
    for subject in subjects:
        courses = Course.objects.get(id=subject.course.id)
        course_list.append(courses.id)
    perc = None
    final_course = []
    result_count1 = None
    # Removing Duplicate Course Id
    for course in course_list:
        if course not in final_course:
            final_course.append(course)
    students_count = Student.objects.filter(course_id__in=final_course).count()

    #session = Session_year.objects.filter(id =student.session_year_id.id)
    session_years = Session_year.objects.all()
    courses = Course.objects.all()
    session_years = Session_year.objects.all()


    

    ExternalResult_pass_count = Regular_board_exam.objects.filter(result__gte ='40' ,student_id = student.id).count()


    sessions = Session_year.objects.filter(id=student.session_year_id.id)
    subject = Subject.objects.all()
    

    Back_Exam_Result_count  = Back_board_exam.objects.filter(obtained_marks__gte ='40',student_id = student.id).count()
    # print(InternalResult_pass_count)
    #InternalResult_fail_count = StudentResult.objects.filter(exam_marks__range=(0, 31)).count()


    #print(subject_count)
    #print(perc)
    context = {
        'perc': perc,
        'subject_count': subject_count,
        'subjects': subjects,
        'course_count': course_count,
        'course': course,
        'ExternalResult_pass_count': ExternalResult_pass_count,
        'Back_Exam_Result_count':Back_Exam_Result_count,
    }
    return render(request, 'Student/home.html', context)
  


def STUDENT_NOTIFICATION(request):
    student = Student.objects.filter(admin = request.user.id)
    for i in student:
        student_id = i.id
        notification = Student_Notification.objects.filter(student_id = student_id)

        context ={
            'notification':notification,
        }
        return render(request,'Student/notification.html',context)


def STUDENT_NOTIFICATION_MARK_AS_DONE(request,status):
    notification = Student_Notification.objects.get(id = status)
    notification.status = 1
    notification.save()
    return redirect('student_notification')


def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(admin = request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id = student_id)

    context = {
        "feedback_history":feedback_history,
    }
    return render(request,'Student/feedback.html',context)


def STUDENT_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        student = Student.objects.get(admin=request.user.id)
        feedbacks = Student_Feedback(
            student_id = student,
            feedback = feedback,
            feedback_reply = "",
        )
        feedbacks.save()
    return redirect('student_feedback')


@login_required(login_url='/')
def view_internal_mark(request):
    student = Student.objects.get(admin = request.user.id)
    subjects = Subject.objects.filter(course=student.course_id.id)
    session_years = Session_year.objects.filter(id = student.session_year_id.id)

    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    internal_mark = None
    if action is not None:
        if request.method == "POST":
            subjects = request.POST.get('subjects')
            session_years = request.POST.get('session_years')

            student = Student.objects.get(admin = request.user.id)
            get_subject = Subject.objects.get(id=subjects)
            get_session_year = Session_year.objects.get(id=session_years)
            internal_mark = StudentResult.objects.filter(subject_id=get_subject,session_year_id=get_session_year,student_id=student)
    context = {
        'subjects': subjects,
        'session_years': session_years,
        'action': action,
        'get_subject': get_subject,
        'get_session_year': get_session_year,
        'internal_mark': internal_mark,
    }
    return render(request, 'Student/view_internal_mark.html',context)


def view_regular_board_result(request):
    student = Student.objects.get(admin = request.user.id)
    courses = Course.objects.get(id = student.course_id.id)
    session_years = Session_year.objects.get(id = student.session_year_id.id)

    regular_result = Regular_board_exam.objects.filter(course=courses, session_year=session_years,student_id=student)
    context = {
        'regular_result': regular_result,
        'courses':courses,
        'session_years':session_years,
    }
    return render(request, 'Student/view_regular_board_result.html', context)


def view_back_board_result(request):
    student = Student.objects.get(admin = request.user.id)
    courses = Course.objects.get(id = student.course_id.id)
    session_years = Session_year.objects.get(id = student.session_year_id.id)

    back_result = Back_board_exam.objects.filter(course=courses,session_year=session_years,student_id=student)
    context = {
        'courses':courses,
        'session_years':session_years,
        'back_result': back_result,
    }
    return render(request, 'Student/view_back_board_result.html', context)
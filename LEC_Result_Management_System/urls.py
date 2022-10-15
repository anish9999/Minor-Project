
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .import views,Hod_Views,Staff_Views,Student_Views
urlpatterns = [
        path('admin/', admin.site.urls),
        path('base/', views.BASE, name='base'),
        path('inbox_content/',views.INBOX_CONTENT, name='inbox_content'),

        # Login Path
        path('',views.LOGIN,name='login'),
        path('doLogin', views.doLogin, name='doLogin'),
        path('doLogout',views.doLogout,name='logout'),


        # Profile Update
        path('Profile',views.PROFILE,name='profile'),
        path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),


        # Inbox
        path('Inbox',views.INBOX,name='inbox'),
        path('Compose',views.INBOX_CHECK,name='inbox_check'),
        path('Important',views.INBOX_IMPORTANT,name='inbox_imp'),
        path('Sent/mail',views.SENT_MAIL,name='sent_mail'),
        path('Drafts',views.DRAFTS,name='drafts'),
        path('Trash',views.TRASH,name='trash'),

        # Notification
        path('Notifications',views.NOTIFICATIONS, name='allnotification'),


        # This is  Hod Panel Url
        path('Hod/Home',Hod_Views.HOME,name='admin_home'),
        path('Hod/Student/Add',Hod_Views.ADD_STUDENT,name='add_student'),
        path('Hod/Student/View',Hod_Views.VIEW_STUDENT,name='view_student'),
        path('Hod/Student/Edit/<str:id>',Hod_Views.EDIT_STUDENT,name='edit_student'),
        path('Hod/Student/Update',Hod_Views.UPDATE_STUDENT,name= 'update_student'),
        path('Hod/Student/Delete/<str:admin>', Hod_Views.DELETE_STUDENT,name='delete_student'),


        path('Hod/Staff/Add',Hod_Views.ADD_STAFF,name='add_staff'),
        path('Hod/Staff/Views',Hod_Views.VIEW_STAFF,name='view_staff'),
        path('Hod/Staff/Edit/<str:id>',Hod_Views.EDIT_STAFF,name='edit_staff'),
        path('Hod/Staff/Update',Hod_Views.UPDATE_STAFF,name='update_staff'),
        path('Hod/Staff/Delete/<str:admin>',Hod_Views.DELETE_STAFF,name='delete_staff'),


        path('Hod/Course/Add',Hod_Views.ADD_COURSE,name='add_course'),
        path('Hod/Course/View',Hod_Views.VIEW_COURSE,name='view_course'),
        path('Hod/Course/Edit<str:id>',Hod_Views.EDIT_COURSE,name='edit_course'),
        path('Hod/Course/Update',Hod_Views.UPDATE_COURSE, name='update_course'),
        path('Hod/Course/Delete/<str:id>',Hod_Views.DELETE_COURSE,name='delete_course'),


        path('Hod/Subject/Add', Hod_Views.ADD_SUBECT,name='add_subject'),
        path('Hod/Subject/View', Hod_Views.VIEW_SUBJECT,name='view_subject'),
        path('Hod/Subject/Edit/<str:id>',Hod_Views.EDIT_SUBJECT,name='edit_subject'),
        path('Hod/Subject/Update', Hod_Views.UPDATE_SUBJECT,name='update_subject'),
        path('Hod/Subject/Delete/<str:id>',Hod_Views.DELETE_SUBJECT,name='delete_subject'),


        path('Hod/Session/Add',Hod_Views.ADD_SESSION,name='add_session'),
        path('Hod/Session/View',Hod_Views.VIEW_SESSION,name='view_session'),
        path('Hod/Session/Edit/<str:id>',Hod_Views.EDIT_SESSION,name='edit_session'),
        path('Hod/Session/Update',Hod_Views.UPDATE_SESSION,name='update_session'),
        path('Hod/Session/Delete/<str:id>',Hod_Views.DELETE_SESSION,name='delete_session'),


        path('Hod/Staff/Send_Notification',Hod_Views.STAFF_SEND_NOTIFICATION,name='staff_send_notification'),
        path('Hod/Staff/Save_Notification',Hod_Views.SAVE_STAFF_NOTIFICATION,name='save_staff_notification'),

        path('Hod/Staff/feedback',Hod_Views.STAFF_FEEDBACK,name='staff_feedback_reply'),
        path('Hod/Staff/feedback/save',Hod_Views.STAFF_FEEDBACK_SAVE,name='staff_feedback_reply_save'),

        path('Hod/Student/send_notification',Hod_Views.STUDENT_SEND_NOTIFICATION,name= 'student_send_notification'),
        path('Hod/Student/save_notification',Hod_Views.SAVE_STUDENT_NOTIFICATION,name='save_student_notification'),

        path('Hod/Student/feedback',Hod_Views.STUDENT_FEEDBACK,name='get_student_feedback'),
        path('Hod/Student/feedback/reply/save',Hod_Views.REPLY_STUDENT_FEEDBACK,name='reply_student_feedback'),

        path('Hod/Student/details/<str:id>',Hod_Views.STUDENT_DETAILS,name='student_details'),
        path('Hod/Staff/details/<str:id>',Hod_Views.STAFF_DETAILS,name='staff_details'),


             ##                  ''' RESULTS'''                       ##
        path('Hod/Results/InternalExamView', Hod_Views.view_internal_mark, name="view_internal_mark"),
         path('Hod/Result/InternalMark/Edit/<str:id>', Hod_Views.edit_internal_mark,name='edit_internal_mark'),
        path('Hod/Result/InternalMark/Update', Hod_Views.update_internal_mark,name='update_internal_mark'),
        path('Hod/Result/InternalMark/<str:id>', Hod_Views.delete_internal_mark,name='delete_internal_mark'),

        path('Hod/Results/Regular/Add', Hod_Views.add_regular_board_result,name="add_regular_board_result"),
        path('Hod/Results/Regular/Save', Hod_Views.regular_board_result_save,name="regular_board_result_save"),
        path('Hod/Results/Regular/View', Hod_Views.view_regular_board_result,name="view_regular_board_result"),
        path('Hod/Result/Regular/Edit/<str:id>', Hod_Views.edit_regular_board_result,name='edit_regular_board_result'),
        path('Hod/Result/Regular/Update', Hod_Views.update_regular_board_result,name='update_regular_board_result'),
        path('Hod/Result/Regular/<str:id>', Hod_Views.delete_regular_board_result,name='delete_regular_board_result'),

        path('Hod/Results/Back/Add', Hod_Views.add_back_board_result, name="add_back_board_result"),
        path('Hod/Results/Back/Save', Hod_Views.back_board_result_save, name="back_board_result_save"),
        path('Hod/Results/Back/View', Hod_Views.view_back_board_result, name="view_back_board_result"),
        path('Hod/Result/Back/Edit/<str:id>', Hod_Views.edit_back_board_result,name='edit_back_board_result'),
        path('Hod/Result/Back/Update', Hod_Views.update_back_board_result,name='update_back_board_result'),
        path('Hod/Result/Back/<str:id>', Hod_Views.delete_back_board_result,name='delete_back_board_result'),





        # This is a  Staff Urls
        path('Staff/Home',Staff_Views.HOME,name='staff_home'),
        path('Staff/Notifications',Staff_Views.NOTIFICATIONS,name='notifications'),
        path('Staff/marks_as_done/<str:status>',Staff_Views.STAFF_NOTIFICATION_MARK_AS_DONE, name='staff_notification_mark_as_done'),

        path('Staff/staff_feedback', Staff_Views.STAFF_FEEDBACK, name="staff_feedback"),
        path('Staff/Feedback/Save',Staff_Views.STAFF_FEEDBACK_SAVE,name='staff_feedback_save'),


        path('Staff/Add/InternalResult',Staff_Views.STAFF_ADD_RESULT,name='staff_internal_result'),
        path('Staff/Save/InternalResult',Staff_Views.STAFF_SAVE_RESULT,name='staff_save_internal_result'),
        path('Staff/View/InternalResult',Staff_Views.STAFF_VIEW_INTERNALRESULT,name='staff_view_internal_result'),
        path('Staff/Update/InternalResult/<str:id>',Staff_Views.STAFF_EDIT_INTERNALRESULT,name='staff_update_internal_result'),
        path('Staff/Delete/InternalResult/<str:id>',Staff_Views.DELETE_STAFF_INTERNALRESULT,name='delete_internal_result'),


        # Student Urls
        path('Student/Home',Student_Views.home,name='student_home'),
        path('Student/Notifications',Student_Views.STUDENT_NOTIFICATION,name='student_notification'),
        path('Student/marks_as_done/<str:status>',Student_Views.STUDENT_NOTIFICATION_MARK_AS_DONE, name='student_notification_mark_as_done'),


        path('Student/feedback',Student_Views.STUDENT_FEEDBACK,name='student_feedback'),
        path('Student/feedback/save',Student_Views.STUDENT_FEEDBACK_SAVE,name= 'student_feedback_save'),

        path('Student/View/InternalResult',Student_Views.view_internal_mark,name='student_view_internal_result'),
        path('Student/View/Board/Regular',Student_Views.view_regular_board_result,name='student_view_regular_board_result'),
        path('Student/View/Board/Back',Student_Views.view_back_board_result,name='student_view_back_board_result'),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

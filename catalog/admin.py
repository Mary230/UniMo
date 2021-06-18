from django.contrib import admin
from .models import Student, Competition, User, Teacher, TakenCompetitionn, Subject, CompetitionFile, AnswerFile, ColabHref


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_student', 'is_teacher',)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'university_name', 'points', 'display_list_competition')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'university_name', 'subject', 'display_list_students')


class CometitionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'desc', 'state', 'author')


class TakenCompetitionnAdmin(admin.ModelAdmin):
    list_display = ('student', 'competition', 'score', 'date')


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')


class CompetitionFileAdmin(admin.ModelAdmin):
    list_display = ('competition', 'test_file', 'data_file', 'true_answer_file')


class AnswerFileAdmin(admin.ModelAdmin):
    list_display = ('student', 'competition', 'model_file', 'data_file', 'is_public')

class ColabHrefAdmin(admin.ModelAdmin):
    list_display = ('student', 'competition', 'href')



admin.site.register(User, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Competition, CometitionAdmin)
admin.site.register(TakenCompetitionn, TakenCompetitionnAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(CompetitionFile, CompetitionFileAdmin)
admin.site.register(AnswerFile, AnswerFileAdmin)
admin.site.register(ColabHref, ColabHrefAdmin)


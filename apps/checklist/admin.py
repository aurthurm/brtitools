from django.contrib import admin
from django.db import models
from django import forms
from django.forms import TextInput, Textarea

from .models import (
    Response,
    Answer, 
    Question,
    Group,
    Category,
    CheckList,
    Section,
)


class GroupInline(admin.TabularInline):
    model = Group
    extra = 0


class CustomQuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomQuestionForm, self).__init__(*args, **kwargs)
        self.initial['group'] = Group.objects.filter(pk=0)
        if self.instance.parent:       
            self.fields['group'].queryset = self.instance.parent.groups.all()
        else:
            self.fields['group'].queryset = Group.objects.filter(pk=0)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = CustomQuestionForm
    fields = (('checklist', 'category', 'group', 'required', ),'parent', ('question', 'help'), )
    search_fields = ['question', ]
    list_display = ['question', 'group', 'number', 'category']    
    inlines = [GroupInline, ]
    list_filter = ('checklist', 'category', )   
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':8, 'cols':50})},
    }


class AnswerInline(admin.StackedInline):
    model = Answer    
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':50})},
    }
    fields = ('question', ('answer', 'comment', ), )
    extra = 0


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    fields = (('evaluator', 'site', 'checklist'), 'comment',)
    list_filter = ('checklist', )
    inlines = [AnswerInline, ]

class QuestionInline(admin.StackedInline):
    model = Question

@admin.register(CheckList)
class CheckListAdmin(admin.ModelAdmin):
    fields = (('name', 'section'), 'description')
    # inlines = [QuestionInline, ]


admin.site.register(Section)
admin.site.register(Category)


# formfield_overrides = {
#     models.CharField: {'widget': TextInput(attrs={'size':'20'})},
#     models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
# }
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey

from .._core.mixins import DateCreateUpdateMixin
from ..sites.models import Site

class Section(models.Model):
    """
    Section :-
        IT, Laboratory
    """
    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("Description"), null=True, blank=True)

    class Meta:
        verbose_name = _("sections")
        verbose_name_plural = _("sections")

    def __str__(self):
        return self.name


class CheckList(DateCreateUpdateMixin):
    """
    A checlist :-
        a set questions that await answering
    """
    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("Description"), null=True, blank=True)
    is_published = models.BooleanField(_("Users can see it and answer it"), default=True)
    need_logged_user = models.BooleanField(_("Only authenticated users can see it and answer it"))
    editable_answers = models.BooleanField(_("Users can edit their answers afterwards"), default=True)
    section = models.ForeignKey("Section", on_delete=models.SET_NULL, null=True, related_name="checklists")

    class Meta:
        verbose_name = _("check list")
        verbose_name_plural = _("check lists")

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("checklist-detail", kwargs={"checklist_id": self.pk})


class Category(models.Model):
    name = models.CharField(_("name"), max_length=30)
    description = models.TextField(_("Description"), null=True, blank=True)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name



TEXT = "text"
SHORT_TEXT = "short-text"
RADIO = "radio"
SELECT = "select"
SELECT_IMAGE = "select_image"
SELECT_MULTIPLE = "select-multiple"
INTEGER = "integer"
FLOAT = "float"
DATE = "date"

QUESTION_TYPES = (
    (TEXT, _("text (multiple line)")),
    (SHORT_TEXT, _("short text (one line)")),
    (RADIO, _("radio")),
    (SELECT, _("select")),
    (SELECT_MULTIPLE, _("Select Multiple")),
    (SELECT_IMAGE, _("Select Image")),
    (INTEGER, _("integer")),
    (FLOAT, _("float")),
    (DATE, _("date")),
)


class Question(MPTTModel):
    checklist = models.ForeignKey("CheckList", on_delete=models.CASCADE, related_name="questions")
    question = models.TextField(_("Question"),)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, related_name="questions")
    required = models.BooleanField(_("Required"), default=True)
    type = models.CharField(_("Type"), max_length=200, choices=QUESTION_TYPES, default=RADIO)
    number = models.IntegerField(_("Number"), blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    help = models.TextField(_("Help"), null=True, blank=True)
    group = models.ForeignKey("Group", on_delete=models.CASCADE, null=True, blank=True, related_name='questions')

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")
        ordering = ("number",)
    
    def save(self, *args, **kwargs):
        all_questions = Question.objects.all()
        if self in all_questions:
            pass # dont change number
        else:
            self.number = all_questions.count() + 1

        super(Question, self).save(*args, **kwargs)
    
    def get_admin_change_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.pk])

    @staticmethod
    def standardize(value, group_by_letter_case=None, group_by_slugify=None):
        """ Standardize a value in order to group by slugify or letter case """
        if group_by_slugify:
            value = slugify(value)
        if group_by_letter_case:
            value = value.lower()
        return value

    @staticmethod
    def standardize_list(string_list, group_by_letter_case=None, group_by_slugify=None):
        """ Return a list of standardized string from a csv string.."""
        return [Question.standardize(strng, group_by_letter_case, group_by_slugify) for strng in string_list]
    
    def __str__(self):
        msg = "Question '{}' ".format(self.question)
        if self.required:
            msg += "(*) "
        return msg


class Group(models.Model):
    """
    A group :-
        a question might have sub questions that are grouped
    """
    question = models.ForeignKey("Question", on_delete=models.SET_NULL, null=True, related_name="groups")
    name = models.CharField(_("name"), max_length=50)

    def __str__(self):
        return self.name 


YES = "yes"
NO = "no"
PARTIAL = "partial"

ANSWER_CHOICES = (
    (YES, _("yes")),
    (NO, _("no")),
    (PARTIAL, _("partial")),
)


class Response(DateCreateUpdateMixin):
    """
    A response :-
        a set of answers for a specific checklist for a specitic site
    """
    evaluator = models.ForeignKey("auth.User", on_delete=models.PROTECT, related_name="responses")
    site = models.ForeignKey(Site, on_delete=models.PROTECT, related_name="responses")
    checklist = models.ForeignKey("CheckList", on_delete=models.CASCADE, related_name="responses")
    comment = models.TextField(_("Comment"), null=True, blank=True)

    def __str__(self):
        return f' Evaluator: {self.evaluator.username}, {self.checklist.name}, Created: {self.date_created}, Updated: {self.date_updated}'


class Answer(DateCreateUpdateMixin):
    """
    An Answer :-
        - direct response to a specific question
        - an answer is linked to (this) specific Response (Analysis) undergoing
    """
    question = models.ForeignKey("Question", on_delete=models.CASCADE, related_name="answers")
    answer = models.CharField(_("Choice"), max_length=50, choices=ANSWER_CHOICES, default=PARTIAL)
    comment = models.TextField(_("Comment"), blank=True, null=True)
    response = models.ForeignKey("Response", on_delete=models.CASCADE, related_name="answers")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['question', 'response', ],
                name = "unique answer"
            )
        ]

    def __str__(self):
        return "{} ANSWER '{}' COMMENT '{}'".format(self.question.question, self.answer, self.comment)


from django.db.models.signals import post_save, pre_save, m2m_changed
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

from apps.checklist.models import (
    Response, 
    Answer,
    YES, NO, PARTIAL,
)


def populate__checklist_questions__to_response(instance, sender, **kwargs):
    """
    When a Response is created,
    Initialise Answer for every question in the selected checklist.
    """
    print("inside signal")
    response = instance
    # get selected checklist
    checklist = instance.checklist
    # get all questions in this checklist
    questions = checklist.questions.all()
    if kwargs['created'] == True:
        print("created")
        # create an answer for each question and assign its instance to this response
        if questions.count() > 0:
            for question in questions:
                Answer.objects.create(
                    question = question,
                    answer = NO,
                    response = response
                )
    else:
        print("just a save")
        # get all answers for this response
        answers = Answer.objects.filter(response__exact=response)
        # answers should equate questions in a checklist
        print("descrepancy ??", questions.count(), answers.count())
        if questions.count() > answers.count():
            # new question(s) added 
            # check is each question was answered else add answer
            for question in questions:
                is_answered = answers.filter(question__exact=question)
                print("is answered: ", is_answered.count())
                if is_answered.count() == 0:
                    # this is the new question
                    # linking it to this answer response
                    print("Questio to add: ", question)
                    Answer.objects.create(
                        question = question,
                        answer = NO,
                        response = response
                    )
                else: 
                    # question was answered
                    pass
        else:
            # a question was deleted -> model will CASCADE
            pass                


post_save.connect(populate__checklist_questions__to_response, sender=Response)
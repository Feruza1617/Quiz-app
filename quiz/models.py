from random import random

from django.db import models

# Create your models here.





class Quiz(models.Model):
    title = models.CharField(max_length=221)
    topic = models.CharField(max_length=221)
    number_of_questions = models.IntegerField()
    time = models.IntegerField(help_text="Duration of the quiz in minutes")
    required_score_to_pass = models.IntegerField(help_text="Required score in %")
    # difficulty = models.IntegerField(choices=DIFFICULTY, default=0)

    def __str__(self):
        return f"{self.title}-{self.topic}"

    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]

    class Meta:
        verbose_name_plural = 'quizzes'
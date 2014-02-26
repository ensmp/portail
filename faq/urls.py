from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('faq.views',
    url(r'^$', 'questions', name='faq_questions'),
    url(r'^poser_question/?$', 'poser_question', name='faq_poser_question'),
    url(r'^question_posee/?$', 'question_posee', name='faq_question_posee'),
)
from datetime import timedelta
from random import Random
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .services.rules import OPERATIONS, SECONDS_BY_LEVEL, generate_question

class RulesTests(TestCase):
    def test_questions_are_valid_for_every_setting(self):
        for age in range(6, 13):
            for operation in OPERATIONS:
                for level in range(1, 6):
                    q = generate_question(age, operation, level, Random(4))
                    if operation == "sumar": self.assertEqual(q.left + q.right, q.answer)
                    elif operation == "restar": self.assertEqual(q.left - q.right, q.answer)
                    elif operation == "multiplicar": self.assertEqual(q.left * q.right, q.answer)
                    elif operation == 'dividir': self.assertEqual(q.left // q.right, q.answer)
                    elif operation == 'comparar': self.assertEqual(max(q.left, q.right), q.answer)
                    else: self.assertEqual(q.left + q.right, q.answer)
                    self.assertGreaterEqual(q.answer, 0)
                    if operation == 'dividir': self.assertNotEqual(q.right, 0)
        self.assertGreater(SECONDS_BY_LEVEL[1], SECONDS_BY_LEVEL[5])

class FlowTests(TestCase):
    def choose_age(self): return self.client.post(reverse('age'), {'age': 8, 'time_mode': 'normal'})
    def test_age_validation_and_guard(self):
        self.assertRedirects(self.client.get(reverse('operations')), reverse('age'))
        self.assertEqual(self.client.post(reverse('age'), {'age': 13}).status_code, 400)
        self.assertRedirects(self.choose_age(), reverse('operations'))

    def test_high_contrast_preference_is_applied_from_the_session(self):
        self.client.post(reverse('age'), {'age': 8, 'time_mode': 'normal', 'high_contrast': 'true'})
        self.assertTrue(self.client.session['high_contrast'])
        self.assertContains(self.client.get(reverse('operations')), 'class="high-contrast"')

    def test_dashboard_and_service_worker(self):
        self.choose_age()
        self.assertContains(self.client.get(reverse('dashboard')), 'Aún no has terminado una sesión')
        worker = self.client.get(reverse('service_worker'))
        self.assertEqual(worker['Content-Type'], 'application/javascript')
        self.assertContains(worker, "addEventListener")

    def test_english_and_catalan_interface_copy(self):
        for language, expected in (("en", "Let's learn maths!"), ("ca", "Aprenem matemàtiques!")):
            self.client.post(reverse('set_language'), {'language': language, 'next': reverse('age')})
            self.assertContains(self.client.get(reverse('age')), expected)
    def test_operation_levels_and_full_session(self):
        self.choose_age()
        for op in OPERATIONS:
            response = self.client.get(reverse('levels', args=[op]))
            self.assertContains(response, 'Nivel', count=5)
        url = reverse('play', args=['sumar', 1])
        self.client.get(url)
        for number in range(10):
            game = self.client.session['game']; answer = game['question']['answer']
            response = self.client.post(url, {'answer': answer})
            self.assertContains(response, 'Muy bien')
            if number < 9: self.client.post(reverse('next_question'))
            else: self.assertRedirects(self.client.post(reverse('next_question')), reverse('results'))
        self.assertContains(self.client.get(reverse('results')), '10')
    def test_expired_and_double_send(self):
        self.choose_age(); url = reverse('play', args=['restar', 1]); self.client.get(url)
        session = self.client.session; game = session['game']; game['expires_at'] = (timezone.now()-timedelta(seconds=1)).isoformat(); session['game'] = game; session.save()
        self.assertContains(self.client.post(url, {'answer': 1}), 'Se acabó el tiempo')
        self.assertEqual(len(self.client.session['game']['answers']), 1)
        self.client.post(url, {'answer': 1})
        self.assertEqual(len(self.client.session['game']['answers']), 1)

    def test_progress_and_review_are_private_to_the_session(self):
        self.choose_age(); url = reverse('play', args=['sumar', 1]); self.client.get(url)
        for number in range(10):
            self.client.post(url, {'answer': -1})
            self.client.post(reverse('next_question'))
        self.assertContains(self.client.get(reverse('results')), 'Repasar lo que cuesta')
        self.assertEqual(self.client.session['progress']['sumar']['completed'], 1)
        self.assertContains(self.client.get(reverse('levels', args=['sumar'])), 'Nivel 1 · recomendado')
        response = self.client.post(reverse('review'))
        self.assertRedirects(response, reverse('play', args=['sumar', 1]))
        game = self.client.session['game']
        self.assertTrue(game['is_review'])
        self.assertEqual(game['questions_total'], 5)

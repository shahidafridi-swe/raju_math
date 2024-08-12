from django.utils import timezone
from .models import Student, Payment

class PaymentGenerationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.generate_payments_for_current_month()
        response = self.get_response(request)
        return response

    def generate_payments_for_current_month(self):
        now = timezone.now()
        current_year = now.year
        current_month = now.strftime('%B')
        
        for student in Student.objects.all():
            Payment.objects.get_or_create(
                student=student,
                month=current_month,
                year=current_year,
                defaults={'is_paid': False}
            )

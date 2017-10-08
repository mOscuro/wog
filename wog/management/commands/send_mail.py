from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from django.core.mail import send_mail


def send_test_mail():
    send_mail('Testing django emails', 'DJANGO EMAIL TESTING WORKING', 'matthieu.oscuro@gmail.com', ['matthieu.oscuro@gmail.com'])


class Command(BaseCommand):
    help = 'Creates Group for authenticated user with model permission'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Sending mail...'))
        send_test_mail()
        self.stdout.write(self.style.SUCCESS('Done!'))
        

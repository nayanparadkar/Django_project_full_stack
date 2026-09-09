from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tweet.models import Tweet


class Command(BaseCommand):
    help = "Create sample users and tweets for local development"

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(username='devuser')
        if created:
            user.set_password('devpass')
            user.save()
        for i in range(1, 6):
            Tweet.objects.get_or_create(user=user, content=f'Sample tweet {i}')
        self.stdout.write(self.style.SUCCESS('Seeded sample tweets (user devuser / devpass)'))

from django.core.management.base import BaseCommand, CommandError
from users.models import User


class Command(BaseCommand):
  def reset_housemates_done_monthly(self, *args, **options):
      
from time import sleep

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError

__all__ = [
    "Command",
]


class Command(BaseCommand):
    help = "Waits until the database is available."

    def add_arguments(self, parser):
        parser.add_argument(
            "--seconds",
            nargs="?",
            type=int,
            help="Number of seconds to wait before retrying",
            default=3,
        )
        parser.add_argument(
            "--retries",
            nargs="?",
            type=int,
            help="Number of retries before exiting",
            default=5,
        )

    def handle(self, **options) -> None:
        wait = options["seconds"]
        retries = options["retries"]

        if wait <= 0:
            self.stderr.write(
                self.style.ERROR("Error: --seconds must be a positive integer.")
            )
            return
        if retries <= 0:
            self.stderr.write(
                self.style.ERROR("Error: --retries must be a positive integer.")
            )
            return

        self.stdout.write(
            f"Waiting for the database (up to {retries} retries every "
            f"{wait} second(s))..."
        )

        for i in range(retries):
            try:
                connection.ensure_connection()
                self.stdout.write(self.style.SUCCESS("Database is available!"))
                return
            except OperationalError:
                if i == retries - 1:
                    self.stderr.write(
                        self.style.ERROR(
                            "Error: Could not connect to database after "
                            f"{retries} retries."
                        )
                    )
                    return
                else:
                    sleep(wait)
                    self.stdout.write(
                        f"Retry {i+1}/{retries} - waiting for the database..."
                    )

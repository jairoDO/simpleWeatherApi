from django.core.management.base import BaseCommand
from ...models import Weather
from ...utils.geocoder import Geocoder

geocoder = Geocoder()


class Command(BaseCommand):
    help = 'Generate entries in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of entries to generate (default: 10)'
        )

    def handle(self, *args, **options):
        count = options['count']
        for _ in range(count):
            weather_data = Weather.generate_random_weather_with_real_location(
                geocoder_instance=geocoder,
                choose_instance=True
            )
            Weather(**weather_data).save()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated {count} entries')
        )

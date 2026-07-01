"""
Management command: seed_pexels_images

Downloads and attaches Pexels photos to every model that has an image field
and currently has no image set.

Usage:
    python manage.py seed_pexels_images
    python manage.py seed_pexels_images --model service
    python manage.py seed_pexels_images --overwrite
"""

from django.core.management.base import BaseCommand
from core.models import Service, Testimonial, BlogPost, GalleryImage, Event
from core.utils.pexels import search_pexels, download_pexels_image


SEED_QUERIES = {
    'service': [
        ('healthcare', 'healthcare AI technology'),
        ('retail', 'retail commerce AI'),
        ('education', 'education technology AI'),
        ('logistics', 'logistics transport AI'),
        ('security', 'security surveillance AI'),
        ('other', 'artificial intelligence technology'),
    ],
    'blog': [
        ('AI Technology', 'artificial intelligence future'),
        ('Case Study', 'business technology success'),
        ('Business Insights', 'business analytics data'),
        ('Innovation', 'innovation digital transformation'),
        ('default', 'technology AI solutions'),
    ],
    'gallery': 'AI solutions technology office',
    'event': 'technology conference event',
    'testimonial': 'professional business person portrait',
}


def _pick_query(model_name, obj):
    if model_name == 'service':
        for cat, q in SEED_QUERIES['service']:
            if obj.category == cat:
                return q
        return 'artificial intelligence'
    if model_name == 'blog':
        for cat, q in SEED_QUERIES['blog']:
            if obj.category and cat.lower() in obj.category.lower():
                return q
        return SEED_QUERIES['blog'][-1][1]
    return SEED_QUERIES.get(model_name, 'technology')


class Command(BaseCommand):
    help = 'Fetch and attach Pexels images to model records that have no image.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            choices=['service', 'blog', 'gallery', 'event', 'testimonial', 'all'],
            default='all',
            help='Which model to seed (default: all)',
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            default=False,
            help='Replace existing images too',
        )

    def handle(self, *args, **options):
        target = options['model']
        overwrite = options['overwrite']

        tasks = {
            'service':     (Service.objects.all(),     'image',  'service'),
            'blog':        (BlogPost.objects.all(),    'image',  'blog'),
            'gallery':     (GalleryImage.objects.all(),'image',  'gallery'),
            'event':       (Event.objects.all(),       'image',  'event'),
            'testimonial': (Testimonial.objects.all(), 'photo',  'testimonial'),
        }

        if target != 'all':
            tasks = {target: tasks[target]}

        for model_name, (queryset, field_name, _) in tasks.items():
            self.stdout.write(self.style.MIGRATE_HEADING(f'\n--- {model_name.upper()} ---'))
            _photo_cache = {}  # query → list of photo dicts

            for obj in queryset:
                current = getattr(obj, field_name)
                if current and not overwrite:
                    obj_str = str(obj).encode('ascii', 'replace').decode('ascii')
                    self.stdout.write(f'  skip  {obj_str} (already has image)')
                    continue

                query = _pick_query(model_name, obj)
                if query not in _photo_cache:
                    photos = search_pexels(query, per_page=15, page=1)
                    _photo_cache[query] = photos

                photos = _photo_cache.get(query, [])
                if not photos:
                    self.stdout.write(self.style.WARNING(f'  no results for "{query}"'))
                    continue

                # Pick a different photo for each object to avoid repetition
                idx = list(queryset).index(obj) % len(photos)
                photo = photos[idx]
                filename = f'pexels_{photo["id"]}.jpg'

                image_file = download_pexels_image(photo['large'], filename)
                if image_file is None:
                    obj_str = str(obj).encode('ascii', 'replace').decode('ascii')
                    self.stdout.write(self.style.ERROR(f'  failed to download for {obj_str}'))
                    continue

                if current and overwrite:
                    current.delete(save=False)

                getattr(obj, field_name).save(filename, image_file, save=True)
                photographer = photo["photographer"].encode('ascii', 'replace').decode('ascii')
                obj_str = str(obj).encode('ascii', 'replace').decode('ascii')
                self.stdout.write(
                    self.style.SUCCESS(f'  OK  {obj_str}  <- {photographer} / Pexels')
                )

        self.stdout.write(self.style.SUCCESS('\nDone.'))

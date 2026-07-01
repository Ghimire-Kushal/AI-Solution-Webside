"""
Run: python manage.py update_portfolio_testimonials
Replaces portfolio projects and testimonials with the exact data from the brief.
"""
from django.core.management.base import BaseCommand
from core.models import Service, Testimonial


PORTFOLIO = [
    {
        'slug': 'healthsync-ai',
        'title': 'HealthSync AI',
        'record_type': 'portfolio',
        'category': 'healthcare',
        'short_description': 'AI-powered healthcare workflow and patient management platform.',
        'description': (
            'HealthSync AI transforms how healthcare providers manage patient workflows, '
            'appointments, and diagnostics. By integrating AI into core hospital operations, '
            'we help medical teams focus on care while automation handles coordination.'
        ),
        'features': [
            'Automated appointment scheduling',
            'Predictive patient risk alerts',
            'Real-time record synchronization',
            'AI-assisted diagnostics',
            'Wearable device integration',
        ],
        'icon': 'bi-heart-pulse',
        'client_name': 'Horizon Care',
        'is_featured': True,
        'order': 1,
    },
    {
        'slug': 'retailmind',
        'title': 'RetailMind',
        'record_type': 'portfolio',
        'category': 'retail',
        'short_description': 'Retail analytics and customer behavior intelligence solution.',
        'description': (
            'RetailMind gives retailers a deep understanding of customer behavior, '
            'optimizes product placement, and forecasts sales with precision. '
            'Integrated with POS and CRM systems for seamless operations.'
        ),
        'features': [
            'Customer movement tracking',
            'Sales forecasting',
            'Inventory optimization',
            'Product placement recommendations',
            'POS and CRM integration',
        ],
        'icon': 'bi-shop',
        'client_name': 'UrbanStyle',
        'is_featured': True,
        'order': 2,
    },
    {
        'slug': 'edunova',
        'title': 'EduNova',
        'record_type': 'portfolio',
        'category': 'education',
        'short_description': 'AI-based adaptive learning and education management system.',
        'description': (
            'EduNova personalizes the learning journey for every student using AI-driven '
            'recommendations, automated assessments, and engagement analytics. '
            'Supports multilingual environments for international institutions.'
        ),
        'features': [
            'Personalized learning modules',
            'Automated grading',
            'AI-generated quizzes',
            'Student engagement analytics',
            'Multilingual support',
        ],
        'icon': 'bi-mortarboard',
        'client_name': 'Nova International College',
        'is_featured': True,
        'order': 3,
    },
    {
        'slug': 'fleetpilot-ai',
        'title': 'FleetPilot AI',
        'record_type': 'portfolio',
        'category': 'logistics',
        'short_description': 'Transportation and logistics optimization platform.',
        'description': (
            'FleetPilot AI brings intelligent automation to fleet management — from live '
            'vehicle tracking and dynamic route optimization to predictive fuel analytics '
            'and automated delivery scheduling.'
        ),
        'features': [
            'Live vehicle tracking',
            'Route optimization',
            'Fuel prediction analytics',
            'Driver performance insights',
            'Delivery scheduling automation',
        ],
        'icon': 'bi-truck',
        'client_name': 'SwiftMove Logistics',
        'is_featured': True,
        'order': 4,
    },
    {
        'slug': 'securevision',
        'title': 'SecureVision',
        'record_type': 'portfolio',
        'category': 'security',
        'short_description': 'AI-driven surveillance and security monitoring solution.',
        'description': (
            'SecureVision combines computer vision and behavioral AI to provide real-time '
            'threat detection, facial recognition access control, and cloud-based security '
            'analytics for enterprise environments.'
        ),
        'features': [
            'Real-time threat detection',
            'Facial recognition access control',
            'Suspicious activity alerts',
            'Cloud-based security analytics',
            'Remote monitoring dashboard',
        ],
        'icon': 'bi-shield-check',
        'client_name': 'Nexa Corporate Solutions',
        'is_featured': True,
        'order': 5,
    },
]

TESTIMONIALS = [
    {
        'name': 'Dr. Melissa Carter',
        'role': 'Chief Medical Officer',
        'company': 'Horizon Care',
        'content': 'HealthSync AI improved our hospital operations significantly and reduced patient waiting times.',
        'rating': 4.8,
        'project_name': 'HealthSync AI',
        'is_active': True,
    },
    {
        'name': 'Daniel Brooks',
        'role': 'Head of Operations',
        'company': 'UrbanStyle',
        'content': 'RetailMind helped us understand customer behavior better and increase overall revenue.',
        'rating': 4.7,
        'project_name': 'RetailMind',
        'is_active': True,
    },
    {
        'name': 'Priya Sharma',
        'role': 'Academic Director',
        'company': 'Nova International College',
        'content': 'EduNova transformed the learning experience for our students with personalized AI recommendations.',
        'rating': 4.9,
        'project_name': 'EduNova',
        'is_active': True,
    },
    {
        'name': 'Eric Thompson',
        'role': 'CEO',
        'company': 'SwiftMove Logistics',
        'content': 'FleetPilot AI streamlined our delivery network and improved fuel efficiency.',
        'rating': 4.6,
        'project_name': 'FleetPilot AI',
        'is_active': True,
    },
    {
        'name': 'Karen White',
        'role': 'Security Director',
        'company': 'Nexa Corporate Solutions',
        'content': 'SecureVision strengthened our security infrastructure with real-time monitoring and alerts.',
        'rating': 4.8,
        'project_name': 'SecureVision',
        'is_active': True,
    },
]


class Command(BaseCommand):
    help = 'Update portfolio projects and testimonials to match the brief exactly'

    def handle(self, *args, **kwargs):
        self._update_portfolio()
        self._update_testimonials()
        self.stdout.write(self.style.SUCCESS('Portfolio and testimonials updated successfully!'))

    def _update_portfolio(self):
        slugs = [p['slug'] for p in PORTFOLIO]

        # Remove old portfolio records not in this list
        deleted, _ = Service.objects.filter(record_type='portfolio').exclude(slug__in=slugs).delete()
        if deleted:
            self.stdout.write(f'  Removed {deleted} old portfolio record(s)')

        for data in PORTFOLIO:
            slug = data.pop('slug')
            obj, created = Service.objects.update_or_create(slug=slug, defaults=data)
            data['slug'] = slug  # restore
            action = 'Created' if created else 'Updated'
            self.stdout.write(f'  {action}: {obj.title}')

        self.stdout.write(f'  Portfolio total: {Service.objects.filter(record_type="portfolio").count()}')

    def _update_testimonials(self):
        # Clear all existing testimonials and replace with the 5 from the brief
        Testimonial.objects.all().delete()
        self.stdout.write('  Cleared existing testimonials')

        for data in TESTIMONIALS:
            Testimonial.objects.create(**data)
            self.stdout.write(f'  Created: {data["name"]} - {data["company"]}')

        self.stdout.write(f'  Testimonials total: {Testimonial.objects.count()}')

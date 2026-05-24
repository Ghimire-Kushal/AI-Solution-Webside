"""
Run: python manage.py seed_data
Seeds the database with all real content from the AI Solutions Portfolio 2026.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from core.models import Service, Testimonial, Event, BlogPost, SiteSettings


class Command(BaseCommand):
    help = 'Seeds the database with initial portfolio and testimonial data'

    def handle(self, *args, **kwargs):
        self.seed_services()
        self.seed_testimonials()
        self.seed_events()
        self.seed_blog()
        self.seed_settings()
        self.stdout.write(self.style.SUCCESS('✅  Database seeded successfully!'))

    def seed_services(self):
        services = [
            {
                'title': 'HealthSync AI',
                'slug': 'healthsync-ai',
                'category': 'healthcare',
                'short_description': 'AI-powered healthcare workflow and patient management platform.',
                'description': 'HealthSync AI transforms how healthcare providers manage patient workflows, appointments, and diagnostics. By integrating AI into core hospital operations, we help medical teams focus on care while automation handles coordination.',
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
                'title': 'RetailMind',
                'slug': 'retailmind',
                'category': 'retail',
                'short_description': 'Retail analytics and customer behavior intelligence solution.',
                'description': 'RetailMind gives retailers a deep understanding of customer behavior, optimizes product placement, and forecasts sales with precision. Integrated with POS and CRM systems for seamless operations.',
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
                'title': 'EduNova',
                'slug': 'edunova',
                'category': 'education',
                'short_description': 'AI-based adaptive learning and education management system.',
                'description': 'EduNova personalizes the learning journey for every student using AI-driven recommendations, automated assessments, and engagement analytics. Supports multilingual environments for international institutions.',
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
                'title': 'FleetPilot AI',
                'slug': 'fleetpilot-ai',
                'category': 'logistics',
                'short_description': 'Transportation and logistics optimization platform.',
                'description': 'FleetPilot AI brings intelligent automation to fleet management — from live vehicle tracking and dynamic route optimization to predictive fuel analytics and automated delivery scheduling.',
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
                'title': 'SecureVision',
                'slug': 'securevision',
                'category': 'security',
                'short_description': 'AI-driven surveillance and security monitoring solution.',
                'description': 'SecureVision combines computer vision and behavioral AI to provide real-time threat detection, facial recognition access control, and cloud-based security analytics for enterprise environments.',
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

        for data in services:
            Service.objects.get_or_create(slug=data['slug'], defaults=data)

        self.stdout.write('  → 5 portfolio services seeded')

    def seed_testimonials(self):
        testimonials = [
            {
                'name': 'Dr. Melissa Carter',
                'role': 'Chief Medical Officer',
                'company': 'Horizon Care',
                'content': 'HealthSync AI improved our hospital operations significantly and reduced patient waiting times. The predictive risk alerts alone have helped us prevent several critical incidents.',
                'rating': 4.8,
                'project_name': 'HealthSync AI',
            },
            {
                'name': 'Daniel Brooks',
                'role': 'Head of Operations',
                'company': 'UrbanStyle',
                'content': 'RetailMind helped us understand customer behavior better and increase overall revenue. The inventory optimization feature saved us thousands in overstock costs within the first month.',
                'rating': 4.7,
                'project_name': 'RetailMind',
            },
            {
                'name': 'Priya Sharma',
                'role': 'Academic Director',
                'company': 'Nova International College',
                'content': 'EduNova transformed the learning experience for our students with personalized AI recommendations. Student engagement scores improved by 40% in just one semester.',
                'rating': 4.9,
                'project_name': 'EduNova',
            },
            {
                'name': 'Eric Thompson',
                'role': 'CEO',
                'company': 'SwiftMove Logistics',
                'content': 'FleetPilot AI streamlined our delivery network and improved fuel efficiency. We reduced delivery times by 30% and our drivers love the intelligent route suggestions.',
                'rating': 4.6,
                'project_name': 'FleetPilot AI',
            },
            {
                'name': 'Karen White',
                'role': 'Security Director',
                'company': 'Nexa Corporate Solutions',
                'content': 'SecureVision strengthened our security infrastructure with real-time monitoring and alerts. The facial recognition system has completely replaced our old access card system.',
                'rating': 4.8,
                'project_name': 'SecureVision',
            },
        ]

        for data in testimonials:
            Testimonial.objects.get_or_create(
                name=data['name'], company=data['company'], defaults=data
            )

        self.stdout.write('  → 5 client testimonials seeded')

    def seed_events(self):
        events = [
            {
                'title': 'AI-Solutions Company Launch',
                'description': 'Official launch of AI-Solutions in Kathmandu, Nepal. Introduced our vision for transforming digital workplaces with intelligent AI technologies.',
                'date': date(2024, 1, 15),
                'location': 'ISMT College, Tinkune, Kathmandu',
                'is_completed': True,
            },
            {
                'title': 'HealthSync AI Go-Live',
                'description': 'Successful deployment of HealthSync AI at Horizon Care hospital. First enterprise AI rollout covering 3 departments and 200+ staff.',
                'date': date(2024, 4, 10),
                'location': 'Kathmandu, Nepal',
                'is_completed': True,
            },
            {
                'title': 'RetailMind Beta Launch — UrbanStyle',
                'description': 'Deployed RetailMind analytics platform for UrbanStyle retail chain across 5 store locations. Integrated with existing POS and CRM systems.',
                'date': date(2024, 7, 22),
                'location': 'Kathmandu, Nepal',
                'is_completed': True,
            },
            {
                'title': 'EduNova Partnership — Nova International College',
                'description': 'Signed partnership agreement and initiated EduNova implementation for 2,000+ students. Multilingual support configured for Nepali and English.',
                'date': date(2024, 10, 5),
                'location': 'Kathmandu, Nepal',
                'is_completed': True,
            },
            {
                'title': 'FleetPilot AI & SecureVision Rollout',
                'description': 'Simultaneous deployment of FleetPilot AI for SwiftMove Logistics and SecureVision for Nexa Corporate Solutions. Two major enterprise clients go live.',
                'date': date(2025, 1, 20),
                'location': 'Kathmandu, Nepal',
                'is_completed': True,
            },
            {
                'title': 'AI-Solutions Annual Tech Summit 2025',
                'description': 'First annual technology summit bringing together 200+ business leaders, AI experts, and clients. Showcase of live AI demos and panel discussions on the future of workplace automation.',
                'date': date(2025, 6, 15),
                'location': 'Hotel Himalaya, Kathmandu',
                'is_completed': True,
            },
            {
                'title': 'Product Version 2.0 Release',
                'description': 'Major platform update including enhanced Gemini AI integration, new analytics dashboard, and mobile-first design for all client portals.',
                'date': date(2026, 3, 10),
                'location': 'AI-Solutions HQ, Kathmandu',
                'is_completed': False,
            },
            {
                'title': 'International Expansion — UK Office Opening',
                'description': 'Opening of AI-Solutions UK office in Sunderland to serve European and international clients. Marks the beginning of our global expansion strategy.',
                'date': date(2026, 7, 3),
                'location': 'Sunderland, United Kingdom',
                'is_completed': False,
            },
        ]

        for data in events:
            Event.objects.get_or_create(
                title=data['title'], date=data['date'], defaults=data
            )

        self.stdout.write('  → 8 timeline events seeded')

    def seed_blog(self):
        posts = [
            {
                'title': 'How AI Virtual Assistants Are Transforming the Workplace',
                'slug': 'ai-virtual-assistants-transforming-workplace',
                'excerpt': 'Discover how AI-powered virtual assistants are reducing manual workload, improving response times, and revolutionizing how teams collaborate.',
                'content': 'Artificial Intelligence is no longer a futuristic concept — it is actively reshaping how businesses operate today. AI virtual assistants, in particular, have emerged as one of the most impactful tools in the modern workplace.\n\nFrom scheduling meetings to answering customer queries and generating reports, AI assistants handle repetitive cognitive tasks with remarkable accuracy and speed. At AI-Solutions, our Aria assistant processes thousands of interactions daily across our client deployments.\n\nThe key benefit is not just automation — it is augmentation. AI does not replace your team; it empowers them to focus on creative, strategic, and human-centric work that machines cannot do.',
                'author': 'AI-Solutions Team',
                'category': 'AI Technology',
                'is_published': True,
                'published_at': timezone.now(),
            },
            {
                'title': 'The Future of AI in Healthcare: Lessons from HealthSync AI',
                'slug': 'future-ai-healthcare-healthsync',
                'excerpt': 'Our HealthSync AI project at Horizon Care revealed powerful insights about how AI can support — not replace — healthcare professionals.',
                'content': 'When we started building HealthSync AI, we had one principle: technology should serve the doctor, not the other way around. After deploying at Horizon Care hospital, we have seen this principle pay off in remarkable ways.\n\nPatient waiting times dropped by 35%. Risk alerts flagged three critical cases that might otherwise have been missed. Record synchronization, which used to take staff hours per shift, now happens automatically in real time.\n\nBut the most important lesson? The doctors trust the system more when they understand it. Transparency in AI decision-making is not optional — it is essential for adoption in high-stakes environments like healthcare.',
                'author': 'AI-Solutions Team',
                'category': 'Case Study',
                'is_published': True,
                'published_at': timezone.now(),
            },
            {
                'title': '5 Ways AI Can Cut Your Business Operational Costs by 40%',
                'slug': '5-ways-ai-cut-operational-costs',
                'excerpt': 'Real numbers from real deployments: here is how AI-Solutions clients reduced operational costs by an average of 40% within 6 months.',
                'content': 'Cost reduction is one of the most compelling business cases for AI adoption. But vague claims are not enough — here are five concrete mechanisms with real figures from our deployments.\n\n1. Workflow Automation: Manual, repetitive tasks account for up to 30% of employee time. Automating these with AI cuts that to near zero.\n2. Predictive Maintenance: AI predicts equipment failures before they happen, reducing downtime costs significantly.\n3. Inventory Optimization: RetailMind helped UrbanStyle reduce overstock by 25% in month one.\n4. Energy Management: Smart building AI reduces energy consumption by 15–20%.\n5. Customer Service Automation: AI chatbots handle 70% of common queries without human intervention.\n\nThe ROI on AI investment, when implemented correctly, is typically realized within 6–9 months.',
                'author': 'AI-Solutions Team',
                'category': 'Business Insights',
                'is_published': True,
                'published_at': timezone.now(),
            },
        ]

        for data in posts:
            BlogPost.objects.get_or_create(slug=data['slug'], defaults=data)

        self.stdout.write('  → 3 blog posts seeded')

    def seed_settings(self):
        SiteSettings.objects.get_or_create(pk=1, defaults={
            'site_name': 'AI-Solutions',
            'tagline': 'Innovate | Support | Empower',
            'email': 'hello@ai-solutions.com',
            'phone': '+977 98XXXXXXXX',
            'address': 'Kathmandu, Nepal',
            'time_zone': 'Asia/Kathmandu',
        })
        self.stdout.write('  → Site settings initialised')

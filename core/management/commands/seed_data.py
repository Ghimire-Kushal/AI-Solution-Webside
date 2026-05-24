"""
Run: python manage.py seed_data
Seeds every section to 10 items with realistic AI-Solutions content.
"""
import io
import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import date, timedelta
from core.models import Service, Testimonial, Event, BlogPost, GalleryImage, ContactMessage, SiteSettings


class Command(BaseCommand):
    help = 'Seeds all sections to 10 items each'

    def handle(self, *args, **kwargs):
        self.seed_services()
        self.seed_testimonials()
        self.seed_events()
        self.seed_blog()
        self.seed_gallery()
        self.seed_contacts()
        self.seed_settings()
        self.stdout.write(self.style.SUCCESS('\n✅  All sections seeded to 10 items!'))

    # ──────────────────────────────────────────────
    # SERVICES (10)
    # ──────────────────────────────────────────────
    def seed_services(self):
        services = [
            {
                'title': 'HealthSync AI',
                'slug': 'healthsync-ai',
                'category': 'healthcare',
                'short_description': 'AI-powered healthcare workflow and patient management platform.',
                'description': 'HealthSync AI transforms how healthcare providers manage patient workflows, appointments, and diagnostics. By integrating AI into core hospital operations, we help medical teams focus on care while automation handles coordination. Deployed at Horizon Care, it reduced patient waiting times by 35% and flagged critical risk cases in real time.',
                'features': ['Automated appointment scheduling', 'Predictive patient risk alerts', 'Real-time record synchronization', 'AI-assisted diagnostics', 'Wearable device integration'],
                'icon': 'bi-heart-pulse', 'client_name': 'Horizon Care', 'is_featured': True, 'order': 1,
            },
            {
                'title': 'RetailMind',
                'slug': 'retailmind',
                'category': 'retail',
                'short_description': 'Retail analytics and customer behavior intelligence solution.',
                'description': 'RetailMind gives retailers a deep understanding of customer behavior, optimizes product placement, and forecasts sales with precision. Integrated with POS and CRM systems for seamless operations. UrbanStyle saw a 25% reduction in overstock costs within the first month of deployment.',
                'features': ['Customer movement tracking', 'Sales forecasting', 'Inventory optimization', 'Product placement recommendations', 'POS and CRM integration'],
                'icon': 'bi-shop', 'client_name': 'UrbanStyle', 'is_featured': True, 'order': 2,
            },
            {
                'title': 'EduNova',
                'slug': 'edunova',
                'category': 'education',
                'short_description': 'AI-based adaptive learning and education management system.',
                'description': 'EduNova personalizes the learning journey for every student using AI-driven recommendations, automated assessments, and engagement analytics. Supports multilingual environments for international institutions. Nova International College recorded a 40% improvement in student engagement scores.',
                'features': ['Personalized learning modules', 'Automated grading', 'AI-generated quizzes', 'Student engagement analytics', 'Multilingual support'],
                'icon': 'bi-mortarboard', 'client_name': 'Nova International College', 'is_featured': True, 'order': 3,
            },
            {
                'title': 'FleetPilot AI',
                'slug': 'fleetpilot-ai',
                'category': 'logistics',
                'short_description': 'Transportation and logistics optimization platform.',
                'description': 'FleetPilot AI brings intelligent automation to fleet management — from live vehicle tracking and dynamic route optimization to predictive fuel analytics and automated delivery scheduling. SwiftMove Logistics reduced delivery times by 30% within two months.',
                'features': ['Live vehicle tracking', 'Route optimization', 'Fuel prediction analytics', 'Driver performance insights', 'Delivery scheduling automation'],
                'icon': 'bi-truck', 'client_name': 'SwiftMove Logistics', 'is_featured': True, 'order': 4,
            },
            {
                'title': 'SecureVision',
                'slug': 'securevision',
                'category': 'security',
                'short_description': 'AI-driven surveillance and security monitoring solution.',
                'description': 'SecureVision combines computer vision and behavioral AI to provide real-time threat detection, facial recognition access control, and cloud-based security analytics for enterprise environments. Nexa Corporate Solutions replaced their legacy access card system entirely.',
                'features': ['Real-time threat detection', 'Facial recognition access control', 'Suspicious activity alerts', 'Cloud-based security analytics', 'Remote monitoring dashboard'],
                'icon': 'bi-shield-check', 'client_name': 'Nexa Corporate Solutions', 'is_featured': True, 'order': 5,
            },
            {
                'title': 'AI Virtual Assistant (Aria)',
                'slug': 'aria-virtual-assistant',
                'category': 'other',
                'short_description': 'Enterprise-grade AI virtual assistant for customer and employee support.',
                'description': 'Aria is AI-Solutions\' flagship conversational AI — deployed as an intelligent front-desk assistant for businesses. Powered by Google Gemini, Aria handles customer queries, routes support tickets, books appointments, and escalates complex issues to human agents seamlessly.',
                'features': ['Natural language understanding', '24/7 automated response', 'CRM and ticketing integration', 'Multi-language support', 'Escalation to human agents'],
                'icon': 'bi-robot', 'client_name': 'AI-Solutions (Internal)', 'is_featured': True, 'order': 6,
            },
            {
                'title': 'SmartHR Analytics',
                'slug': 'smarthr-analytics',
                'category': 'other',
                'short_description': 'AI-powered HR analytics for workforce planning and retention.',
                'description': 'SmartHR Analytics helps HR teams predict employee attrition, identify high performers, and plan hiring cycles using machine learning models trained on company-specific data. Reduces turnover costs and improves workforce planning accuracy by up to 60%.',
                'features': ['Attrition risk prediction', 'Performance trend analysis', 'Hiring demand forecasting', 'Sentiment analysis from surveys', 'Automated HR reporting'],
                'icon': 'bi-people-fill', 'client_name': 'TechBridge Corp', 'is_featured': False, 'order': 7,
            },
            {
                'title': 'DocuMind',
                'slug': 'documind',
                'category': 'other',
                'short_description': 'Intelligent document processing and data extraction platform.',
                'description': 'DocuMind uses AI to extract, classify, and validate data from unstructured documents — invoices, contracts, forms, and reports. It eliminates manual data entry, reduces errors by 90%, and integrates directly with ERP and accounting systems.',
                'features': ['OCR with 99%+ accuracy', 'Contract clause extraction', 'Invoice auto-processing', 'Compliance flag detection', 'ERP / accounting integration'],
                'icon': 'bi-file-earmark-text', 'client_name': 'FinCore Accountancy', 'is_featured': False, 'order': 8,
            },
            {
                'title': 'AgriSense AI',
                'slug': 'agrisense-ai',
                'category': 'other',
                'short_description': 'Precision agriculture and crop yield prediction platform.',
                'description': 'AgriSense AI empowers farmers and agribusinesses with AI-driven crop monitoring, yield forecasting, and soil health analytics. Using satellite imagery and IoT sensor data, it provides actionable insights that increase yields by an average of 22%.',
                'features': ['Satellite crop monitoring', 'Yield prediction models', 'Soil health analysis', 'Irrigation optimization', 'Weather risk alerts'],
                'icon': 'bi-flower1', 'client_name': 'GreenField Agro', 'is_featured': False, 'order': 9,
            },
            {
                'title': 'FinGuard AI',
                'slug': 'finguard-ai',
                'category': 'security',
                'short_description': 'AI-powered financial fraud detection and risk management.',
                'description': 'FinGuard AI monitors financial transactions in real time, detecting anomalies, flagging suspicious patterns, and preventing fraud before it occurs. Built for banks, fintech companies, and e-commerce platforms that process high transaction volumes.',
                'features': ['Real-time transaction monitoring', 'Anomaly and fraud detection', 'Risk scoring per transaction', 'Regulatory compliance reporting', 'API integration with payment gateways'],
                'icon': 'bi-bank', 'client_name': 'NovaPay Fintech', 'is_featured': False, 'order': 10,
            },
        ]

        count = 0
        for data in services:
            _, created = Service.objects.get_or_create(slug=data['slug'], defaults=data)
            if created:
                count += 1
        self.stdout.write(f'  → Services: {Service.objects.count()} total ({count} new)')

    # ──────────────────────────────────────────────
    # TESTIMONIALS (10)
    # ──────────────────────────────────────────────
    def seed_testimonials(self):
        testimonials = [
            {'name': 'Dr. Melissa Carter', 'role': 'Chief Medical Officer', 'company': 'Horizon Care', 'content': 'HealthSync AI improved our hospital operations significantly and reduced patient waiting times. The predictive risk alerts alone have helped us prevent several critical incidents that could have cost lives.', 'rating': 4.8, 'project_name': 'HealthSync AI'},
            {'name': 'Daniel Brooks', 'role': 'Head of Operations', 'company': 'UrbanStyle', 'content': 'RetailMind helped us understand customer behavior better and increase overall revenue. The inventory optimization feature saved us thousands in overstock costs within the first month of deployment.', 'rating': 4.7, 'project_name': 'RetailMind'},
            {'name': 'Priya Sharma', 'role': 'Academic Director', 'company': 'Nova International College', 'content': 'EduNova transformed the learning experience for our students with personalized AI recommendations. Student engagement scores improved by 40% in just one semester — results we never expected so quickly.', 'rating': 4.9, 'project_name': 'EduNova'},
            {'name': 'Eric Thompson', 'role': 'CEO', 'company': 'SwiftMove Logistics', 'content': 'FleetPilot AI streamlined our delivery network and improved fuel efficiency. We reduced delivery times by 30% and our drivers appreciate the intelligent route suggestions that avoid congestion.', 'rating': 4.6, 'project_name': 'FleetPilot AI'},
            {'name': 'Karen White', 'role': 'Security Director', 'company': 'Nexa Corporate Solutions', 'content': 'SecureVision strengthened our security infrastructure with real-time monitoring and alerts. The facial recognition system has completely replaced our old access card system — far more reliable.', 'rating': 4.8, 'project_name': 'SecureVision'},
            {'name': 'James Patel', 'role': 'HR Director', 'company': 'TechBridge Corp', 'content': 'SmartHR Analytics gave us visibility we never had before. We identified our top 15% performers and redesigned retention packages based on real data. Attrition dropped by 20% in 6 months.', 'rating': 4.7, 'project_name': 'SmartHR Analytics'},
            {'name': 'Sophie Nguyen', 'role': 'Finance Manager', 'company': 'FinCore Accountancy', 'content': 'DocuMind processes our client invoices in seconds — something that took our team hours every day. Error rates dropped to nearly zero and our staff can now focus on advisory work instead of data entry.', 'rating': 4.9, 'project_name': 'DocuMind'},
            {'name': 'Raj Adhikari', 'role': 'Farm Operations Manager', 'company': 'GreenField Agro', 'content': 'AgriSense AI changed how we think about farming. Yield predictions are remarkably accurate and the irrigation optimization alone paid back our investment in the first growing season.', 'rating': 4.6, 'project_name': 'AgriSense AI'},
            {'name': 'Laura Chen', 'role': 'CTO', 'company': 'NovaPay Fintech', 'content': 'FinGuard AI catches fraud attempts that our old rule-based system completely missed. Transaction monitoring is real-time and the API integration with our payment gateway was seamless.', 'rating': 4.8, 'project_name': 'FinGuard AI'},
            {'name': 'Marcus Reid', 'role': 'Digital Transformation Lead', 'company': 'GlobalBridge Enterprises', 'content': 'Working with AI-Solutions was a genuinely collaborative experience. They understood our business before writing a single line of code. Aria — their virtual assistant — is now the first point of contact for all our customer enquiries.', 'rating': 5.0, 'project_name': 'AI Virtual Assistant'},
        ]

        count = 0
        for data in testimonials:
            _, created = Testimonial.objects.get_or_create(name=data['name'], company=data['company'], defaults=data)
            if created:
                count += 1
        self.stdout.write(f'  → Testimonials: {Testimonial.objects.count()} total ({count} new)')

    # ──────────────────────────────────────────────
    # EVENTS (10)
    # ──────────────────────────────────────────────
    def seed_events(self):
        events = [
            {'title': 'AI-Solutions Company Launch', 'description': 'Official launch of AI-Solutions in Kathmandu, Nepal. Introduced our vision for transforming digital workplaces with intelligent AI technologies. Over 100 guests attended including local business leaders and tech entrepreneurs.', 'date': date(2024, 1, 15), 'location': 'ISMT College, Tinkune, Kathmandu', 'is_completed': True},
            {'title': 'HealthSync AI Go-Live at Horizon Care', 'description': 'Successful deployment of HealthSync AI at Horizon Care hospital. First enterprise AI rollout covering 3 departments and 200+ staff. Patient waiting times reduced by 35% in the first week.', 'date': date(2024, 4, 10), 'location': 'Kathmandu, Nepal', 'is_completed': True},
            {'title': 'RetailMind Beta Launch — UrbanStyle', 'description': 'Deployed RetailMind analytics platform for UrbanStyle retail chain across 5 store locations. Integrated with existing POS and CRM systems. Overstock costs reduced by 25% within 30 days.', 'date': date(2024, 7, 22), 'location': 'Kathmandu, Nepal', 'is_completed': True},
            {'title': 'EduNova Partnership — Nova International College', 'description': 'Signed partnership agreement and initiated EduNova implementation for 2,000+ students. Multilingual support configured for Nepali and English. Student engagement jumped 40% in semester one.', 'date': date(2024, 10, 5), 'location': 'Kathmandu, Nepal', 'is_completed': True},
            {'title': 'FleetPilot AI & SecureVision Double Launch', 'description': 'Simultaneous deployment of FleetPilot AI for SwiftMove Logistics and SecureVision for Nexa Corporate Solutions. Two major enterprise clients go live on the same day — a milestone for our delivery team.', 'date': date(2025, 1, 20), 'location': 'Kathmandu, Nepal', 'is_completed': True},
            {'title': 'AI-Solutions Annual Tech Summit 2025', 'description': 'First annual technology summit bringing together 200+ business leaders, AI experts, and clients. Live AI demos, panel discussions on workplace automation, and announcement of three new product lines.', 'date': date(2025, 6, 15), 'location': 'Hotel Himalaya, Kathmandu', 'is_completed': True},
            {'title': 'SmartHR Analytics — TechBridge Corp Launch', 'description': 'Deployed SmartHR Analytics for TechBridge Corp\'s HR team. AI-powered attrition prediction and performance analytics now serve 1,500 employees. Turnover rate fell 20% within 6 months.', 'date': date(2025, 9, 8), 'location': 'Kathmandu, Nepal', 'is_completed': True},
            {'title': 'DocuMind & FinGuard AI Launch', 'description': 'Launched DocuMind for FinCore Accountancy and FinGuard AI for NovaPay Fintech. Both solutions went live simultaneously, marking AI-Solutions\' entry into fintech and professional services sectors.', 'date': date(2025, 11, 12), 'location': 'Kathmandu, Nepal', 'is_completed': True},
            {'title': 'Product Platform v2.0 Release', 'description': 'Major platform update featuring enhanced Gemini AI integration, redesigned analytics dashboards, mobile-first client portals, and a new developer API for custom integrations.', 'date': date(2026, 3, 10), 'location': 'AI-Solutions HQ, Kathmandu', 'is_completed': False},
            {'title': 'UK Office Opening — Sunderland', 'description': 'Grand opening of AI-Solutions UK office in Sunderland, marking the beginning of our international expansion. Serving European and UK-based enterprise clients. First EU contracts signed at the launch event.', 'date': date(2026, 7, 3), 'location': 'Sunderland, United Kingdom', 'is_completed': False},
        ]

        count = 0
        for data in events:
            _, created = Event.objects.get_or_create(title=data['title'], date=data['date'], defaults=data)
            if created:
                count += 1
        self.stdout.write(f'  → Events: {Event.objects.count()} total ({count} new)')

    # ──────────────────────────────────────────────
    # BLOG POSTS (10)
    # ──────────────────────────────────────────────
    def seed_blog(self):
        posts = [
            {
                'title': 'How AI Virtual Assistants Are Transforming the Workplace',
                'slug': 'ai-virtual-assistants-transforming-workplace',
                'excerpt': 'AI-powered virtual assistants are reducing manual workload, improving response times, and revolutionizing how teams collaborate.',
                'content': 'Artificial Intelligence is no longer a futuristic concept — it is actively reshaping how businesses operate today. AI virtual assistants, in particular, have emerged as one of the most impactful tools in the modern workplace.\n\nFrom scheduling meetings to answering customer queries and generating reports, AI assistants handle repetitive cognitive tasks with remarkable accuracy and speed. At AI-Solutions, our Aria assistant processes thousands of interactions daily across our client deployments.\n\nThe key benefit is not just automation — it is augmentation. AI does not replace your team; it empowers them to focus on creative, strategic, and human-centric work that machines cannot do.\n\nCompanies that have adopted AI assistants report an average of 35% improvement in team productivity and a 50% reduction in routine email volume. The ROI is typically realized within 3 months of deployment.',
                'author': 'Pratik Rauniyar', 'category': 'AI Technology', 'is_published': True, 'published_at': timezone.now() - timedelta(days=60),
            },
            {
                'title': 'The Future of AI in Healthcare: Lessons from HealthSync AI',
                'slug': 'future-ai-healthcare-healthsync',
                'excerpt': 'Our HealthSync AI project at Horizon Care revealed powerful insights about how AI can support — not replace — healthcare professionals.',
                'content': 'When we started building HealthSync AI, we had one principle: technology should serve the doctor, not the other way around. After deploying at Horizon Care hospital, we have seen this principle pay off in remarkable ways.\n\nPatient waiting times dropped by 35%. Risk alerts flagged three critical cases that might otherwise have been missed. Record synchronization, which used to take staff hours per shift, now happens automatically in real time.\n\nBut the most important lesson? The doctors trust the system more when they understand it. Transparency in AI decision-making is not optional — it is essential for adoption in high-stakes environments like healthcare.\n\nAs we continue to develop HealthSync AI, we are focused on explainability: making sure every alert, every recommendation, comes with a clear reason that a clinician can evaluate and act on.',
                'author': 'AI-Solutions Team', 'category': 'Case Study', 'is_published': True, 'published_at': timezone.now() - timedelta(days=45),
            },
            {
                'title': '5 Ways AI Can Cut Your Business Operational Costs by 40%',
                'slug': '5-ways-ai-cut-operational-costs',
                'excerpt': 'Real numbers from real deployments: how AI-Solutions clients reduced operational costs by an average of 40% within 6 months.',
                'content': 'Cost reduction is one of the most compelling business cases for AI adoption. Here are five concrete mechanisms with real figures from our deployments.\n\n1. Workflow Automation: Manual, repetitive tasks account for up to 30% of employee time. Automating these with AI cuts that near zero.\n\n2. Predictive Maintenance: AI predicts equipment failures before they happen, reducing unplanned downtime costs by up to 70%.\n\n3. Inventory Optimization: RetailMind helped UrbanStyle reduce overstock by 25% in month one alone.\n\n4. Energy Management: Smart building AI reduces energy consumption by 15–20% through intelligent HVAC and lighting control.\n\n5. Customer Service Automation: AI chatbots handle 70% of common queries without human intervention, cutting support costs dramatically.\n\nThe ROI on AI investment, when implemented correctly, is typically realized within 6–9 months.',
                'author': 'AI-Solutions Team', 'category': 'Business Insights', 'is_published': True, 'published_at': timezone.now() - timedelta(days=30),
            },
            {
                'title': 'Building Responsible AI: Our Ethics Framework',
                'slug': 'responsible-ai-ethics-framework',
                'excerpt': 'At AI-Solutions, every product we build is guided by a clear ethics framework. Here is what that means in practice.',
                'content': 'As AI becomes more embedded in critical business decisions, the question of responsibility becomes paramount. Who is accountable when an AI system makes a wrong call? How do we ensure AI does not amplify existing biases?\n\nAt AI-Solutions, we have developed a five-pillar ethics framework that guides every product we build:\n\n1. Transparency: Every AI decision must be explainable in plain language.\n2. Fairness: Models are tested across demographic groups to identify and remove bias.\n3. Privacy: We follow GDPR-aligned data minimization principles by default.\n4. Accountability: Every deployment has a named human responsible for AI outcomes.\n5. Safety: Critical systems include human-in-the-loop checkpoints for high-stakes decisions.\n\nThis framework is not just a document — it is built into our development process, tested in QA, and reviewed quarterly.',
                'author': 'Pratik Rauniyar', 'category': 'AI Ethics', 'is_published': True, 'published_at': timezone.now() - timedelta(days=22),
            },
            {
                'title': 'How We Built RetailMind: A Behind-the-Scenes Look',
                'slug': 'how-we-built-retailmind',
                'excerpt': 'A transparent look at the architecture, challenges, and decisions behind one of our most complex deployments.',
                'content': 'RetailMind started as a simple question from UrbanStyle\'s operations team: "Why do we keep running out of our bestsellers while overstocking items that don\'t sell?"\n\nThe answer, it turned out, was a data problem. Their POS data existed in one system, their stock management in another, and customer behavior data was barely captured at all.\n\nPhase 1 was data unification. We built a pipeline that merged POS transactions, inventory logs, and in-store sensor data into a single real-time data warehouse.\n\nPhase 2 was the ML layer. We trained gradient boosting models on 18 months of historical data to forecast demand at the SKU level, by store, by day of week.\n\nPhase 3 was the interface — a clean dashboard that store managers could actually use without a data science degree.\n\nThe result: 25% overstock reduction in month one, and UrbanStyle now considers data-driven inventory management a core competitive advantage.',
                'author': 'AI-Solutions Team', 'category': 'Technical Deep Dive', 'is_published': True, 'published_at': timezone.now() - timedelta(days=18),
            },
            {
                'title': 'AI in Education: What EduNova Taught Us About Student Engagement',
                'slug': 'ai-education-edunova-engagement',
                'excerpt': 'Personalized learning is not just a buzzword — EduNova proved it with a 40% engagement improvement at Nova International College.',
                'content': 'Traditional education delivers the same content to every student at the same pace. AI-powered education does the opposite — it meets each student where they are.\n\nEduNova\'s personalization engine analyses learning patterns, quiz performance, time-on-task, and content preferences to build a unique learning pathway for every student.\n\nAt Nova International College, the results were striking. Students who previously disengaged from standard lecture materials responded actively to the AI-curated content sequences. Completion rates for online modules jumped from 54% to 89%.\n\nThe automated grading system freed up lecturer time by an estimated 8 hours per week per faculty member — time redirected into one-on-one student support.\n\nThe key insight? Engagement is not a student problem. It is a content-fit problem. When the material matches the learner\'s level and style, engagement follows naturally.',
                'author': 'AI-Solutions Team', 'category': 'Case Study', 'is_published': True, 'published_at': timezone.now() - timedelta(days=14),
            },
            {
                'title': 'Getting Started with AI: A Practical Guide for Small Businesses',
                'slug': 'getting-started-ai-small-businesses',
                'excerpt': 'You do not need a million-pound budget to benefit from AI. Here is a practical starting point for small and medium businesses.',
                'content': 'The biggest misconception about AI is that it is only for large enterprises with massive technology budgets. The reality is very different — some of the most impactful AI applications cost less than a part-time employee\'s monthly salary.\n\nStep 1: Identify your highest-volume repetitive tasks. These are your best AI candidates — things like responding to common customer queries, processing invoices, or scheduling appointments.\n\nStep 2: Start with a pilot. Pick one process, automate it with an AI tool, and measure the results over 30 days. Do not try to automate everything at once.\n\nStep 3: Choose integrated solutions over custom builds. Off-the-shelf AI tools that plug into your existing software (CRM, accounting, email) deliver value faster and cheaper than bespoke development.\n\nStep 4: Train your team. AI adoption fails when staff feel threatened rather than supported. Frame AI as a productivity tool, not a replacement.\n\nAt AI-Solutions, we offer free initial consultations to help businesses identify their best AI starting point. Contact us to book yours.',
                'author': 'Pratik Rauniyar', 'category': 'Business Insights', 'is_published': True, 'published_at': timezone.now() - timedelta(days=10),
            },
            {
                'title': 'The Role of Gemini AI in Modern Business Applications',
                'slug': 'gemini-ai-modern-business-applications',
                'excerpt': 'Google Gemini has opened new possibilities for business AI. Here is how we are using it to power smarter applications.',
                'content': 'Google Gemini represents a significant leap in what large language models can do for business applications. Unlike earlier models, Gemini was designed from the ground up for multimodal reasoning — understanding text, images, and structured data together.\n\nAt AI-Solutions, we use Gemini as the backbone of our Aria virtual assistant. What makes Gemini particularly powerful for enterprise use is its ability to follow complex instructions consistently, maintain context across long conversations, and generate structured outputs that integrate directly with business systems.\n\nFor document processing in DocuMind, Gemini extracts and classifies contract clauses with an accuracy that previously required specialized NLP models trained on legal data.\n\nFor FinGuard AI, Gemini helps generate plain-language explanations of why a transaction was flagged — making it easier for compliance teams to review and act on alerts.\n\nThe key to using Gemini effectively in production is prompt engineering: carefully designing the instructions that shape every AI interaction. This is as much an art as a science, and it is a core competency we have built at AI-Solutions.',
                'author': 'AI-Solutions Team', 'category': 'AI Technology', 'is_published': True, 'published_at': timezone.now() - timedelta(days=7),
            },
            {
                'title': 'From Kathmandu to Sunderland: The AI-Solutions Story',
                'slug': 'ai-solutions-story-kathmandu-sunderland',
                'excerpt': 'How a tech startup born in Nepal\'s capital grew into a company with global ambitions and an upcoming UK office.',
                'content': 'AI-Solutions began with a simple observation: small and medium businesses in Nepal were being left behind by the AI revolution. The tools that existed were either too expensive, too complex, or designed for western markets with different business contexts.\n\nWe set out to build AI solutions that were practical, affordable, and genuinely useful for businesses in our market. Starting with HealthSync AI and HealthSync AI at Horizon Care hospital, we proved that enterprise-grade AI could be deployed in resource-constrained environments without sacrificing quality.\n\nFive deployments and 500+ satisfied users later, the question shifted from "can we build this?" to "where do we take this next?"\n\nThe answer is Sunderland. Our upcoming UK office positions AI-Solutions to serve European clients who need the kind of hands-on, relationship-driven approach we have always offered — now backed by a portfolio of proven deployments.\n\nThe journey from a small team in Tinkune, Kathmandu to an international AI company has been anything but linear. But every challenge along the way has made our products, our processes, and our team stronger.',
                'author': 'Pratik Rauniyar', 'category': 'Company News', 'is_published': True, 'published_at': timezone.now() - timedelta(days=4),
            },
            {
                'title': 'AI Security: How FinGuard and SecureVision Protect Our Clients',
                'slug': 'ai-security-finguard-securevision',
                'excerpt': 'Security is not just a feature — it is the product. Inside our two AI security solutions and what makes them different.',
                'content': 'In an era of increasingly sophisticated cyber threats and financial fraud, AI has become the most effective tool for real-time security monitoring. Rule-based systems cannot keep up with the speed and creativity of modern attacks. AI can.\n\nSecureVision uses computer vision models trained on thousands of hours of security footage to recognize suspicious behaviors — not just faces. Unusual movement patterns, abandoned objects, and crowd density anomalies all trigger alerts before human operators would even notice.\n\nFinGuard AI works differently. Rather than looking for known fraud patterns, it builds a behavioral baseline for every account and flags deviations. A transaction that is completely normal for one customer might be highly suspicious for another. FinGuard understands the difference.\n\nBoth products share a core design principle: the AI raises alerts, but humans make the final call. This is not a limitation — it is intentional. In security contexts, false positives have real costs, and a well-trained human combined with a well-trained AI is always more reliable than either alone.\n\nIf your organization processes sensitive financial data or manages physical security at scale, contact us to discuss a tailored deployment.',
                'author': 'AI-Solutions Team', 'category': 'AI Security', 'is_published': True, 'published_at': timezone.now() - timedelta(days=2),
            },
        ]

        count = 0
        for data in posts:
            _, created = BlogPost.objects.get_or_create(slug=data['slug'], defaults=data)
            if created:
                count += 1
        self.stdout.write(f'  → Blog posts: {BlogPost.objects.count()} total ({count} new)')

    # ──────────────────────────────────────────────
    # GALLERY IMAGES (10) — generated placeholders
    # ──────────────────────────────────────────────
    def seed_gallery(self):
        gallery_items = [
            ('AI-Solutions Office, Kathmandu', '#1B4F72', '#2E86DE', 'HQ'),
            ('HealthSync AI Dashboard', '#0d6b4f', '#22c55e', 'HS'),
            ('RetailMind Store Analytics', '#7c2d12', '#f97316', 'RM'),
            ('EduNova Learning Platform', '#581c87', '#a855f7', 'EN'),
            ('FleetPilot AI Operations Room', '#1e3a5f', '#3b82f6', 'FP'),
            ('SecureVision Monitoring Centre', '#450a0a', '#ef4444', 'SV'),
            ('AI Tech Summit 2025', '#134e4a', '#14b8a6', 'TS'),
            ('Team at Nova International College', '#1a2e05', '#84cc16', 'TC'),
            ('AI-Solutions Product Demo Day', '#0c1445', '#6366f1', 'PD'),
            ('UK Office Launch — Sunderland', '#1c1917', '#a8a29e', 'UK'),
        ]

        count = 0
        existing_titles = set(GalleryImage.objects.values_list('title', flat=True))

        for title, bg_color, accent, label in gallery_items:
            if title in existing_titles:
                continue

            img_content = self._make_svg(title, bg_color, accent, label)
            filename = title.lower().replace(' ', '-').replace(',', '').replace('—', '').replace('/', '') + '.svg'
            filename = '-'.join(filename.split())[:50] + '.svg'

            img = GalleryImage(title=title, description=f'AI-Solutions — {title}')
            img.image.save(filename, ContentFile(img_content.encode('utf-8')), save=True)
            count += 1

        self.stdout.write(f'  → Gallery: {GalleryImage.objects.count()} total ({count} new)')

    def _make_svg(self, title, bg, accent, label):
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{accent};stop-opacity:0.6" />
    </linearGradient>
  </defs>
  <rect width="800" height="600" fill="url(#bg)"/>
  <circle cx="400" cy="240" r="100" fill="{accent}" opacity="0.15"/>
  <circle cx="400" cy="240" r="70" fill="{accent}" opacity="0.2"/>
  <text x="400" y="260" font-family="Arial" font-size="64" font-weight="bold"
        fill="{accent}" text-anchor="middle" dominant-baseline="middle">{label}</text>
  <text x="400" y="380" font-family="Arial" font-size="22" font-weight="600"
        fill="white" text-anchor="middle" opacity="0.9">{title}</text>
  <text x="400" y="420" font-family="Arial" font-size="16"
        fill="white" text-anchor="middle" opacity="0.5">AI-Solutions Portfolio</text>
  <rect x="340" y="450" width="120" height="3" rx="2" fill="{accent}" opacity="0.7"/>
</svg>'''

    # ──────────────────────────────────────────────
    # CONTACT MESSAGES (10)
    # ──────────────────────────────────────────────
    def seed_contacts(self):
        contacts = [
            {'name': 'Aarav Joshi', 'email': 'aarav.joshi@techvision.com', 'phone': '+977 9801234567', 'subject': 'Interested in HealthSync AI for our clinic', 'message': 'Hello, we run a multi-speciality clinic in Kathmandu with around 50 doctors. We are very interested in deploying HealthSync AI to manage our appointment flow and patient records. Could we schedule a demo?', 'is_read': False},
            {'name': 'Samantha Clarke', 'email': 'samantha@urbanretail.co.uk', 'phone': '+44 7700900123', 'subject': 'RetailMind enquiry for UK retail chain', 'message': 'Hi there, we operate 12 stores across the UK and are looking for an analytics solution to optimise inventory and understand customer foot traffic patterns. RetailMind looks very promising.', 'is_read': False},
            {'name': 'Bikram Thapa', 'email': 'bikram.thapa@collegedu.np', 'phone': '+977 9855432100', 'subject': 'EduNova for our college — 3,000 students', 'message': 'We are a private college in Pokhara with 3,000 students across engineering and management programmes. We need an adaptive learning platform that supports Nepali language content. Is EduNova suitable?', 'is_read': True},
            {'name': 'James Harrington', 'email': 'j.harrington@swiftlogistics.com', 'phone': '+1 555 0198', 'subject': 'Fleet management AI for 200-vehicle operation', 'message': 'We manage a fleet of 200 delivery vehicles across 3 cities. Our current tracking system is outdated and we lose significant money on fuel inefficiency and poor routing. FleetPilot AI seems like exactly what we need.', 'is_read': True},
            {'name': 'Meena Pandey', 'email': 'meena@nexasecurity.com', 'phone': '+977 9841567890', 'subject': 'Security monitoring for corporate campus', 'message': 'We have a corporate campus with 15 buildings and 2,000+ employees. Our current CCTV system requires 24/7 human monitoring which is expensive and error-prone. Would SecureVision work for a campus of this scale?', 'is_read': False},
            {'name': 'Oliver Bennett', 'email': 'oliver.bennett@finnovate.io', 'phone': '+44 7911123456', 'subject': 'FinGuard AI for payment processing platform', 'message': 'We are a fintech startup processing approximately 50,000 transactions per day. Our current fraud detection flags too many false positives, frustrating legitimate customers. I would like to discuss FinGuard AI as a potential replacement.', 'is_read': False},
            {'name': 'Sunita Maharjan', 'email': 'sunita.maharjan@greenfield.np', 'phone': '+977 9823456789', 'subject': 'AgriSense AI pilot for our cooperative', 'message': 'Our farming cooperative covers 500 hectares across the Terai region. We want to improve yield predictability and reduce irrigation waste. Could AI-Solutions run a pilot project with AgriSense AI for us?', 'is_read': True},
            {'name': 'Rachel Kim', 'email': 'rachel.kim@globalcorp.com', 'phone': '+82 10 1234 5678', 'subject': 'AI virtual assistant for customer service team', 'message': 'We receive over 2,000 customer enquiries per day across email and web chat. Our support team is overwhelmed. We are interested in deploying an AI assistant like Aria to handle first-line queries. Can you share pricing information?', 'is_read': False},
            {'name': 'Thomas Muller', 'email': 't.muller@sunderland-tech.co.uk', 'phone': '+44 7800654321', 'subject': 'Partnership enquiry — Sunderland tech cluster', 'message': 'I represent a technology cluster in Sunderland with 40 member companies. I heard about your upcoming UK office and would love to explore partnership opportunities for mutual referrals and joint client projects.', 'is_read': True},
            {'name': 'Priyanka Shrestha', 'email': 'priyanka.s@hospital.gov.np', 'phone': '+977 9867890123', 'subject': 'Government hospital AI implementation enquiry', 'message': 'I am the IT Director at a government hospital in Kathmandu. We are evaluating AI solutions for our patient management system as part of a digital health initiative. We have strict data residency requirements. Could AI-Solutions accommodate an on-premise deployment of HealthSync AI?', 'is_read': False},
        ]

        count = 0
        for data in contacts:
            existing = ContactMessage.objects.filter(email=data['email'], subject=data['subject']).first()
            if not existing:
                ContactMessage.objects.create(**data)
                count += 1

        self.stdout.write(f'  → Contacts: {ContactMessage.objects.count()} total ({count} new)')

    # ──────────────────────────────────────────────
    # SITE SETTINGS
    # ──────────────────────────────────────────────
    def seed_settings(self):
        SiteSettings.objects.get_or_create(pk=1, defaults={
            'site_name': 'AI-Solutions',
            'tagline': 'Innovate | Support | Empower',
            'email': 'hello@ai-solutions.com',
            'phone': '+977 98XXXXXXXX',
            'address': 'Tinkune, Kathmandu, Nepal',
            'time_zone': 'Asia/Kathmandu',
        })
        self.stdout.write('  → Site settings ready')

from django.db import models
from django.utils import timezone


# ─── Service Offerings (what the company provides) ────────────
class ServiceOffering(models.Model):
    ICON_CHOICES = [
        ('bi-robot',           'AI / Robot'),
        ('bi-gear-wide-connected', 'Automation'),
        ('bi-bar-chart-line',  'Analytics'),
        ('bi-shield-check',    'Security'),
        ('bi-chat-dots',       'Chatbot'),
        ('bi-cpu',             'Custom AI'),
        ('bi-cloud-upload',    'Cloud'),
        ('bi-diagram-3',       'Integration'),
    ]

    title       = models.CharField(max_length=200)
    subtitle    = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    icon        = models.CharField(max_length=100, default='bi-robot')
    image       = models.ImageField(upload_to='service_offerings/', blank=True, null=True)
    features    = models.JSONField(default=list)
    highlight   = models.CharField(max_length=100, blank=True, help_text='Short badge text, e.g. "Most Popular"')
    is_active   = models.BooleanField(default=True)
    order       = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Service Offering'
        verbose_name_plural = 'Service Offerings'

    def __str__(self):
        return self.title


# ─── Service / Portfolio ──────────────────────────────────────
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('healthcare', 'Healthcare'),
        ('retail', 'Retail & Commerce'),
        ('education', 'Education'),
        ('logistics', 'Logistics & Transport'),
        ('security', 'Security & Surveillance'),
        ('other', 'Other'),
    ]

    TYPE_SERVICE   = 'service'
    TYPE_PORTFOLIO = 'portfolio'
    TYPE_CHOICES = [
        (TYPE_SERVICE,   'Service Offering'),
        (TYPE_PORTFOLIO, 'Portfolio Project'),
    ]

    record_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default=TYPE_SERVICE,
        help_text='Service Offering = what we provide. Portfolio Project = past client work.'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    features = models.JSONField(default=list)
    icon = models.CharField(max_length=100, default='bi-gear')
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    client_name = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Service / Portfolio'
        verbose_name_plural = 'Services / Portfolio'

    def __str__(self):
        return self.title


# ─── Proxy models for split admin views ───────────────────────
class ServiceOffering(Service):
    """Proxy — shows only Service Offerings in admin."""
    class Meta:
        proxy = True
        verbose_name = 'Service Offering'
        verbose_name_plural = 'Service Offerings'


class PortfolioProject(Service):
    """Proxy — shows only Portfolio Projects in admin."""
    class Meta:
        proxy = True
        verbose_name = 'Portfolio Project'
        verbose_name_plural = 'Portfolio Projects'


# ─── Customer Testimonials ────────────────────────────────────
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    project_name = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating', '-created_at']
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return f"{self.name} — {self.company}"


# ─── Blog Posts ───────────────────────────────────────────────
class BlogPost(models.Model):
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    excerpt = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.CharField(max_length=100, default='AI-Solutions Team')
    category = models.CharField(max_length=100, blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


# ─── Gallery Images ───────────────────────────────────────────
class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/')
    description = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'

    def __str__(self):
        return self.title


# ─── Events Timeline ──────────────────────────────────────────
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f"{self.title} — {self.date}"


# ─── Contact Messages ─────────────────────────────────────────
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    job_details = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} — {self.company}"


# ─── Site Settings (singleton — only 1 row ever) ─────────────
class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='AI-Solutions')
    tagline = models.CharField(max_length=200, default='Innovate | Support | Empower')
    logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    email = models.EmailField(default='student.helpline@sunderland.ac.uk')
    phone = models.CharField(max_length=20, blank=True, default='+44 191 515 3000')
    address = models.TextField(blank=True, default='Chester Road, Sunderland, United Kingdom, SR1 3SD')
    time_zone = models.CharField(max_length=50, default='Asia/Kathmandu')
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

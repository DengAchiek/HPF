from django.db import models
from django.templatetags.static import static
from django.urls import NoReverseMatch, reverse


class ActiveOrderedModel(models.Model):
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ("sort_order", "id")


class ImageMixin(models.Model):
    image = models.FileField(upload_to="cms/", blank=True)
    static_image = models.CharField(
        max_length=255,
        blank=True,
        help_text="Optional static image path, for example images/im-01.jpeg.",
    )
    image_alt = models.CharField(max_length=255, blank=True)

    class Meta:
        abstract = True

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        if self.static_image:
            return static(self.static_image)
        return ""


class LinkMixin(models.Model):
    button_label = models.CharField(max_length=120, blank=True)
    button_url_name = models.CharField(
        max_length=80,
        blank=True,
        help_text="Named Django route, for example projects, contact, donate.",
    )
    button_external_url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Full URL or mailto/tel link. Used when route name is blank.",
    )

    class Meta:
        abstract = True

    @property
    def button_href(self):
        if self.button_url_name:
            try:
                return reverse(self.button_url_name)
            except NoReverseMatch:
                return "#"
        return self.button_external_url or "#"


class SiteSettings(models.Model):
    singleton_key = models.CharField(max_length=32, unique=True, default="main", editable=False)
    organization_name = models.CharField(max_length=160, default="Health Planet Foundation")
    tagline = models.CharField(
        max_length=220,
        blank=True,
        default="Sustainable environment, Healthy communities, Future generations",
    )
    footer_about = models.TextField(blank=True)
    focus_dropdown_label = models.CharField(max_length=80, default="Focus Areas")
    logo = models.FileField(upload_to="branding/", blank=True)
    static_logo = models.CharField(max_length=255, blank=True, default="images/HPF-logo.jpeg")
    contact_name = models.CharField(max_length=160, blank=True)
    location = models.CharField(max_length=160, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    copyright_text = models.CharField(max_length=180, blank=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.organization_name

    @classmethod
    def load(cls):
        return cls.objects.first() or cls()

    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        if self.static_logo:
            return static(self.static_logo)
        return ""


class NavigationItem(ActiveOrderedModel):
    label = models.CharField(max_length=80)
    url_name = models.CharField(max_length=80, blank=True)
    external_url = models.CharField(max_length=255, blank=True)
    is_cta = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    @property
    def href(self):
        if self.url_name:
            try:
                return reverse(self.url_name)
            except NoReverseMatch:
                return "#"
        return self.external_url or "#"


class FooterLink(ActiveOrderedModel):
    GROUP_PROGRAMS = "programs"
    GROUP_ORGANIZATION = "organization"
    GROUP_CONTACT = "contact"
    GROUP_CHOICES = (
        (GROUP_PROGRAMS, "Programs"),
        (GROUP_ORGANIZATION, "Organization"),
        (GROUP_CONTACT, "Contact"),
    )

    group = models.CharField(max_length=32, choices=GROUP_CHOICES)
    label = models.CharField(max_length=120)
    url_name = models.CharField(max_length=80, blank=True)
    external_url = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.get_group_display()} - {self.label}"

    @property
    def href(self):
        if self.url_name:
            try:
                return reverse(self.url_name)
            except NoReverseMatch:
                return "#"
        return self.external_url or "#"


class PageContent(ImageMixin):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=160)
    meta_title = models.CharField(max_length=180, blank=True)
    hero_class = models.CharField(max_length=80, blank=True)
    hero_kicker = models.CharField(max_length=120, blank=True)
    hero_title = models.CharField(max_length=220)
    hero_text = models.TextField(blank=True)

    class Meta:
        ordering = ("slug",)
        verbose_name = "Page content"
        verbose_name_plural = "Page content"

    def __str__(self):
        return self.title


class SectionContent(ImageMixin, LinkMixin):
    page_slug = models.SlugField()
    key = models.SlugField(help_text="Template key, for example home_features or about_team.")
    kicker = models.CharField(max_length=120, blank=True)
    title = models.CharField(max_length=220, blank=True)
    body = models.TextField(blank=True)
    image_caption = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ("page_slug", "key")
        constraints = [
            models.UniqueConstraint(fields=("page_slug", "key"), name="unique_section_per_page")
        ]

    def __str__(self):
        return f"{self.page_slug}: {self.key}"


class FeatureCard(ActiveOrderedModel):
    section_key = models.SlugField(default="home_features")
    icon = models.CharField(max_length=12, blank=True)
    title = models.CharField(max_length=160)
    body = models.TextField()

    def __str__(self):
        return self.title


class StatItem(ActiveOrderedModel):
    label = models.CharField(max_length=80)
    value = models.CharField(max_length=40)
    description = models.CharField(max_length=160)

    def __str__(self):
        return f"{self.label}: {self.value}"


class Project(ImageMixin, ActiveOrderedModel):
    title = models.CharField(max_length=160)
    description = models.TextField()
    status = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.title


class NewsItem(ImageMixin, ActiveOrderedModel):
    title = models.CharField(max_length=180)
    date_label = models.CharField(max_length=80, blank=True)
    summary = models.TextField()

    def __str__(self):
        return self.title


class GalleryImage(ImageMixin, ActiveOrderedModel):
    gallery_key = models.SlugField(default="home_gallery")
    caption = models.CharField(max_length=120, blank=True)
    focus_class = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.caption or self.static_image or self.image.name


class PartnerLogo(GalleryImage):
    class Meta:
        proxy = True
        verbose_name = "Home partner logo"
        verbose_name_plural = "Home partner logos"


class TeamMember(ActiveOrderedModel):
    TEAM_MANAGEMENT = "management"
    TEAM_BOARD = "board"
    TEAM_CHOICES = (
        (TEAM_MANAGEMENT, "Management Team"),
        (TEAM_BOARD, "Board of Directors"),
    )

    team = models.CharField(max_length=24, choices=TEAM_CHOICES)
    name = models.CharField(max_length=140)
    role = models.CharField(max_length=140)
    bio = models.TextField()
    initials = models.CharField(max_length=8, blank=True)
    photo = models.FileField(upload_to="staff/", blank=True)
    static_photo = models.CharField(max_length=255, blank=True)
    photo_alt = models.CharField(max_length=180, blank=True)
    photo_pending = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def photo_url(self):
        if self.photo:
            return self.photo.url
        if self.static_photo:
            return static(self.static_photo)
        return ""

    @property
    def display_initials(self):
        if self.initials:
            return self.initials
        return "".join(part[:1] for part in self.name.split()[:2]).upper()


class FocusArea(ImageMixin, ActiveOrderedModel):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=160)
    kicker = models.CharField(max_length=80, default="Focus area")
    summary = models.TextField()
    priority_kicker = models.CharField(max_length=120, default="Program priority")
    priority_title = models.CharField(
        max_length=180,
        default="Practical action built around community needs.",
    )
    points_text = models.TextField(
        blank=True,
        help_text="One priority per line.",
    )

    def __str__(self):
        return self.title

    @property
    def points(self):
        return [point.strip() for point in self.points_text.splitlines() if point.strip()]


class CareerOpening(ActiveOrderedModel):
    role = models.CharField(max_length=140)
    location = models.CharField(max_length=120)
    employment_type = models.CharField(max_length=80)

    def __str__(self):
        return self.role


class InternshipTrack(ActiveOrderedModel):
    role = models.CharField(max_length=140)
    focus = models.TextField()
    icon = models.CharField(max_length=12, default="IN")

    def __str__(self):
        return self.role


class DonationAmount(ActiveOrderedModel):
    amount = models.CharField(max_length=40)
    label = models.CharField(max_length=120)
    select_value = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.amount} - {self.label}"

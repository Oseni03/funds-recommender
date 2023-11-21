import hashid_field
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.utils.text import slugify


# Create your models here.
class OpportunityCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, unique=True)
    abbrv = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ApplicantType(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FundEligibility(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Agency(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    seed = models.CharField(max_length=20)
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FundingInstrument(models.Model):
    abbrv = models.CharField(max_length=10)
    description = models.CharField(max_length=150)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return str(self.description)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FundingActivityCategory(models.Model):
    abbrv = models.CharField(max_length=10)
    description = models.CharField(max_length=150)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return str(self.description)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Synopsis(models.Model):
    opportunity_id = models.CharField(max_length=25)
    agency_code = models.CharField(max_length=25)
    agency_name = models.CharField(max_length=150)
    agency_phone = models.CharField(max_length=20)
    agency_address_desc = models.CharField(max_length=255)
    agency_detail = models.ForeignKey(
        Agency, on_delete=models.PROTECT, related_name="synopsises"
    )
    top_agency_detail = models.ForeignKey(Agency, on_delete=models.PROTECT)
    agency_contact_phone = models.CharField(max_length=20)
    agency_contact_name = models.CharField(max_length=150)
    agency_contact_desc = models.CharField(max_length=255)
    agency_contact_email = models.CharField(max_length=255)
    description = models.TextField()
    response_date = models.DateTimeField()
    posting_date = models.DateTimeField()
    archive_date = models.DateTimeField()
    cost_sharing = models.BooleanField()
    award_ceiling = models.BigIntegerField()
    award_ceiling_formatted = models.CharField(max_length=100)
    award_floor = models.BigIntegerField()
    award_floor_formatted = models.CharField(max_length=100)
    applicant_eligibilty_desc = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()

    applicant_types = models.ManyToManyField("ApplicantType")
    funding_instruements = models.ManyToManyField("FundingInstrument")
    funding_activity_categories = models.ManyToManyField(
        "FundingActivityCategory", related_name="synopsis"
    )


class CFDA(models.Model):
    identifier = models.PositiveBigIntegerField()
    number = models.CharField(max_length=25)
    program_title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return str(self.program_title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.program_title)
        super().save(*args, **kwargs)


class FundProfile(models.Model):
    id = hashid_field.HashidAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    matches = models.ManyToManyField(
        "Fund", related_name="profiles", through="Recommendation"
    )
    location = models.CharField(max_length=255, help_text=_("Your geographic scope"))
    objectives = models.TextField(help_text=_("Your mission and goals"))
    applicant_type = models.ForeignKey(ApplicantType, on_delete=models.PROTECT)
    opportunity_category = models.ForeignKey(
        OpportunityCategory, on_delete=models.PROTECT
    )
    eligibility = models.ForeignKey(FundEligibility, on_delete=models.PROTECT)
    estimated_budget = models.DecimalField(max_digits=15, decimal_places=2)
    background = models.TextField(help_text=_("Little about your history"))
    project_summary = models.TextField(help_text=_("Describe the problem to be solved"))
    summary = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class FundManager(BaseUserManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "agency", "applicant_type", "eligibility", "opportunity_category"
            )
            .all()
        )


class Fund(models.Model):
    id = hashid_field.HashidAutoField(primary_key=True)
    opportunity_title = models.CharField(max_length=255)
    agency = models.ForeignKey(Agency, on_delete=models.PROTECT, related_name="funds")
    top_agency = models.ForeignKey(Agency, on_delete=models.PROTECT)
    opportunity_number = models.CharField(max_length=15, unique=True)
    applicant_type = models.ForeignKey(
        ApplicantType, on_delete=models.PROTECT, related_name="funds"
    )
    cfdas = models.ManyToManyField("CFDA", related_name="funds")
    eligibility = models.ForeignKey(
        FundEligibility, on_delete=models.PROTECT, related_name="funds"
    )
    opportunity_category = models.ForeignKey(
        OpportunityCategory, on_delete=models.PROTECT, related_name="funds"
    )
    synopsis = models.ForeignKey(Synopsis, on_delete=models.CASCADE)
    expected_award_no = models.IntegerField()
    eligibility_info = models.TextField()
    description = models.TextField()
    summary = models.TextField(null=True)
    url = models.URLField()
    slug = models.SlugField(null=True, unique=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = FundManager()

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("funds:fund", args=(self.slug,))


class Recommendation(models.Model):
    profile = models.ForeignKey(FundProfile, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["profile", "fund"],
                name="unique_profile_fund",
            ),
        ]

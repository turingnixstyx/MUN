from django.db import models

# Create your models here.


class Challenge(models.Model):
    name = models.CharField(max_length=255, unique=True)
    short_description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Committee(models.Model):
    name = models.CharField(max_length=255, unique=True)
    challenge = models.ForeignKey(
        Challenge,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="committee_to_challenge"
    )

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    name = models.CharField(max_length=255, unique=True)
    committee = models.ForeignKey(
        Committee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="portfolio_to_committee"
    )

    def to_dict(self):
        return {
            'name': self.name,
            'committee': self.committee.name if self.committee else None
        }

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-name']


class SubPortfolio(Portfolio):
    class Meta:
        proxy = True

from django.db import models


class Instrument(models.Model):
    # TODO: Define fields here
    INSTRUMENT_TYPES = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

    instrument_type = models.ModelChoiceField()

    class Meta:
        verbose_name = "Instrument"
        verbose_name_plural = "Instruments"

    def __str__(self):
        pass

    def save(self):
        pass

    @models.permalink
    def get_absolute_url(self):
        return ('')

    # TODO: Define custom methods here

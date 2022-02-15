from django.db import models

# Create your models here.

class Country(models.Model):
    """
    Table used to store references about a countries name and their related alpha-2 code as well as their
    currency code.
    # NOTE:
        To be used later in the retrieval of the exchange rates
    """

    name = models.CharField(max_length=128)
    currency_code = models.CharField(max_length=8)
    alpha_code = models.CharField(max_length=8)


class ExchangeRateHolder(models.Model):
    """
    Table used to temoporarily store the exchange rates for specific countries
    This is being made use in order to mitigate the effects of hitting the exchange rate API
    """

    begin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="exchange_from")
    to = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="exchange_to")
    created = models.DateTimeField(auto_now_add=True)

class Records(models.Model):
    """
    Table to store the actual records that are needed in the task
    """

    PURCHASE_TYPE = "PURCHASE"
    SALE_TYPE = "SALE"

    TYPE_CHOICES = (
        (PURCHASE_TYPE, "Purchase"),
        (SALE_TYPE, "Sale"),
    )

    date = models.DateTimeField()
    type = models.CharField(max_length=12, choices=TYPE_CHOICES)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="records_country")
    currency = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="records_currency") # NOTE: This is a bit of a weird one that was inadvertantly created due to my Country table.
    net = models.DecimalField(decimal_places=2, max_digits=16)
    vat = models.DecimalField(decimal_places=2, max_digits=16)

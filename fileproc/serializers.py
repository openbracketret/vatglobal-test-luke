from rest_framework import serializers

from fileproc.models import Records

class RecordSerializer(serializers.ModelSerializer):


    def get_country(self, instance):
        return instance.country.name

    def get_currency(self, instance):
        return instance.currency.currency_code


    class Meta:
        model = Records
        fields = ('date', 'type', 'currency', 'country', 'net', 'vat')
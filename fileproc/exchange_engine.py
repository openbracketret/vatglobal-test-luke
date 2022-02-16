
from fileproc.models import ExchangeRateHolder, Country
import datetime
import requests

class ExchangeRateAPI():
    """
    The class that will connect to the exchange API and return the values which are passing in
    """

    def __init__(self):
        """
        Init function
        """
        self.base_url = 'http://'
        

    def get_conversion_rate(self, currency_from, currency_to):
        """
        Function to make a request to the exchange API and return the exchange rate for those two
        specific countries

        Params
        --------
        currency_from (string): The currency code for the FROM currency
        currency_to (string): The currency code for the TO currency

        Returns
        ---------
        exchange_rate (float): The exchange rate that can be used for basic multiplication
        """

        # TODO: Figure out how the API works and make this return meaningful information
        return 1.0


class ExchangeRateManager():
    """
    This class will be used to take in a set of jobs if they need their values to be
    converted to a specific currency.
    It will manage the use of hitting the EU exchange API as well as the use of the 
    ExchangeRateHolder model
    """

    def __init__(self, records):
        """
        Init function
        Params
        -------
        Records (Queryset<Records>): The records that need to be converted
        """
        self.records = records
        self.__clear_old_holders()

    def process_exchange_rate(self, currency_code):
        """
        Used as the main function that will convert all of the records values based on their current
        country and the requested currency

        Params
        ----------
        currency_code (String): The currency being requested to convert to

        Returns
        ---------
        records (dict): A dictionary of the processed records
        """

        currency_country = Country.objects.get(currency_code=currency_code)

        # Now we need to know of the set of possibilities for convertions
        record_currencies = list(set([x.currency.currency_code for x in self.records]))
        # Now delete my NONE country
        record_currencies.remove("NONE")

        # Now we need to collect the records for ExchangeRateHolder
        exchange_rates = self.__collect_needed_exchange_rates(currency_code, record_currencies)

        # We always know what TO currency we are going to be needing, it is just a matter
        # of mapping the FROM currency for the correct multiplcation
        rate_map = dict()
        for item in exchange_rates:
            rate_map[item.begin.currency_code] = item.rate

        returner = self.records.values()
        for item in returner:

            # Set the country to be the actual name of the country instead of just the id
            item["country_id"] = Country.objects.get(id=item["country_id"]).name
            # Currency will always be the requested currency now?
            item["currency_id"] = Country.objects.get(id=item["country_id"]).currency_code

            item["net"] = item["net"] * rate_map[item["currency_id"]]
            item["vat"] = item["vat"] * rate_map[item["currency_id"]]

        return returner

    def __clear_old_holders(self):
        """
        Private function to clear all exchange rate holders that are older than 30 minutes
        """
        now = datetime.datetime.now() - datetime.timedelta(minutes=30)
        ExchangeRateHolder.objects.filter(created__gt=now).delete()
        return

    def __collect_needed_exchange_rates(self, currency_code_to, from_codes):
        """
        Private function to process the needed exchange rates

        Params
        --------
        currency_code_to (string): The currency code to which we are converting
        from_codes (list<string>): The currency codes FROM which we are converting

        Returns
        --------
        exchange_rates (Queryset<ExchangeRateHolder>): The exchange rates requested
        """

        api = ExchangeRateAPI()

        # Store the original from_codes in order to make the return at the end work
        orig_from_codes = from_codes

        # We don't want to fetch exchange rates that we already have to let's remove those from the
        # from_codes variable
        already_have = ExchangeRateHolder.objects.filter(
            begin__currency_code__in=from_codes,
            to__currency_code=currency_code_to
        )

        already_have_codes = list(set([x.begin.currency_code for x in already_have]))

        for code in already_have_codes:
            from_codes.remove(code)


        # Now we collect the exchange rates only for those that we need
        for code in from_codes:
            rate = api.get_conversion_rate(code, currency_code_to)

            ExchangeRateHolder.objects.create(
                begin=Country.objects.get(currency_code=code),
                to=Country.objects.get(currency_code=currency_code_to),
                rate=rate
            )

        return ExchangeRateHolder.objects.filter(
            begin__currency_code__in=orig_from_codes,
            to__currency_code=currency_code_to
        )







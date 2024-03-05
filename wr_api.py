from decouple import config
from wikirate4py import API


class WikirateAPI:
    '''
    Class to handle data fetching from the Wikirate API.
    '''

    def __init__(self, api_key: str):
        '''
        Initialize the class with an API key.

        Args:
            api_key (str): The API key for authentication.
        '''
        self.api = API(api_key)

    def get_metric(self, metric_id):
        return self.api.get_metric(metric_id)

    def get_metrics(self, metric_designer=None):
        '''
        Fetch metrics, optionally filtered by a metric designer.

        Args:
            metric_designer (str, optional): The designer of the metrics to
            filter by. Defaults to None.

        Returns:
            Response from the API.
        '''
        return self.api.get_metrics(designer=metric_designer)

    def get_answer(self, answer_id):
        return self.api.get_answer(answer_id)

    def get_answers(self, metric_designer, metric_name):
        return self.api.get_answers(metric_designer=metric_designer, metric_name=metric_name)


wr_api = WikirateAPI(config('WR_API_KEY'))
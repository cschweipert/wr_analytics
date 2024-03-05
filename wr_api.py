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

    def get_metrics(self, limit, offset, metric_designer=None):
        '''
        Fetch metrics, optionally filtered by a metric designer.

        Args:
            metric_designer (str, optional): The designer of the metrics to
            filter by. Defaults to None.

        Returns:
            Response from the API.
        '''
        return self.api.get_metrics(
            limit=limit,
            offset=offset,
            designer=metric_designer)

    def get_answer(self, answer_id):
        return self.api.get_answer(answer_id)

    def get_answers(self,
                    limit,
                    offset,
                    metric_name, metric_designer):
        return self.api.get_answers(
            limit=limit,
            offset=offset,
            metric_name=metric_name,
            metric_designer=metric_designer)


wr_api = WikirateAPI(config('WR_API_KEY'))

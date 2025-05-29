import pandas as pd


class OrganizationDataService:
    def __init__(self):
        # load the data
        self.data = pd.DataFrame()  # Placeholder for actual data loading logic
        pass

    def get_data(self,params):
        '''
        
        Filter the data based on the params
        :param params:
        {
        'filter':{'company_id': 10} // where
        'groupby': [list of columns ]
        'orderby': {col_name:asc|desc} // order by
        'limit': 500,
        'data_range': 'last 6months | last 12months | last 24months | all',
        }
        :return:
        '''
        pass

#from create_portfolio
'''def total_portfolio_risk(self):
     self.environment['Weighted_risk'] = (self.environment['Value_per_stock']/sum(self.environment['Value_per_stock']))*self.environment['Risk']*len(self.environment)
     total_portfolio_risk = sum(self.environment['Weighted_risk'])/len(self.environment)
     return total_portfolio_risk'''

'''def capital_check(self, begin_portfolio):
    portfolio_value_start = round(sum(begin_portfolio['Value_per_stock']), 2)
    portfolio_value_now = round(sum(self.environment['Value_per_stock']), 2)
    rest_value = portfolio_value_start - portfolio_value_now
    if rest_value != 0:
        i = randrange(20)
        self.environment.Value_per_stock.iloc[i] = self.environment.Value_per_stock.iloc[i] + rest_value
    else:
        print('Risk Check Complete!')'''
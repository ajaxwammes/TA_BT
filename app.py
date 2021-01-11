from flask import Flask, request, jsonify
import pandas as pd
from services.create_portfolio import PortfolioCreator
from services.withdraw_deposit import DepositWithdrawer


app = Flask(__name__)

anything = []

@app.route('/api/withdraw_deposit', methods = ['POST'])
def withdraw_deposit():
    begin_portfolio = pd.read_csv('./data/post_creation.csv')
    content = request.json
    customerID = content['customerID']
    money_delta = content['money_delta']
    dw_obj = DepositWithdrawer(begin_portfolio)
    result = dw_obj.run(begin_portfolio=begin_portfolio,
                        money_delta=money_delta)
    anything.append(list(result['Company']))
    return jsonify('')

@app.route('/api/create_portfolio', methods = ['POST'])
def create_portfolio():
    all_products = pd.read_csv('./data/Portfolio.csv')
    content = request.json
    fresh_environment = all_products[all_products.Industry.isin(content['choices'])]
    customerID = content['customerID']
    risk_level = content['risk_level']
    money_in_portfolio = content['money_in_portfolio']
    pc_obj = PortfolioCreator(fresh_environment)
    result = pc_obj.run(money_in_portfolio=money_in_portfolio,
                        risk_level=risk_level,
                        all_products=all_products).reset_index(drop=True)
    anything.append(list(result['Value_per_stock']))
    return jsonify('')

@app.route('/api/show', methods = ['GET'])
def show():
    return jsonify(anything)



if __name__ == '__main__':
    app.run(port=5000)
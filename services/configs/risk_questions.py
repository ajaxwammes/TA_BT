#question 1: age
#no drop-down, does not allow values under 18 (years old)
"""
Between 18 - 30: 3
Between 31 - 45: 2
Between 46 - 60: 1
Older or equal to 61: 0
"""

#question 2: investment amount
#no drop-down, does not allow values under 10 (USD)
#no points allocated at this question, but is an individual input for create_portfolio.py


#question 3: how much % of my wealth I want to invest?
#no drop-down
'''
Between 0% - 25%: 3
Between 26% - 50%: 2
Between 51% - 75%: 1
Between 76% - 100%: 0
'''


#question 4: my main motivation for investing is:?
#drop-down answers:
q3 = {'Get more out of my savings': 2,
      'Build extra income for retirement': 3,
      'Save extra for university': 1,
      "Save extra for an emergency": 0,
      "I don't know yet": 2
      }


'''
points - final risk level (so when total score is 2, risk level should be 1)
0-1: 0
2-3: 1
4-5: 2
6-7: 3
8-9: 4
'''


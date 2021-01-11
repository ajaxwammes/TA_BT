try:
    from services.assess_risk import RiskAssessor
except ModuleNotFoundError as ex:
    import sys
    sys.path.append('./')
    from services.assess_risk import RiskAssessor

if __name__ == "__main__":
    #INPUT
    CustomerID = 1001
    q1_answer = '80%'
    q2_answer = 'Between 5 and 10 years'
    q3_answer = 'Pension'
    q4_answer = 'No'

    ra_obj = RiskAssessor()
    result = ra_obj.get_risk_level(q1_answer=q1_answer,
                          q2_answer=q2_answer,
                          q3_answer=q3_answer,
                          q4_answer=q4_answer)
    print(result)
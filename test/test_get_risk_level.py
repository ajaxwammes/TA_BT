try:
    from services.utils import risk_assessment
except ModuleNotFoundError as ex:
    import sys
    sys.path.append('./')
    from services.utils import risk_assessment

q1_answer = '20%'
q2_answer = 'Between 5 and 10 years'
q3_answer = 'Pension'
q4_answer = 'No'

score_q1 = risk_assessment.q1[q1_answer]
score_q2 = risk_assessment.q2[q2_answer]
score_q3 = risk_assessment.q3[q3_answer]
score_q4 = risk_assessment.q4[q4_answer]

if __name__ == '__main__':
    total_score = score_q1 + score_q2 + score_q3 + score_q4
    res_key, res_val = min(risk_assessment.risk.items(), key=lambda x: abs(total_score - x[1]))
    print(res_key)



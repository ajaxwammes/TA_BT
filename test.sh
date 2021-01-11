##example call for deposit / withdraw
#curl \
#-H "Content-Type: application/json" \
#-X POST \
#-d '{
#"customerID" : 1001,
#"money_delta" : 200
#}' \
#http://127.0.0.1:5000/api/withdraw_deposit


##example call for create portfolio
#curl \
#-H "Content-Type: application/json" \
#-X POST \
#-d '{
#"choices": [
#  "Renewable energy",
#  "Clean water and oceans",
#  "Circular economy",
#  "Transportation of the future",
#  "Energy-saving technology",
#  "Plant-based food",
#  "Overall sustainability"
#],
#"customerID" : 1001,
#"risk_level" : 2,
#"money_in_portfolio" : 10000
#}' \
#http://127.0.0.1:5000/api/create_portfolio


#example call for risk assessment
curl \
-H "Content-Type: application/json" \
-X POST \
-d '{
"customerID" : "1001",
"q1_answer" : "80%",
"q2_answer" : "Between 5 and 10 years",
"q3_answer" : "Pension",
"q4_answer" : "No"
}' \
http://127.0.0.1:5000/api/assess_risk
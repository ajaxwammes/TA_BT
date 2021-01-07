curl \
-H "Content-Type: application/json" \
-X POST \
-d '{
"customerID" : 1001,
"money_delta" : 200
}' \
http://127.0.0.1:5000/api/withdraw_deposit


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




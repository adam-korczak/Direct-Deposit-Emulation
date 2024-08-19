import requests
import csv
import json

headers = {
    "Authorization": f"Bearer {bearer_token}"
}

#using pagination on new foreign key for each table to reach specific data we're looking for 
def fetch_payments(date):
    payments = []
    continuation_token = "START"
    
    while continuation_token != "END":
        url = f"{base_url}/payments?date={date}&continuationToken={continuation_token}"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            payments.append(data)
            continuation_token = data.get("paginationToken", "END")
        else:
            print(f"Failed to fetch payments: {response.status_code} - {response.text}")
            break
    
    return payments

def fetch_customer(bank_account_id):
    url = f"{base_url}/customers?bankAccountId={bank_account_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('data', {})
    else:
        print(f"Failed to fetch customer: {response.status_code} - {response.text}")
        return None

def fetch_loans(username):
    url = f"{base_url}/loans/{username}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Failed to fetch loans: {response.status_code} - {response.text}")
        return []

def process_payments(payments):
    processed_payments = []

    for payment in payments:
        bank_account_id = payment.get("bankAccountId")
        amount = payment.get("amount")
        
        customer = fetch_customer(bank_account_id)
        
        if not customer:
            continue
        
        username = customer.get("username")
        loans = fetch_loans(username)
        
        if loans:
            for loan in loans:
                if loan['status'] == "OPEN":
                    loan_id = loan["loanId"]
                    balance = loan["balance"]
                    expected_payment_amount = loan["expectedPaymentAmount"]
                    
                    amount_applied = min(amount, balance)
                    amount_reimbursed = round(max(0, amount - balance), 2)

                    
                    processed_payments.append({
                        "username": username,
                        "loanId": loan_id,
                        "amountApplied": amount_applied,
                        "amountReimbursed": amount_reimbursed
                    })
                    
                    break
        else:
            processed_payments.append({
                "username": username,
                "loanId": "",
                "amountApplied": 0,
                "amountReimbursed": amount
            })
    
    return processed_payments

def generate_csv(processed_payments):
    with open('processedPayments.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "loanId", "amountApplied", "amountReimbursed"])
        writer.writeheader()
        writer.writerows(processed_payments)

def main(date):
    payments = fetch_payments(date)
    processed_payments = process_payments(payments)
    generate_csv(processed_payments)

if __name__ == "__main__":
    date = input('Enter a date in YYYY-MM-DD format from "2024-06-14 to 2024-06-28: ')
    main(date)

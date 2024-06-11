
from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

@app.route('/')
def get_transactions():
    return render_template("transactions.html", transactions = transactions)



@app.route('/add', methods =['GET', 'POST'])
def add_transaction():

    if request.method == "GET":
        return render_template("form.html")
    if request.method == "POST":
        transact = {
            'id': len(transactions)+1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
        transactions.append(transact)
        return redirect(url_for('get_transactions'))



# Update operation
@app.route('/edit/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    if request.method == "GET":
        for tran in transactions:
            if tran['id'] == transaction_id:
                return render_template("edit.html", transaction = tran)
    if request.method == "POST":
        new_date = request.form['date']
        new_amount = float(request.form['amount'])
        for tran in transactions:
            if tran['id'] == transaction_id:
                tran['date'] = new_date
                tran['amount'] = new_amount
                break
        return redirect(url_for('get_transactions'))


# Delete operation
@app.route('/delete/<int:transaction_id>', methods=['GET'])
def delete_transaction(transaction_id):
    for tran in transactions:
        if tran['id'] == transaction_id:
            transactions.remove(tran)
    return redirect(url_for('get_transactions'))


@app.route('/search', methods=['GET', 'POST'])
def search_transactions():
    if request.method == "POST":
        minimum = float(request.form['min_amount'])
        maximum = float(request.form['max_amount'])
        filtered_trans=[]
        for tran in transactions:
            if (tran['amount'] <= maximum) and (tran['amount'] >= minimum):
                filtered_trans.append(tran)
        return render_template("transactions.html", transactions = filtered_trans)
    if request.method == "GET":
        return render_template("search.html")



@app.route('/balance')
def total_balance():
    total_bal = 0
    for tran in transactions:
        total_bal += float(tran['amount'])
    output = f"Total balance: {total_bal}"
    return render_template("transactions.html", transactions = transactions, total_balance=output)
# Run the Flask app

if __name__ == "__main__":
    app.run(debug=True)
    
    
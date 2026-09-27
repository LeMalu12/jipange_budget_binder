from flask import Flask, render_template, request, redirect, url_for
from database import get_db_connection, init_db, seed_portfolios

app = Flask(__name__)


# Create database tables
init_db()

# Add starting portfolios if they do not already exist
seed_portfolios()


@app.route("/")
def home():
    connection = get_db_connection()

    portfolios = connection.execute(
        "SELECT * FROM portfolios"
    ).fetchall()

    transactions = connection.execute(
        """
        SELECT * FROM transactions
        ORDER BY created_at DESC, id DESC
        """
    ).fetchall()

    connection.close()

    total_balance = sum(
        portfolio["balance"] for portfolio in portfolios
    )

    flexible_balance = next(
        (
            portfolio["balance"]
            for portfolio in portfolios
            if portfolio["name"] == "Flexible"
        ),
        0
    )

    committed_balance = total_balance - flexible_balance

    return render_template(
        "index.html",
        portfolios=portfolios,
        transactions=transactions,
        total_balance=total_balance,
        committed_balance=committed_balance,
        flexible_balance=flexible_balance
    )

@app.route("/add-transaction", methods=["POST"])
def add_transaction():

    description = request.form["description"].strip()
    amount = float(request.form["amount"])
    category = request.form["category"]

    connection = get_db_connection()

    portfolio = connection.execute(
        "SELECT * FROM portfolios WHERE name = ?",
        (category,)
    ).fetchone()

    if portfolio and amount > 0 and amount <= portfolio["balance"]:

        new_balance = portfolio["balance"] - amount

        connection.execute(
            """
            UPDATE portfolios
            SET balance = ?
            WHERE name = ?
            """,
            (new_balance, category)
        )

        connection.execute(
            """
            INSERT INTO transactions
            (description, amount, category)
            VALUES (?, ?, ?)
            """,
            (description, amount, category)
        )

        connection.commit()

    connection.close()

    return redirect(url_for("home"))

@app.route("/add-portfolio", methods=["POST"])
def add_portfolio():

    name = request.form["name"].strip()

    if name:

        connection = get_db_connection()

        existing = connection.execute(
            "SELECT * FROM portfolios WHERE name = ?",
            (name,)
        ).fetchone()

        if not existing:

            connection.execute(
                """
                INSERT INTO portfolios (name, balance)
                VALUES (?, 0)
                """,
                (name,)
            )

            connection.commit()

        connection.close()

    return redirect(url_for("home"))

@app.route("/allocate-money", methods=["POST"])
def allocate_money():

    category = request.form["category"]
    amount = float(request.form["amount"])

    connection = get_db_connection()

    flexible = connection.execute(
        """
        SELECT * FROM portfolios
        WHERE name = 'Flexible'
        """
    ).fetchone()

    target = connection.execute(
        """
        SELECT * FROM portfolios
        WHERE name = ?
        """,
        (category,)
    ).fetchone()

    if (
        flexible
        and target
        and amount > 0
        and amount <= flexible["balance"]
    ):

        connection.execute(
            """
            UPDATE portfolios
            SET balance = balance - ?
            WHERE name = 'Flexible'
            """,
            (amount,)
        )

        connection.execute(
            """
            UPDATE portfolios
            SET balance = balance + ?
            WHERE name = ?
            """,
            (amount, category)
        )

        connection.commit()

    connection.close()

    return redirect(url_for("home"))

@app.route("/ai-category", methods=["POST"])
def ai_category():

    description = request.form["ai_description"].strip()

    connection = get_db_connection()

    portfolios = connection.execute(
        "SELECT name FROM portfolios"
    ).fetchall()

    connection.close()

    categories = [
        portfolio["name"]
        for portfolio in portfolios
    ]

    try:
        suggestion = suggest_category(
            description,
            categories
        )

    except Exception as error:
        print("AI ERROR:", error)
        suggestion = "AI service unavailable"

    connection = get_db_connection()

    portfolios = connection.execute(
        "SELECT * FROM portfolios"
    ).fetchall()

    transactions = connection.execute(
        """
        SELECT * FROM transactions
        ORDER BY created_at DESC, id DESC
        """
    ).fetchall()

    connection.close()

    total_balance = sum(
        portfolio["balance"]
        for portfolio in portfolios
    )

    flexible_balance = next(
        (
            portfolio["balance"]
            for portfolio in portfolios
            if portfolio["name"] == "Flexible"
        ),
        0
    )

    committed_balance = total_balance - flexible_balance

    return render_template(
        "index.html",
        portfolios=portfolios,
        transactions=transactions,
        total_balance=total_balance,
        committed_balance=committed_balance,
        flexible_balance=flexible_balance,
        ai_suggestion=suggestion,
        ai_description=description
    )

if __name__ == "__main__":
    app.run(debug=True)
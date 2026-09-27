# Jipange

**Give every shilling a purpose.**

Jipange is a digital budgeting solution designed to help mobile-money users organize a single wallet balance into purpose-based portfolios such as rent, food, electricity, transport, savings, and school fees.

Instead of only showing users how much money they have, Jipange helps them understand **what their money is for**.

## Problem

Mobile-money wallets typically display one total balance, even when portions of that money are already intended for specific expenses.

For example, a user may have KSh 100,000 in their wallet, but some of that money may already be committed to rent, electricity, food, transport, savings, or school fees.

Without separating these commitments, it can be difficult to know how much money is genuinely available to spend.

## Solution

Jipange introduces digital budgeting portfolios that allow users to assign portions of their existing balance to specific purposes.

Moving money between portfolios does not change the overall wallet balance. Instead, it helps users organize and understand how their money has been allocated.

## Key Features

- View total, committed, and flexible balances
- Create custom budget portfolios
- Allocate money from Flexible funds to specific portfolios
- Maintain the same total balance when reallocating funds
- Record expenses against individual portfolios
- Automatically update portfolio balances after spending
- Prevent spending beyond a portfolio's available balance
- View recent transaction history
- AI transaction categorization interface

## AI Integration

Jipange includes an AI-assisted transaction categorization interface designed to use the Google Gemini API.

The intended workflow allows a user to describe a transaction in natural language, after which AI suggests the most appropriate existing budget portfolio.

During final hackathon testing, the external AI integration was unavailable, so manual transaction categorization remains the working fallback.

AI is designed only to provide recommendations. Financial calculations, allocations, and balance changes are handled deterministically by the application and remain under user control.

## Technology Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- Google Gemini API integration
- VS Code

## Running the Project

Install the required packages:

```bash
pip install -r requirements.txt
run the flask application
python app.py

Then open the local address displayed by Flask in your browser.
Prototype Limitations
- Mobile-money transactions are simulated
- The prototype is not connected to a live mobile-money provider
- Gemini AI integration was attempted but was unavailable during final testing
- Manual portfolio selection provides the fallback for transaction categorization
Hackathon Development
Jipange was developed during the hackathon as a functional prototype.
The Flask application, SQLite database structure, budgeting logic, portfolio allocation system, transaction handling, overspending controls, user interface, and AI integration layer were developed for the project.
Standard open-source technologies and libraries such as Flask and SQLite were used as the underlying development tools.
Future Development
Future versions of Jipange could include:
- Full AI-assisted transaction categorization
- AI-generated budgeting recommendations
- Mobile-money API integration
- Automatic transaction synchronization
- Budget alerts and spending insights
- Improved authentication and security
- Mobile application support
##Vision
**Mobile money tells you how much money you have. Jipange tells you what that money is for.**

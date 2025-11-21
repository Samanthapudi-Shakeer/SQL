# Example Natural Language Queries

This document provides example questions you can ask AskQL with different types of databases.

## E-commerce Database Examples

### Product Queries
```
- "Show me all products"
- "List products under $50"
- "Find products with low stock (less than 10 units)"
- "What are the most expensive products?"
- "Show products added in the last week"
```

### Customer Queries
```
- "How many customers do we have?"
- "List all customers from New York"
- "Find customers who signed up this month"
- "Show customers with more than 5 orders"
- "Who are our top 10 customers by total spending?"
```

### Order Queries
```
- "Show recent orders"
- "What were yesterday's orders?"
- "Find orders over $1000"
- "List pending orders"
- "Show canceled orders from last month"
```

### Analytics Queries
```
- "What's the total revenue this month?"
- "Show sales by category"
- "What's the average order value?"
- "Count orders by status"
- "Show daily sales for the last 7 days"
```

### Complex Join Queries
```
- "Show customer names with their total order amounts"
- "List products with their category names and stock levels"
- "Find orders with customer details and shipping addresses"
- "Show products that have never been ordered"
- "Display users who haven't ordered in 3 months"
```

## Employee/HR Database Examples

### Employee Queries
```
- "List all employees"
- "Show employees in the Engineering department"
- "Find employees hired in 2023"
- "Who are the highest paid employees?"
- "List managers and their direct reports"
```

### Department Queries
```
- "How many employees are in each department?"
- "What's the average salary by department?"
- "Show departments with more than 10 employees"
- "List empty departments"
```

### Payroll Queries
```
- "What's the total payroll cost?"
- "Show salary distribution by job title"
- "Find employees due for performance review"
- "List employees with salary above company average"
```

## Sales CRM Database Examples

### Lead Queries
```
- "Show all open leads"
- "Find leads from last week"
- "List leads assigned to John Doe"
- "Show high-value leads (>$50k potential)"
- "Count leads by source"
```

### Deal Queries
```
- "What deals are closing this month?"
- "Show won deals from last quarter"
- "List deals in negotiation stage"
- "What's the total pipeline value?"
- "Find stalled deals (no activity in 30 days)"
```

### Activity Queries
```
- "Show calls made today"
- "List meetings scheduled this week"
- "Find overdue tasks"
- "Show email activity by sales rep"
```

## Blog/Content Database Examples

### Post Queries
```
- "List all published posts"
- "Show draft posts"
- "Find posts by author John Smith"
- "What are the most viewed posts?"
- "Show posts from last month"
```

### Comment Queries
```
- "How many comments does each post have?"
- "Show recent comments"
- "Find posts with no comments"
- "List unapproved comments"
```

### Analytics Queries
```
- "What's the average word count per post?"
- "Show posting frequency by month"
- "List most active authors"
- "Find posts with highest engagement"
```

## Financial Database Examples

### Transaction Queries
```
- "Show all transactions from today"
- "Find transactions over $10,000"
- "List failed transactions"
- "What's the total transaction volume this month?"
- "Show transactions by payment method"
```

### Account Queries
```
- "List accounts with negative balance"
- "Show account balances above $1M"
- "Find dormant accounts (no activity in 6 months)"
- "What's the total deposits vs withdrawals?"
```

### Budget Queries
```
- "Show spending by category this month"
- "Compare budget vs actual spending"
- "List categories over budget"
- "What's our burn rate?"
```

## Inventory Database Examples

### Stock Queries
```
- "Show items low on stock"
- "List out-of-stock products"
- "Find items that need reordering"
- "What's the total inventory value?"
- "Show stock movement for last week"
```

### Warehouse Queries
```
- "How much stock is in each warehouse?"
- "Find items in warehouse A"
- "List warehouses at capacity"
- "Show stock distribution by location"
```

## Tips for Better Queries

### Be Specific
- ❌ "Show data"
- ✅ "Show customer data from California"

### Use Clear Filters
- ❌ "Find old orders"
- ✅ "Find orders from last year"

### Specify What You Want to See
- ❌ "Information about users"
- ✅ "Show user names, email addresses, and signup dates"

### Ask for Aggregations Clearly
- ❌ "How many?"
- ✅ "How many orders were placed in January?"

### Be Explicit About Sorting
- ❌ "Show products"
- ✅ "Show products sorted by price, highest first"

### Mention Time Ranges
- ✅ "Last 7 days"
- ✅ "This month"
- ✅ "Between January 1 and March 31"
- ✅ "In 2023"

### Ask for Relationships
- ✅ "Show customers with their orders"
- ✅ "List products with their categories"
- ✅ "Display users and their most recent activity"

## Handling Ambiguity

If AskQL asks for clarification, provide more context:

**Example 1:**
- Question: "Show the total"
- AskQL: "Total of what? Revenue, orders, customers, or something else?"
- Better: "Show the total revenue this month"

**Example 2:**
- Question: "List items"
- AskQL: "Which table? We have products, orders, and inventory_items"
- Better: "List all products"

**Example 3:**
- Question: "Show data from yesterday"
- AskQL: "Which data? Orders, transactions, signups?"
- Better: "Show orders from yesterday"

## Advanced Query Examples

### Window Functions (if supported)
```
- "Show running total of sales by date"
- "Rank customers by total spending"
- "Show each product's sales as a percentage of total sales"
```

### Multiple Aggregations
```
- "For each category, show count of products, average price, and total stock"
- "Show daily, weekly, and monthly revenue"
```

### Conditional Logic
```
- "Categorize customers as 'high value' if they spent over $1000, otherwise 'regular'"
- "Show products marked as 'low stock' when quantity is under 10"
```

### Date Calculations
```
- "Show orders from exactly 30 days ago"
- "Find customers whose subscription expires in the next week"
- "Calculate customer age from birth date"
```

## Troubleshooting Query Issues

### Empty Results
If you get no results, try:
- Broadening your filters
- Checking spelling of table/column references
- Removing date restrictions
- Asking "Show me a sample of data from [table]" first

### Too Many Results
If you get too many results:
- Add more specific filters
- Request only top N results
- Add date range restrictions
- Sort by relevance

### Clarification Loops
If AskQL keeps asking for clarification:
- Use exact table names from schema
- Be more specific about what you want
- Break complex questions into simpler ones
- Reference specific columns

---

**Remember**: AskQL learns from context. If your first query doesn't work perfectly, refine it based on the results or clarification questions!

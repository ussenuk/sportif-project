# sportif-project

A Unstructured Supplementary Service Data or USSD based sport news delivery system to facilitate access to diverse sport materials without internet accessibility.

### Prerequisites
Install pipenv to manage python environment

### Setup
Clone the repo and run ```pipenv install``` inside the repo directory or run the following ```python main.py```

### Database Structure

## Tables:
- subscriptions: Stores subscription information (id, name, price)
- members: Stores member information (id, first_name, last_name, gender, email, city, country, username, password, balance)
- subscription_members: Many-to-many association table linking subscriptions and members
- news: Stores news articles (id, title, content, category, subscription_id, member_id)
## Relationships:
- A subscription can have many members (through subscription_members).
- A member can have many subscriptions (through subscription_members).
- news article for a category belongs to one subscription.


### Fonctionality
### Members
- Registration
- Subscription to a News (Football, Basketball, Others)
- Ability to top_up credit
- Ability to subscribe to multiple plan as a member

### News
- List the News based on categories
- Unsubscribe to news categories
- Charges after accessing the news

### Subscription
- Charges on subscription
- Removing subscription
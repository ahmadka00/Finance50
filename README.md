
# Wishlist website
#### Video Demo:  <https://youtu.be/s3cjCOAIdNg>
#### Description:
This is a Flask-based web application for managing wishlists. Users can register, log in, and add, view and delete items on their personal wishlist. The application uses the CS50 Library to interact with an SQLite database.

The application implements a login_required decorator, which requires users to log in before accessing certain routes. This feature ensures that only registered and authenticated users can access their personal wishlist, preventing unauthorized access to private information.

The application also includes a registration page that validates user inputs, such as ensuring that the username is unique and that the email address is valid. If a user inputs invalid data, the application will provide appropriate error messages, informing the user of the reason why their registration was unsuccessful. Upon successful registration, the user is redirected to the home page and notified that their registration was completed.

The application includes a history feature that stores the date and time that each wishlist item was added. This feature provides users with a convenient way to track the history of their wishlists and can help users remember the context or reason for adding an item to their wishlist.

Overall, this Flask-based web application is a simple and user-friendly tool for managing personal wishlists. The application implements key features such as authentication, input validation, and history tracking, ensuring that users have a secure and streamlined experience when using the application.
## Requirements
Python 3
Flask
Flask-Session
Werkzeug
cs50
validate_email
functools

## Usage
Register for an account
Log in to your account
Add a new wish by clicking the "Add a Wish" button
View your wishes on the homepage
Delete a wish by clicking the "Delete" button next to the wish
## Files
application.py: Contains the Flask application
templates/: Contains the HTML templates for the web application
static/: Contains the CSS stylesheet for the web application
wishlist.db: SQLite database containing user and wish information
## API Reference
The application provides the following routes:

* '/:' Displays the user's wishes
* '/register': Allows users to register for an account
* '/login': Allows users to log in to their account
* '/logout': Allows users to log out of their account
* '/add': Allows users to add a new wish
* '/delete': Allows users to delete a wish

## Credits

This application was created as part of the CS50x course offered by Harvard University.

The cs50 module used in the application is provided by Harvard University. The validate_email module used in the application is provided by Vlad Temian.
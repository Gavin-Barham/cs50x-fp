# (CS50x Final Project) Freaky Fast Delivery a.k.a FFD

FFD is a Python web application built with the FLASK framework for assigning deliveries to their respective Jimmy John's delivery drivers. FFD is built to quickly and conveniently keep drivers moving in and out without spending minutes in front of the P.O.S determining who should take which deliveries based on proximity to each other and FIFO(first in first out) priority for both drivers and orders. 

## URL

Click the link [Freaky Fast Delivery](www.freakyfast.tech) to load FFD in your browser window.

```
www.freakyfast.tech
```

## Targeted Users
 Jimmy Johns Delivery Drivers

## Use Case
The stores GM is typically the one to assign drivers their deliveries, however often times during a lunch rush they are unable to step away from their current task to assign drivers. Not only can it be inconvenient but often times will take up much more time than should be necessary, especially during busier lunches, and that's where this application comes in.

## Usage
# Login
Upon clicking the URL users will be prompted to make an account (register/login/logout)

# Stores
After initial login users will be directed to page to select from available store #'s to be added to the users list of stores they are employed.

Users will also have the option to select an admin checkbox which will give the user admin privileges' for the selected store upon entering the correct admin passcode.

Users with admin privileges will have the ability to add/remove drivers from the given stores driver table in case of a new driver being hired, or a current driver being fired, let go, or quitting. This is in order to keep the drivers list tidy with no unnecessary extra names and allows flexibility as employees come and go.

# Select your store
Upon submitting the admin/select_store page the user is then redirected to another page where they select from their previously selected stores to choose thier current store they're working from.

Once a current store has been established for the user they may then interact with the homepage to assign orders to drivers.

# Index/Homepage
The main use of the application is once a user is logged in and selected thier store they will see two separate tables on the home page for keeping track of drivers and address/order #'s respectively.

Users can add the names of drivers waiting for an assignment from a select drop down to append the drivers table, with priority centered around FIFO(first in first out).

Users can also enter address and order #'s for the second table with all orders waiting to be assign. The input for the address is using Google Autocomplete API to filter out misspellings or user error for distance calculation. 

Upon filling the two tables with desired data to be assigned and clicking the assign button the application will make an API call to the Google Distance Matrix API. 

The origin is set as the first address on the table with all subsequent orders passing in as destinations. 

Upon receiving the data from the API it then filters out any results over a particular time threshold and just returns the address/orders that are close proximity and should be taken by the same driver. 

Thereafter the first driver name is assigned to the first returned group of results. The application continues this order grouping process and assignment, writing each to a db for an active history, until there are either no more orders or no more drivers to be assigned. 

It will then redirect to a new html page with all recently assigned deliveries with name, address, order #, and time it was assigned. 

# History
Users can also view the entire assignment history for a given store # from the /history page

## Contributing
Now that the final project is being submit pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

[Project: Delivery app/cs50x final project (Repository):](https://github.com/LucidLegend/cs50x-fp)

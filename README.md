Project: Delivery app/ cs50x final project
URL: www.freakyfast.tech
Targeted Users: Jimmy Johns Delivery Drivers

This project was created to help delivery drivers get delivery orders assigned to them based on time and address proximity. The stores GM is typically the one to assign drivers their deliveries, however often times during a lunch rush they are unable to step away from their current task to assign drivers and thats where this application comes in.
Upon clicking the URL users will b prompted to make an account (register/login/logout)
After initial login users will b directed to page to select from available store #'s to be added to the users list of stores they are employed.
The user is then redirected to another page where they select from their previously selected stores to select thier current store theyre working from.
Once a current store has been established for the user they may then interact with the homepage to assign drivers to orders.
The main use of the application is once a user is logged in and selected thier store they will see two seperate tables on the home page for kepping track of drivers and address/order #'s respectively.
Users can add the names of drivers waiting for an assignment from a select drop down to append the drivers table, with priority centered around FIFO(first in first out).
Users can also enter address and order #'s for the second table with all orders waiting to be assign. The input for the address is using Google Autocomplete API to filter out mispellings or user error for distance calculation.
Upon filling the two tables with desired data to be assigned and clicking the assign button the application will make an API call to the Google Distance Matrix API.
The origin is set as the first address on the table with all subsequent orders passing in as destinations.
Upon receiving the data from the API it then filters out any results over a particular time threshold and just returns the address/orders that are close proximity and should be taken by the same driver.
Thereafter the first driver name is assigned to the first returned group of results.
The application comtinues this order grouping process and assignment, writing each to a db for an active history, until there are either no more orders or no more drivers to be assigned.
It will then redirect to a new html page with all recently assigned deliveries with name, address, order #, time it was assigned.
Users can also view the entire assignment history for a given store #.

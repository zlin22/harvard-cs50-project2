# Project 2

Web Programming with Python and JavaScript

## Function of application.py
This is the main Flask application file, containing all the routing and server side code. It uses the socketIO connection for the live updating of messages without refreshing the page

## Function of templates/layout.html
This is the base HTML layout page that other pages extends.

## Function of templates/heythere.html
This is generic page to display error and success messages

## Function of templates/index.html
This is the main page and it displays the main page of the app. If the user is not logged in, it displays a place for the user to register a username. If the user is logged in, then the page will redirect the user to the most recent channel page.

## Function of templates/channels.html
This is a list of all the available channels, and it allows the user to add a new channel.

## Function of templates/channel_details.html
This shows all the messages that were sent to the channel. It allows the user to send a new message, as well as delete any of the messages that the user has previously sent.

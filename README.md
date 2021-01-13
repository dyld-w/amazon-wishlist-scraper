# Amazon Wishlist Scraper

![alt text](https://github.com/dyld-w/amazon-wishlist-scraper/blob/main/wishScraper%20Screenshot.png)

This is a program to get the sum cost of all of the items in an Amazon wishlist that have a price associated with them. Implemented with a GUI written in tkinter, it asks for user input for the name of the wishlist and if it is a new wishlist it asks for the URL to the wishlist. It checks that it is a valid URL then stores the number of items in the list, total cost, name, and URL to a file called lists.txt. If lists.txt didn't exist before this, it is created. In subsequent invocations, user can just input the name
of the saved wishlist and the ouput will say the total number of items in the list before the current invocation and the sum cost of those items; the updated number of items in the list (at the time of invocation) and the sum cost of those items; and the difference in number of items and cost between the most recent invocation and the prior invocation. An example output is shown above.

If anyone wants to use this this, you'll probably have to update the path variable to the correct path to lists.txt on your machine.

This was my first foray into webscraping, first true personal project, and first project in python after a year away from the language. There are bound to be things that could be better and I know the variable names don't follow convention but I had fun making it. :)

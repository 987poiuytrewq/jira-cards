jira-cards
==========

Generate printable cards from JIRA

If you use Atlassian JIRA to track issues in your project, you may also want to use a physical board to move cards around on.

This project allows you to generate a printable view of your issues. The format layout and style of the output can be controlled with css and html.

Included templates are for printing onto square or oblong post-it notes. You can print a blank template onto a piece of paper, then stick post-it notes to it, then print out your issues directly onto the post-it notes.



Dependencies
============

This project requires python 2.x to run, and also the python module python-jira, install through pip:

    sudo apt-get install python-pip
    sudo pip install jira

Usage
=====

run the script with the ```-h``` flag to see the help message

    ./jira-cards.py -h

to see the help for each mode, run

    ./jira-cards.py MODE -h
    
when runnin in ```board``` mode you can either specify a board name using the ```-b``` option or don't specify one and you will be given a list of available boards, type the name displayed to select it

Customising
===========

The script uses html and css to render the cards. 

You can customise the content of each card by creating a new format. Use string replacement tags ```{field_name}``` to insert the fields from jira (to see a list of available fields, use the ```-d``` debug flag.

You can also customise the styling of each card by creating a new css style sheet.

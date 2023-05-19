Step 1

Menu
---------------------
Sandwiches: 
Samuel's Spicy Italian- Ingredients: Salami, Pepperoni, Cheddar Cheese, Red Peppers, Onions, Default Bread: White, Default Spread: Chipotle 
Club Tuna- Ingredients: Tuna Salad, American Cheese, Cucumber, Default Bread: Whole Wheat, Default Spread: Mayo 
Beach House- Ingredients: Turkey, Provolone Cheese, Avocado, Cucumber, Default Bread: Rye, Default Spread: Dijon Mustard 
Cuban- Ingredients: Bacon, Ham, Swiss Cheese, Pickles, Default Bread: Whole Wheat, Default Spread: Dijon Mustard 

Bread Options: Whole Wheat, White, Rye, 
Spread Options: Mayo, Dijon Mustard, Chipotle, 
Options: Toasted, Salted, Extra Cheese, 
Exceptions: Onions, Cucumber, Avocado, Ham,

**Note about Options/Exceptions: The user is not required to enter any options/exceptions when ordering. If they do not order any options, then the options
portion of their printed out order will remain empty (same with exceptions). If they order options that are not part of the list of options, the program will
ignore them and simply not add them to the options portion of their order (this same principle applies to the customer ordering exceptions that are not 
part of the list of exceptions or not an ingredient in the sandwich they are ordering). 

Step 2:
List of terms treated as equivalent:
[samuel's, spicy, italian, samuel's spicy, samuel's italian, spicy italian, samuel's spicy italian]
[club tuna, club, tuna]
[beach house, house, beach]
[whole wheat, wheat, whole]
[mayo, mayonnaise]
[dijon, dijon mustard, mustard]
[toasted, toasty, toast]
[salted, salty, salt]
["yes", "yep", "yup", "yeah", "y"]
["nope", "no", "nah", "n"]
[options, menu, choices]

List of terms that are ignored:
['please', 'thanks', 'thank', 'you', 'with', 'the', 'i', 'want', 'the', 'sandwich']

These words will signal an exception: hold, minus, no, without

Step 3:
I used Python for this assignment. To run this program, just go to line 223 of the file(if __name__ == '__main__':) and press the green button. 
The only file I used for this assignment was sandwich.py. This file contains a menu class which contains all the sandwiches possible, as well as 
the breads, spreads, options and exceptions. It also has the create_menu function to print out the menu when the customer requests. There is also
a class called CustomerInteraction that has the greet_customer function as well as functions for parsing the order the user inputted so the details
can be printed out accurately to the screen. It also has a function called handle_exception that handles situations where the user either forgot to
input a necessary piece of information for making a sandwich(name, bread, spread) or entered something invalid. Lastly, the main method puts everything
together, asking the user for their order and calling upon functions from other classes to output to screen all the correct information.

Step 4:
Example 1: The user asked for a sandwich but did not specify what spread he wanted so the program had to ask him to clarify. 
Welcome to Sam's Sandwich Shop!
What do you want to eat?
I want the tuna on toasted rye minus the cucumber

Your order is missing something required to make a sandwich or have chosen an invalid item! Here are a list of valid choices you must choose
from to finish your order: 
['Mayo', 'Dijon Mustard', 'Chipotle']

Press enter to choose the default spread option for this sandwich or type in your choice from the above choices?
mayo

Your Final Order Details:
Name: Club Tuna
Usual Ingredients: ['Tuna Salad', 'American Cheese', 'Cucumber']
Bread: Rye
Spreads: ['Mayo']
Options: ['Toasted']
Exceptions: ['cucumber']

Is the above final order correct?
yup

Thank you for your order. We'll get to making it right away!

Example 2: The user asked for a sandwich but did not specify what bread they wanted so the program asked him to clarify. 
Welcome to Sam's Sandwich Shop!
What do you want to eat?
I want the beach sandwich with dijon and mayonnaise with extra cheese hold the avocado and cucumber

Your order is missing something required to make a sandwich or have chosen an invalid item! Here are a list of valid choices you must choose
from to finish your order: 
['Whole Wheat', 'White', 'Rye']

Press enter to choose the default bread option for this sandwich or type in your choice from the above choices?


Your Final Order Details:
Name: Beach House
Usual Ingredients: ['Turkey', 'Provolone Cheese', 'Avocado', 'Cucumber']
Bread: Rye
Spreads: ['Mayo', 'Dijon Mustard']
Options: ['Extra Cheese']
Exceptions: ['avocado', 'cucumber']

Is the above final order correct?
Yes

Thank you for your order. We'll get to making it right away!

Example 3: The user asks for a sandwich but does not specify any options or exceptions. Since options and exceptions are not required to be specified,
they just remain as empty lists on the order form. 
Welcome to Sam's Sandwich Shop!
What do you want to eat?
i want the italian on wheat with chipotle

Your Final Order Details:
Name: Samuel's Spicy Italian
Usual Ingredients: ['Salami', 'Pepperoni', 'Cheddar Cheese', 'Red Peppers', 'Onions']
Bread: Whole Wheat
Spreads: ['Chipotle']
Options: []
Exceptions: []

Is the above final order correct?
yup

Thank you for your order. We'll get to making it right away!

Example 4: Fails to create order for the customer. In this example, the system fails because the user keeps entering a spread that is not valid. As 
a result, it just enters an infinite loop where the program keeps repeatedly asking the user to enter a valid spread and it will not make a sandwich
until the user does. Below is an example interaction in this scenario. It never stops asking the user to enter a valid sauce until the user actually does. 
Welcome to Sam's Sandwich Shop!
What do you want to eat?
i want the cuban on rye with ketchup

Your order is missing something required to make a sandwich or have chosen an invalid item! Here are a list of valid choices you must choose
from to finish your order: 
['Mayo', 'Dijon Mustard', 'Chipotle']

Press enter to choose the default spread option for this sandwich or type in your choice from the above choices?
bbq sauce

Your order is missing something required to make a sandwich or have chosen an invalid item! Here are a list of valid choices you must choose
from to finish your order: 
['Mayo', 'Dijon Mustard', 'Chipotle']

Press enter to choose the default spread option for this sandwich or type in your choice from the above choices?
ranch

Your order is missing something required to make a sandwich or have chosen an invalid item! Here are a list of valid choices you must choose
from to finish your order: 
['Mayo', 'Dijon Mustard', 'Chipotle']

Press enter to choose the default spread option for this sandwich or type in your choice from the above choices?
tartar

Your order is missing something required to make a sandwich or have chosen an invalid item! Here are a list of valid choices you must choose
from to finish your order: 
['Mayo', 'Dijon Mustard', 'Chipotle']

Press enter to choose the default spread option for this sandwich or type in your choice from the above choices?
red pepper sauce

Your order is missing something required to make a sandwich or have chosen an invalid item! Here are a list of valid choices you must choose
from to finish your order: 
['Mayo', 'Dijon Mustard', 'Chipotle']

Press enter to choose the default spread option for this sandwich or type in your choice from the above choices?
pesto

Your order is missing something required to make a sandwich or have chosen an invalid item! Here are a list of valid choices you must choose
from to finish your order: 
['Mayo', 'Dijon Mustard', 'Chipotle']

Press enter to choose the default spread option for this sandwich or type in your choice from the above choices?

Step 5:
1. The easiest part of this assignment was setting up the menu and getting it to print out.
2. The hardest part of this assignment was figuring out the logic for the parsing user input function and its helpers. 
3. From doing this assignment, I got a basic understanding of how natural language processing systems work and how they can be applied to other areas.     
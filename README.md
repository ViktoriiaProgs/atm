# atm
ATM Project Python
Create a program,
that will simulate the operation of the ATM/terminal system.
When creating an object, the amount of the user's balance and the access pin are passed as attributes.

The pin code verification is called automatically when the object is created and takes three attempts.
If the login is successful, the balance is automatically written to a separate text file +
the balance of the system itself is stored in another file.

The following actions are available to the user:

1. Withdraw funds.
  In this case, the amount cannot exceed the available balance of the user and the system itself.
  When withdrawing, the amount is automatically deducted from the user's and the system's balance.

2. Deposit funds.
   In this case, the user's and the system's balance will be replenished by the corresponding amount.

3) Find out the current exchange rate.
      Here, we use a request, and the rate itself is obtained from an arbitrary website.

4) Transfer a certain amount to an arbitrary currency.
  Here, we also use a request for the current exchange rate.
  After the operation, another attribute will be created for the user
  (amount of funds in the specified currency),
  the value of which will be stored in a new text file.

5. Each operation is recorded in a separate file in the form of a dictionary,
where the key is time + date (datetime.now()),
the value is the type of operation performed.

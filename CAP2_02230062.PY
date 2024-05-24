##########
# Name: Dorji Tshering
#Department: Electrical
#Std ID: 02230062
##########
#References
#https://www.freecodecamp.org/news/how-to-build-an-online-banking-system-python-oop-tutorial/
#https://www.geeksforgeeks.org/python-program-to-create-bankaccount-class-with-deposit-withdraw-function/
##########


import random # will generate random and distinct account number and password while creating bank acount
import os # connects with operating system and check for existance of files "accounts.txt"

ACCOUNTS_FILE = "accounts.txt" # It is a contant that holds filename which contains account information 


class Account: # account class definition
    def __init__(self, account_number, password, account_type, balance=0.0): #initializes the account with the given parameters such as account number password, account type, and an optional initial balance        self.account_number = account_number
        self.password = password
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount): # defines a function called deposit to add money to the account
        self.balance += amount
        return self.balance  # returns the final balance

    def withdraw(self, amount): # defines a function to withdraw money from the account
        if amount > self.balance:
            raise ValueError("Insufficient funds.") # raise error if there is not enough money
        self.balance -= amount
        return self.balance # returns the balance amount afte withdrawel


class PersonalAccount(Account): #calls the base class for the subclass"Personal account"
    def __init__(self, account_number, password, balance=0.0):
        super().__init__(account_number, password, "Personal", balance) # calls the base class constructor

class BusinessAccount(Account): #calls the base class for the subclass "Business account"
    def __init__(self, account_number, password, balance=0.0):
        super().__init__(account_number, password, "Business", balance) # calls base class constructor

# Bank class definition
class Bank:
    def __init__(self): #  initializes a "Bank" object.
        self.accounts = self.load_accounts() # It calls load_accounts to load existing accounts from a file into the self.accounts dictionary.

    def load_accounts(self):
        accounts = {}
        if os.path.exists(ACCOUNTS_FILE): # checks the file existence
            with open(ACCOUNTS_FILE, 'r') as file: # Reads account data from ACCOUNTS_FILE.
                for line in file:
                    account_number, password, account_type, balance = line.strip().split(',') 
                    balance = float(balance) # used float to accept decimal points
                    # calls function "account_type" to create personal or business account
                    if account_type == "Personal":
                        accounts[account_number] = PersonalAccount(account_number, password, balance)
                    elif account_type == "Business":
                        accounts[account_number] = BusinessAccount(account_number, password, balance)
        return accounts

    def save_accounts(self):
        with open(ACCOUNTS_FILE, 'w') as file: # Save the current state of accounts to the accounts file
            for account in self.accounts.values(): # Each account's data is written as a line in the file.
                file.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")

    def create_account(self, account_type): # Create account number wiht password
        account_number = str(random.randint(1000000000, 9999999999)) # Using random, generates a random account number of digit 10
        password = str(random.randint(1000, 9999)) # gives random account password of 4 digit
        # create a new account based on specified account type
        if account_type == "Personal":
            account = PersonalAccount(account_number, password)
        elif account_type == "Business":
            account = BusinessAccount(account_number, password)
        else:
            raise ValueError("Invalid account type.") # give "Invalid account type" if account chosen is neither of them
        self.accounts[account_number] = account # save new account to the file
        self.save_accounts()
        return account_number, password # gives the account with its password

    def login(self, account_number, password): # login by using given account number and password
        account = self.accounts.get(account_number)
        if account and account.password == password: # checks if the account exits and password typed is matched it gives the account objects
            return account
        return None # if not gives none 


    def delete_account(self, account_number): # delete the account that been created 
        if account_number in self.accounts: 
            del self.accounts[account_number] # remove the deleted account from the dictionary
            self.save_accounts() #save the updated account to the file
            return True # True if account is deleted
        return False #False if account does not exist

    def transfer(self, from_account, to_account_number, amount): #checks if recevier account exit or not 
        if to_account_number not in self.accounts:
            raise ValueError("Receiving account does not exist.") # if does not exit returns the given string
        from_account.withdraw(amount) #specify the amount to be transfered
        self.accounts[to_account_number].deposit(amount) # deposit the funds to targeted account
        self.save_accounts() #save the updated account to file

# Main function to run the application
def main():
    bank = Bank() # Initialize a new Bank object
    while True:
        print("\n--- Bank Application ---")
        print("1. Open Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ") # getting user's choice from above three options
        if choice == '1': # implementing the code for opening of new account
            account_type = input("Enter account type (Personal/Business): ") #
            account_number, password = bank.create_account(account_type)
            print(f"Account created. Account Number: {account_number}, Password: {password}")
        elif choice == '2': # login to an account that had been already created using given given account number and password
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            account = bank.login(account_number, password)
            if account: # if account number and password matches with existing account gives "login successful"
                print("Login successful.")
                while True: #gives following choice for the user
                    print("\n--- Account Menu ---")
                    print("1. Check Balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Transfer")
                    print("5. Delete Account")
                    print("6. Logout")
                    choice = input("Enter choice: ") #asking for user choice
                    if choice == '1':
                        print(f"Balance: {account.balance}") #checking account balance
                    elif choice == '2':
                        amount = float(input("Enter amount to deposit: ")) # depositing fund to the account
                        account.deposit(amount)
                        bank.save_accounts()#save the updated account to account file
                        print(f"Deposited {amount}. New Balance: {account.balance}")# gives the new balance after depositing fund
                    elif choice == '3':
                        amount = float(input("Enter amount to withdraw: "))#withdraw fund from existing account
                        try:
                            account.withdraw(amount)# amount to be withdraw
                            bank.save_accounts()
                            print(f"Withdrawn {amount}. New Balance: {account.balance}")# gives remaining balance after withdrawing
                        except ValueError as e: # value error if fund is insufficient
                            print(e)
                    elif choice == '4':# transfering fund to other account
                        to_account_number = input("Enter destination account number: ")#asks for targeted account number
                        amount = float(input("Enter amount to transfer: "))#amount to be transfer
                        try:
                            bank.transfer(account, to_account_number, amount)
                            print(f"Transferred {amount} to {to_account_number}. New Balance: {account.balance}")
                        except ValueError as e:# handle errors if the account number doesn't exist
                            print(e) 
                    elif choice == '5':# Delete the logged-in account
                        confirm = input("Are you sure you want to delete your account? (yes/no): ")
                        if confirm.lower() == 'yes':# asking for confirmation on choice made
                            if bank.delete_account(account_number):
                                print("Account deleted successfully.")
                                break #exit account menu after deleting the account
                            else:
                                print("Error deleting account.")
                    elif choice == '6':
                        print("Logged out.")
                        break
                    else:
                        print("Invalid choice. Try again.")
            else:
                print("Invalid account number or password.") #if the account number or password doesn't match
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")# handle the invalid choice made by user

if __name__ == "__main__": #checks the script is being run directly
    main() #  calls the main() function to start the application.
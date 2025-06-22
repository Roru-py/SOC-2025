"""
This is where the actual working of the program will happen!
We'll be Querying stuff for testing whether your classes were defined correctly

Whenever something inappropriate happens (like a function returning false in people.py),
raise a Value Error.
"""
from people import * # import everything!

if __name__ == "__main__":  # Equivalent to int main() {} in C++.
    last_input = 99
    while last_input != 0:
        last_input = int(input("Please enter a query number:"))

        if last_input == 1:
            name = input("Name:")
            age = input("Age: ") #age should also be an input right ???
            ID = int(input("ID:"))
            city = input("City:")
            branchcodes = input("Branch(es):")
            # How will you conver this to a list, given that
            # the user will always enter a comma separated list of branch codes?
            # eg>   2,5
            branchcodes = list(map(int,branchcodes.split(",")))
            position = input("Position: ")
            salary = input("Salary: ")
            # Create a new Engineer with given details.
            engineer = Engineer(name,age,ID,city,branchcodes,position=position,salary = salary) # Change this

            engineer_roster.append(engineer) # Add him to the list! See people.py for definiton
            
        
        elif last_input == 2:
            # Gather input to create a Salesperson
            # Then add them to the roster
            name = input("Name:")
            age = input("Age: ")
            ID = int(input("ID:"))
            city = input("City:")
            branchcodes = input("Branch(es):")
            branchcodes = list(map(int,branchcodes.split(",")))
            position = input("Position: ")
            salary = input("Salary: ")
            sales = Salesman(name, age, ID, city, branchcodes, position=position, salary = salary, superior = None)
            
            sales_roster.append(sales)

        elif last_input == 3:
            ID = int(input("Employee ID to print details: "))
            # Print employee details for the given employee ID that is given. 
            found_employee = None
            for employee in engineer_roster + sales_roster:
                if employee.ID == int(ID):
                    found_employee = employee
                    break
            if found_employee is None: print("No such employee")
            else:
                print(f"Name: {found_employee.name} and Age: {found_employee.age}")
                print(f"City of Work: {found_employee.city}")

                ## Write code here to list the branch names to
                ## which the employee reports as a comma separated list
                ## eg> Branches: Goregaon,Fort
                branch_names = []
                for x in found_employee.branches:
                    branch_names.append(branchmap[int(x)]["name"])
                print("Branches: " + str(branch_names))
                print("Position: "+ found_employee.position)
                print(f"Salary: {found_employee.salary}")

        elif last_input == 4:
            #### NO IF ELSE ZONE ######################################################
            # Change branch to new branch or add a new branch depending on class
            # Inheritance should automatically do this. 
            # There should be no IF-ELSE or ternary operators in this zone
            ID = int(input("Enter Employee ID to change branch: "))
            code = int(input("Enter new branch ID: "))
            found_employee = None
            for employee in engineer_roster + sales_roster:
                if employee.ID == int(ID):
                    found_employee = employee
                    break
            found_employee.migrate_branch(code)
            #if statement has to be used here to find the employee otherwise inheritance does its work

            #### NO IF ELSE ZONE ENDS #################################################

        elif last_input == 5:
            ID = int(input("Enter Employee ID to promote: "))
            # promote employee to next position
            found_employee = None
            for employee in engineer_roster + sales_roster:
                if employee.ID == int(ID):
                    found_employee = employee
                    break
            if found_employee is not None:
                if found_employee.promote(): #changed the promote function as i cant find which class ???
                    print("Employee promoted")
                else:
                    print("Employee cannot be promoted further")
            else:
                print("Employee not found")

        elif last_input == 6:
            ID = int(input("Enter Employee ID to give increment: "))
            amt = int(input("Enter amount to increment: "))
            found_employee = None
            for employee in engineer_roster + sales_roster:
                if employee.ID == int(ID):
                    found_employee = employee
                    break
            if found_employee is not None:
                found_employee.increment(amt)
            else:
                print("Employee not found")
            # Increment salary of employee.
        
        elif last_input == 7:
            ID = int(input("Enter Employee ID to find superior: "))
            found_employee = None
            for employee in sales_roster:
                if employee.ID == int(ID):
                    found_employee = employee
                    break
            if found_employee is not None:
                (ID,name) = found_employee.find_superior()
                if ID is not None:
                    print("Name: " + str(name) + " and ID: " + str(ID))
                else:
                    print("Employee doesn't have a superior")
            else:
                print("No employee with given ID")
            # Print superior of the sales employee.
        
        elif last_input == 8:
            ID_E = int(input("Enter Employee ID to add superior: "))
            ID_S = int(input("Enter Employee ID of superior: "))
            # Add superior of a sales employee
            found_employee = None
            for employee in sales_roster:
                if employee.ID == int(ID_E):
                    found_employee = employee
                    break
            if found_employee is not None:
                if found_employee.add_superior(ID_S):
                    print("Superior with ID: "+str(ID_S)+" added to employee") 
                else:
                    print("This ID cannot be added as superior for given employee")
            else:
                print("Employee not found")
            #changed add_superior function to accomodate ID of superior
        else:
            print("No such query number defined")

            
            

            


            


        







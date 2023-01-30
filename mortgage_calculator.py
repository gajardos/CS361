# Author: Sebastian Gajardo
# Date: 1/25/2023
# Course: CS 361 Software Engineering 1
# Description: Mortgage calculator app GUI

from tkinter import * 
from tkinter import ttk
from tkinter import messagebox
#import numpy as np
#import matplotlib as plt

is_hidden = True

def refresh_mortgage_payment_summary(principle, pmi):
    """Refreshes the mortgage payment summary frame based on user inputed data.

    Args:
        principle (_type_): _description_
        property_tax (_type_): _description_
        pmi (_type_): _description_
        insurance (_type_): _description_
        total (_type_): _description_
    """
    principle_number.config(text=str(principle))
    pmi_number.config(text=str(pmi))
    total_number.config(text=str(principle +  pmi))
    return

def show_hide_click():
    """ Shows and hides explanations section dropbox. Called when show/hide button clicked.
    """
    global is_hidden
    
    if is_hidden:
        input_loan_data_list.place(x=15, y=480)
        is_hidden = False
        
    else:
        input_loan_data_list.place_forget()
        is_hidden = True
    return

def clear_click():
    """0 all of the values in the mortgage payment summary frame and blanks
    the input loan data frame.
    """
    principle_number.config(text="0")
    property_tax_number.config(text="0")
    pmi_number.config(text="0")
    home_insurance_number.config(text="0")
    total_number.config(text="0")
    home_price.delete(0, END)
    down_payment_clicked.set("")
    loan_term_clicked.set("")
    credit_score.delete(0, END)
    zipcode.delete(0, END)
    return
    
def calculate_click(price: int, percent_down: int, loan_term: int, interest: int):
    """Calculates 

    Args:
        price (_type_): _description_
        percent_down (_type_): _description_
        loan_term (_type_): _description_
    """
    loan_total = price - (percent_down / 100) * price
    monthly_interest = (interest / 100)/ 12
    total_months = 12 * loan_term
    
    principel = loan_total * (monthly_interest * (1 + monthly_interest)**total_months) / ((1 + monthly_interest)**(total_months) - 1)
    pmi = 0
    
    if percent_down < 20:
        pmi = (.0058 * loan_total) / 12
    
    refresh_mortgage_payment_summary(round(principel, 2), round(pmi, 2))
    return 

def pop_up():
    """Creates a pop and clears data by calling clear_click if yes is selected. If no then returns.
    """
    response = messagebox.askquestion("Question","Are you sure you want to clear all data?")

    if response == "yes":
        clear_click()
    return

# Create window object
app = Tk()

app.title("Mortgage Calculator")
app.geometry("900x750")

# Frames
loan_data_frame = LabelFrame(app, text="Input Loan Data", width=250, height=185, padx=5, pady=5)
mortgage_payment_summary_frame = LabelFrame(app, text="Mortgage Payment Summary", width=250, height=150, padx=5, pady=5)
payment_graph_frame = LabelFrame(app, text="Payment Graph", width=600, height=185, padx=5, pady=5)
breakdown_graph_frame = LabelFrame(app, text="Breakdown Graph", width=600, height=185, padx=20, pady=20)

# Labels
instructions_label = Label(app, text="""Please enter purchase all requested information and press calculate to get mortgage payment summary and graphs.""", 
                           font=("TkDefaultFont",15))
definitions_label = Label(app, text="""Input Loan Data Explanation""", font=("TkDefaultFont",15))


home_price_label = Label(loan_data_frame, text="Home Price")
down_payment_label = Label(loan_data_frame, text="Down Payment %")
loan_term_label = Label(loan_data_frame, text="Loan Term")
credit_score_label = Label(loan_data_frame, text="Credit Score")
zipcode_label = Label(loan_data_frame, text="Zip Code")

principle_interest_lable = Label(mortgage_payment_summary_frame, text="Principle & Interest")
principle_number = Label(mortgage_payment_summary_frame, text="0")
property_tax_label = Label(mortgage_payment_summary_frame, text="Property Tax")
property_tax_number = Label(mortgage_payment_summary_frame, text="0")
pmi_lable = Label(mortgage_payment_summary_frame, text="Mortgage Insurance")
pmi_number = Label(mortgage_payment_summary_frame, text="0")
home_insurance_label = Label(mortgage_payment_summary_frame, text="Home Insurance")
home_insurance_number = Label(mortgage_payment_summary_frame, text="0")
total_label = Label(mortgage_payment_summary_frame, text="Total")
total_number = Label(mortgage_payment_summary_frame, text="0")

# Entry fields
home_price = Entry(loan_data_frame, width=10, borderwidth=0)
credit_score = Entry(loan_data_frame, width=10, borderwidth=0)
zipcode = Entry(loan_data_frame, width=10, borderwidth=0)

# Comboboxes
down_payment_clicked = StringVar()
down_payment_options = ["5", "10", "15", "20"]
down_payment_combo = ttk.Combobox(loan_data_frame, textvariable=down_payment_clicked, values=down_payment_options)

loan_term_clicked = StringVar()
term_options = ["30", "15"]
loan_term_combo = ttk.Combobox(loan_data_frame, textvariable=loan_term_clicked, values=term_options)

# Canvas

# Dropboxes

input_loan_data_list = Listbox(app, width=96, height=15)
input_loan_data_list.insert(END, "* Home Price: Purchase price of the home you're trying to buy.")
input_loan_data_list.insert(END, "* Down Payment Percentage: Percentage of purchase price that is being used as a down payment.")
input_loan_data_list.insert(END, "* Loan Term: Length of time to repay the loan.")
input_loan_data_list.insert(END, "* Credit Score: Score reported by credit bureaus used by loan companies to adjust loan interest rate based on percieved risk.")
input_loan_data_list.insert(END, "* Zip Code: Zip code of the property you are trying to purchase. This will effect the property taxes and insurance rates.")

# Buttons
calculate_button = Button(loan_data_frame, text="Calculate", 
                          command=lambda:calculate_click(int(home_price.get()), int(down_payment_clicked.get()), int(loan_term_clicked.get()), 6.5))
clear_button = Button(app, text="Clear", command=pop_up)

show_hide_button = Button(app, text="Show/Hide", command=show_hide_click)

# Widget placement on the screen
instructions_label.place(x=15, y=10)

loan_data_frame.place(x=15, y=40)
home_price_label.place(x=0, y=0)
home_price.place(x=120, y=0)
down_payment_label.place(x=0,y=25)
down_payment_combo.place(x=120,y=25, width=100, height=25)
loan_term_label.place(x=0, y=50)
loan_term_combo.place(x=120, y=50, width=100, height=25)
credit_score_label.place(x=0, y=75)
credit_score.place(x=120, y=75)
zipcode_label.place(x=0, y=100)
zipcode.place(x=120, y=100)
calculate_button.place(x=70, y=125)

mortgage_payment_summary_frame.place(x=15, y=250)
principle_interest_lable.place(x=0, y=0)
principle_number.place(x=160, y=0)
property_tax_label.place(x=0, y=25)
property_tax_number.place(x=160, y=25)
pmi_lable.place(x=0, y=50)
pmi_number.place(x=160,y=50)
home_insurance_label.place(x=0, y=75)
home_insurance_number.place(x=160, y=75)
total_label.place(x=0, y=100)
total_number.place(x=160, y=100)

payment_graph_frame.place(x=285, y=40)
breakdown_graph_frame.place(x=285, y=250)
clear_button.place(x=100, y=405)

definitions_label.place(x=15, y=450)
show_hide_button.place(x=215, y=450)

# Start program
app.mainloop()
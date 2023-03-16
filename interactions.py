# Author: Sebastian Gajardo
# Date: 2/15/2023
# Course: CS 361 Software Engineering 1
# Description: Mortgage calculator app interactions and button actions.

from tkinter import *
from tkinter import messagebox
import webbrowser
import rate_client

is_hidden = True

def open_link(Event):
    """ Opens link when event is encountered.
    """
    webbrowser.open_new("https://fred.stlouisfed.org/series/MORTGAGE30US")

def refresh_breakdown_graph(price: int, principle: int, pmi: int, ax: object, canvas: object, color: tuple):
    """ Calculates new values and refreshes pie chart on GUI.
    
        args:
        price (int): Price of the property inputed by the user.
        principle (int): Principle portion of the mortgage payment.
        pmi (int): Mortgage insurance.
        color: RGB color of app to match.
        The rest are matplot objects to be updated.
    """
    total = principle + pmi + (1400 / 12) + (price * .012 / 12)
    principle_p = round(principle / total * 100, 2)
    pt_p = round((price * .012 / 12) / total * 100, 2)
    pmi_p = round(pmi / total * 100, 2)
    hmi_p = round((1400 / 12) / total * 100, 2) if principle != 0 else 0
    
    ax.clear()
    
    sizes = [principle_p, pmi_p, hmi_p, 1.2] if principle_p != 0 else [25, 25, 25, 25]
    colors = ["orange", "green", "teal", "yellow"]
    labels = [f'Principle & Interest: % {principle_p}', f'Property Taxes: % {pt_p}', f'Mortgage Insurance: % {pmi_p}', f'Home Insurance: % {hmi_p}']
    ax.pie(sizes, colors=colors, startangle=90, radius=1.5)
    legend = ax.legend(labels, loc="center left", bbox_to_anchor=(1.2, 0.5))
    legend.get_frame().set_facecolor(color)
    legend.get_frame().set_edgecolor("none")

    for text in legend.get_texts():
        text.set_color("white")
    
    canvas.draw()
        
    return 

def show_hide_click(input_loan_data_list: object):
    """ Shows or hides the input loan data list object in the GUI based on boolean value.

    Args:
        input_loan_data_list (object): Object from the GUI.
    """
    global is_hidden
    
    if is_hidden:
        input_loan_data_list.place(x=15, y=480)
        is_hidden = False
        
    else:
        input_loan_data_list.place_forget()
        is_hidden = True
    return

def refresh_mortgage_payment_summary(price: int, principle: int, pmi: int,
                                     principle_number: object, pt_number: object, hmi_number: object, pmi_number: object, total_number: object):
    """ Refreshes the mortgage payment summary object values in the GUI.

    Args:
        price (int): Total price of property to be purchased.
        principle (int): The principel calculated by the mortgage equation.
        pmi (int): Mortgage insurance calculated based on mortgage equation.
        The rest are tkinter objects to be updated on the GUI.
    """
    property_tax = round(price * .012 / 12, 2)
    hmi = round(1400.00 / 12, 2)
    principle_number.config(text=str(principle))
    pt_number.config(text=str(property_tax))
    pmi_number.config(text=str(pmi))
    hmi_number.config(text=str(hmi))
    total_number.config(text=str(round(principle + property_tax +  pmi + hmi, 2)))
    return

def calculate_click(price: int, percent_down: int, loan_term: int, interest: int, 
                    principle_number: object, pt_number: object, pmi_number: object, hmi_number: object, total_number: object, ax: object, canvas: object, 
                    color: tuple):
    """ Calculates mortgage payment based on user passed arguments and calls refresh_mortgage_payment_summary to update GUI
    with the new values.

    Args:
        price (int): Price of property inputed by user.
        percent_down (int): Percentage of total price paid by the user intially.
        loan_term (int): How many years the loan is for.
        interest (int): Interest rate calculated
        The rest are objects to be updated with new values passed to refresh_mortgage_payment_summary(), reference it for more details.
    """
    interest = rate_client.get_rate(interest) if interest != "" else 7.0
    
    loan_total = price - (percent_down / 100) * price
    monthly_interest = (interest / 100)/ 12
    total_months = 12 * loan_term
    
    principel = loan_total * (monthly_interest * (1 + monthly_interest)**total_months) / ((1 + monthly_interest)**(total_months) - 1)
    pmi = 0
    
    if percent_down < 20:
        pmi = (.0058 * loan_total) / 12
    
    refresh_mortgage_payment_summary(price, round(principel, 2), round(pmi, 2), principle_number, pt_number, pmi_number, hmi_number, total_number)
    refresh_breakdown_graph(price, round(principel, 2), round(pmi, 2), ax, canvas, color)
    return 

def clear_click(principle_number: object, property_tax_number: object, pmi_number: object, home_insurance_number: object, 
                total_number: object, home_price: object, down_payment_clicked: object, loan_term_clicked: object, credit_score: object, 
                zipcode: object, ax: object, canvas: object, color: tuple):
    """ Clears or 0's all data members of both the loan data and mortgage payment data frames.

    Args:
        color (tuple): RGB color of app.
        Objects whose value should be cleared from the GUI.
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
    refresh_breakdown_graph(0, 0, 0, ax, canvas, color)
    
    return

def pop_up(principle_number: object, property_tax_number: object, pmi_number: object, home_insurance_number: object, 
           total_number: object, home_price: object, down_payment_clicked: object, loan_term_clicked: object, credit_score: object, 
           zipcode: object, ax: object, canvas: object, color: tuple):
    """ Pops upp a message box when the clear botton is clicked and calls clear click to clear all data 

    Args:
        All arguments to be passed to clear_click(), reference it for more details.
    """
    response = messagebox.askquestion("Question","Are you sure you want to clear all data?")

    if response == "yes":
        clear_click(principle_number, property_tax_number, pmi_number, home_insurance_number, total_number, home_price, down_payment_clicked, 
           loan_term_clicked, credit_score, zipcode, ax, canvas, color)
    return
# Author: Sebastian Gajardo
# Date: 2/15/2023
# Course: CS 361 Software Engineering 1
# Description: Mortgage calculator app GUI using tkinter. Creation and placement of widgets on the screen.

from tkinter import * 
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import interactions

# Create window object
app = Tk()

app.title("Mortgage Calculator")
app.geometry("900x750")

# Frames
loan_data_frame = LabelFrame(app, text="Input Loan Data", width=250, height=185, padx=5, pady=5)
mortgage_payment_summary_frame = LabelFrame(app, text="Mortgage Payment Summary", width=250, height=150, padx=5, pady=5)
payment_graph_frame = LabelFrame(app, text="Payment Graph", width=600, height=185, padx=5, pady=5)
breakdown_graph_frame = LabelFrame(app, text="Breakdown Graph", width=600, height=185, padx=5, pady=3)

# Labels
instructions_label = Label(app, text="""Enter all requested information and press calculate to get results based on latest average mortgage rates published by """, 
                           font=("TkDefaultFont",15))
link_label = Label(app, text="FRED", fg="#0070FF", underline=1, cursor="hand2", font=("TkDefaultFont", 15))
link_label.bind("<Button-1>", interactions.open_link)
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

# Create a matplotlib figure with a pie chart to put in canvas, match colors of all objects to app
r, b, g = app.winfo_rgb(app.cget("bg"))
pie_chart = Figure(figsize=(5.875, 1.6), dpi=100)
pie_chart.set_facecolor((r/65535, b/65535, g/65535, 1))
gs = pie_chart.add_gridspec(1, 1, left=0, right=0.3)
ax = pie_chart.add_subplot(gs[0, 0])
sizes = [25, 25, 25, 25]
colors = ["orange", "green", "teal", "yellow"]
labels = [f'Principle: {0}', f'Mortgage Insurance: {0}', f'Home Insurance: {0}', f'Property Taxes: {0}']
ax.pie(sizes, colors=colors, startangle=90, radius=1.5)
legend = ax.legend(labels, loc="center left", bbox_to_anchor=(1.2, 0.5))
legend.get_frame().set_facecolor((r/65535, b/65535, g/65535, 1))
legend.get_frame().set_edgecolor("none")

for text in legend.get_texts():
    text.set_color("white")

# Canvas
canvas = FigureCanvasTkAgg(pie_chart, master=breakdown_graph_frame)
canvas.draw()
canvas.get_tk_widget().place(x=0,y=0)

# Dropboxes
input_loan_data_list = Listbox(app, width=96, height=15, borderwidth=0, bg=app.cget('bg'))
input_loan_data_list.insert(END, "* Home Price: Purchase price of the home you're trying to buy.")
input_loan_data_list.insert(END, "* Down Payment Percentage: Percentage of purchase price that is being used as a down payment.")
input_loan_data_list.insert(END, "* Loan Term: Length of time to repay the loan.")
input_loan_data_list.insert(END, "* Credit Score (Optional): Score reported by credit bureaus used by loan companies to adjust loan interest rate based on percieved risk.")
input_loan_data_list.insert(END, "* Zip Code: Zip code of the property you are trying to purchase. This will effect the property taxes and insurance rates.")
input_loan_data_list.insert(END, "*")
input_loan_data_list.insert(END, "** If credit score not entered 7.0 percent interest rate will be used for 30 year.")
input_loan_data_list.insert(END, "*")
input_loan_data_list.insert(END, "* Principle & Interest: The portion of your monthly payment that goes directly to total loan ammount and interest from that.")
input_loan_data_list.insert(END, "* Property Tax: Taxes payed to the state for owning property. ** 1.2 percent used as estimate but values vary by location")
input_loan_data_list.insert(END, "* Mortgage Insurance: Insurance payed to loan company while less than 20 percent of the loan is payed.")
input_loan_data_list.insert(END, "* Home Insurance: Insurance for your home required by loan companies. ** 1400 used as an estimate but values very by location.")
input_loan_data_list.insert(END, "*")
input_loan_data_list.insert(END, "** Breakdown graph percentages may not equal 100 percent exactly because of small rounding errors.")

# Buttons

calculate_button = Button(loan_data_frame, text="Calculate", 
                          command=lambda:interactions.calculate_click(int(home_price.get()), int(down_payment_clicked.get()), 
                                                                      int(loan_term_clicked.get()), credit_score.get(), 
                                                                      principle_number, property_tax_number, home_insurance_number, 
                                                                      pmi_number, total_number, ax, canvas, (r/65535, b/65535, g/65535, 1)))
clear_button = Button(app, text="Clear", 
                      command=lambda:interactions.pop_up(principle_number, property_tax_number, pmi_number, home_insurance_number,
                                                         total_number, home_price, down_payment_clicked, loan_term_clicked,credit_score, 
                                                         zipcode, ax, canvas, (r/65535, b/65535, g/65535, 1)))

show_hide_button = Button(app, text="Show/Hide", command=lambda:interactions.show_hide_click(input_loan_data_list))

# Widget placement on the screen
instructions_label.place(x=15, y=10)
link_label.place(x=830,y=10)

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
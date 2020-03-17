# Basic imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

# css
colors = {"background": "grey"}
# Getting the dataset
data = pd.read_csv("Data/training.csv")

# A bit of housekeeping (data cleaning)
# Renaming Columns 
columns_names = {"Q1":"age", "Q2": "gender", "Q3":"marital_status",
                 "Q4":"education", "Q5":"residents", "Q6": "land_ownership",
                 "Q7": "mobile_phone_ownership", "Q8_1": "salaries_or_Wages",
                 "Q8_2": "trading", "Q8_3": "services", "Q8_4": "piece_work",
                 "Q8_5": "rental_income", "Q8_6": "interest", "Q8_7": "pension",
                 "Q8_8": "welfare", "Q8_9": "rely_on_someone", "Q8_10": "dependent",
                 "Q8_11": "other", "Q9": "employeer", "Q10": "trading_goods", 
                 "Q11": "type_of_Service", "Q12":"sent_money", "Q13": "transfer_money",
                 "Q14": "received_money", "Q15": "received_money_days", "Q16":"usage_goods_services", "Q17":"usage_bills",
                 "Q18": "literacy_in_kiswhahili", "Q19": "literacy_in_english"}

data = data.rename(columns_names, axis=1)

# Adding categorical variables
gender_names = {1: "Male", 2: "Female"}
data["Gender"] = data["gender"].map(gender_names)

marital_names ={1: "Married", 2: "Divorced", 3: "Widowed", 4: "Single/Never Married"}
data["Marital Status"] = data["marital_status"].map(marital_names)

education_names = {1: "No Formal Education", 2: "Some Primary", 3: "Primary Completed", 4: "Post Primary", 5: "Some Secondary", 6: "University", 7: "Don't Know"}
data["Education"] = data["education"].map(education_names)

land_ownership_names = {1: "Yes", 2: "No"}
data["Land Ownership"] = data["land_ownership"].map(land_ownership_names)

usage_goods_services_names = {-1: "not applicable", 1: "Never", 2: "Daily", 3: "Weekly", 4: "Monthly", 5: "Less often than monthly"}
data["Usage Goods Service"] = data["usage_goods_services"].map(usage_goods_services_names)

usage_bills_names = {-1: "not applicable", 1: "Never", 2: "Daily", 3: "Weekly", 4: "Monthly", 5: "Less often than monthly"}
data["Usage Bills"] = data["usage_bills"].map(usage_bills_names)

mobile_money_classification_names = {0: "No Mobile Money and no other Financial Service", 1: "No Mobile Money, one other financial service", 2: "Mobile Money Only", 3: "Mobile Money plus"}
data["Mobile Money Classification"] = data["mobile_money_classification"].map(mobile_money_classification_names)

# chart1 dataset
df = pd.DataFrame(data["Mobile Money Classification"].value_counts()).reset_index()

# chart2 dataset
male_with_mm = data[(data["gender"] == 1) & (data["mobile_money_classification"] != 10)]
female_with_mm = data[(data["gender"] == 2) & (data["mobile_money_classification"] != 10)]


fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"type": "domain"}, {"type": "domain"}]],
)

fig.add_trace(go.Pie(labels=male_with_mm["Mobile Money Classification"].values, values= male_with_mm["mobile_money_classification"].values, title="Males with Money Mobile"),
              row=1, col=1)

fig.add_trace(go.Pie(labels=female_with_mm["Mobile Money Classification"].values, values= female_with_mm["mobile_money_classification"].values, title="Females with Money Mobile"),
              row=1, col=2)

# chart3 dataset
income_data = data[data["mobile_money"] == 1]

types_of_income = income_data[['salaries_or_Wages','trading', 'services', 'piece_work', 'rental_income', 'interest',
       'pension', 'welfare', 'rely_on_someone', 'dependent', 'other']]

labels = []
values = []

for i in types_of_income:
    labels.append(i)
    values.append(sum(types_of_income[i]))

chart_data = [
        {
            'values': values,
            'labels': labels,
            'type': 'pie'
        }
    ]

# Create app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='chart1',
            figure={
                'data': [
                     {'x': df["index"].values, 
                     'y': df["Mobile Money Classification"].values,
                     'type': 'bar', 
                     'name': 'Pay Rate'},
                    ],
                'layout': {
                    'title': 'Tanzania Mobile Money Market Dashboard',
                    'xaxis': {'title': 'Mobile Money Users'},
                    'yaxis': {'title': 'Number of Users'}
                }
            }
        )

    ], className="part1"),

    html.Div([
        html.Div([
            dcc.Graph(
                figure=fig     
            )


        ], className="gender"),

        html.Div([
            dcc.Graph(
                figure=px.histogram(data, data.age, color="Mobile Money Classification",nbins=20, opacity=0.60)          
            )

        ], className="age")

    ], className="part2"),

    html.Div([
         html.Div([
            dcc.Graph(
                    id='graph',
                    figure={
                        'data': chart_data,
                        'layout': {"title": "Source of Income for Mobile Money Users"}

            }
        )           
        ])
    ], className="part3"),


    
])


# Run the app
if __name__ == "__main__":
    app.run_server(debug= True)
import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go
import json

class Suspension_histogram_conversion:
    LINPOT_CONVERSION_CONSTANT = 15.0
    LINPOT_CONVERSION_OFFSET = 75.0
    MM_TO_IN_CONVERSION_FACTOR = 0.0393701 
    
    def __init__(self, file_name: str):
        with open(file_name, 'r') as file:
            data = json.load(file)
        self.linpot_data = pd.DataFrame.from_dict(data, orient='columns')
        self.switch_columns()  # Remove self argument
        self.displacement_data = self.convert_volt_to_mm()  # Remove self argument
    
    def switch_columns(self):
        # Fixed: This mapping now swaps correctly
        self.linpot_data = self.linpot_data.rename(
            columns={
                "Front Right": "temp",
                "Front Left": "Rear Left",
                "Rear Left": "Front Right",
                "temp": "Front Left"
            }
        )
    
    def convert_volt_to_mm(self):
        # Vectorized operations - much faster than iterrows()
        displacement_to_mm = self.linpot_data.copy()
        
        displacement_to_mm["Front Right"] = (
            displacement_to_mm["Front Right"] * self.LINPOT_CONVERSION_CONSTANT 
            + self.LINPOT_CONVERSION_OFFSET
        )
        displacement_to_mm["Front Left"] = (
            -displacement_to_mm["Front Left"] * self.LINPOT_CONVERSION_CONSTANT 
            + self.LINPOT_CONVERSION_OFFSET
        )
        displacement_to_mm["Rear Right"] = (
            -displacement_to_mm["Rear Right"] * self.LINPOT_CONVERSION_CONSTANT 
            + self.LINPOT_CONVERSION_OFFSET
        )
        displacement_to_mm["Rear Left"] = (
            -displacement_to_mm["Rear Left"] * self.LINPOT_CONVERSION_CONSTANT 
            + self.LINPOT_CONVERSION_OFFSET
        )
        
        return displacement_to_mm
    
    def suspension_histogram(self):
        app = Dash(__name__)
        app.layout = html.Div([
            html.H4("Suspension Histogram:"),
            dcc.Graph(
                id="suspension-histograms",
                figure={
                    "data": [
                        go.Histogram(
                            x=self.displacement_data["Front Right"], 
                            name="Front Right",
                            opacity=0.7
                        ),
                        go.Histogram(
                            x=self.displacement_data["Front Left"], 
                            name="Front Left",
                            opacity=0.7
                        ),
                        go.Histogram(
                            x=self.displacement_data["Rear Right"], 
                            name="Rear Right",
                            opacity=0.7
                        ),
                        go.Histogram(
                            x=self.displacement_data["Rear Left"], 
                            name="Rear Left",
                            opacity=0.7
                        ),
                    ],
                    "layout": go.Layout(
                        title="Suspension Displacement (mm)",
                        xaxis=dict(title="Displacement (mm)"),
                        yaxis=dict(title="Count"),

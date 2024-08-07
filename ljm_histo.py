import pandas as pd
from dash import Dash, dcc, html, Input, Output
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
        self.switch_columns(self)
        self.displacement_data = self.convert_volt_to_mm(self)

    def switch_columns(self):
        self.linpot_data = self.linpot_data.rename(
                columns={
                    "Front Right": "Front Left",
                    "Front Left": "Rear Left",
                    "Rear Left": "Front Right",
                }
        )

    def convert_volt_to_mm(self):
        displacement_to_mm = self.linpot_data.copy()

        for i, row in displacement_to_mm.iterrows():
            displacement_to_mm.loc[i, "Front Right"] = (
                row["Front Right"] * self.LINPOT_CONVERSION_CONSTANT) + self.LINPOT_CONVERSION_OFFSET
            displacement_to_mm.loc[i, "Front Left"] = -(row["Front Left"] * self.LINPOT_CONVERSION_CONSTANT) + self.LINPOT_CONVERSION_OFFSET
            displacement_to_mm.loc[i, "Rear Right"] = -(row["Rear Right"] * self.LINPOT_CONVERSION_CONSTANT) + self.LINPOT_CONVERSION_OFFSET
            displacement_to_mm.loc[i, "Rear Left"] = -(row["Rear Left"] * self.LINPOT_CONVERSION_CONSTANT) + self.LINPOT_CONVERSION_OFFSET

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
                                x=self.displacement_data["Front Right"], name="Front Right"
                            ),
                            go.Histogram(
                                x=self.displacement_data["Front Left"], name="Front Left"
                            ),
                            go.Histogram(
                                x=self.displacement_data["Rear Right"], name="Rear Right"
                            ),
                            go.Histogram(
                                x=self.displacement_data["Rear Left"], name="Rear Left"
                            ),
                        ],
                        "layout": go.Layout(
                            title="Suspension Displacement (mm)",
                            xaxis=dict(title="Displacement (mm)"),
                            yaxis=dict(title="Count"),
                            barmode="overlay",
                        ),
                    },
                ),
            ])
        
        app.run_server(debug=True)

if __name__ == "__main__":
    processor = Suspension_histogram_conversion("file.ljm")
    processor.suspension_histogram()

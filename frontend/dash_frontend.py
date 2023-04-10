import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from markupsafe import escape as url_escape
import jinja2

import os
import pandas as pd
import joblib

# Set up the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

# Define the upload component
upload_component = dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select Files')
    ]),
    style={
        'width': '50%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    },
    multiple=False
)

# Define the submit button
submit_button = html.Button('Submit', id='submit-button', n_clicks=0, style={'margin': '10px'})

# Define the output component
output_component = html.Div(id='output-data-upload')

# Define the app layout
app.layout = html.Div([
    upload_component,
    submit_button,
    output_component
])

# Define the callback function
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('upload-data', 'filename'),
     State('upload-data', 'contents')])
def update_output(n_clicks, filename, contents):
    if n_clicks == 0:
        return ''
    elif not filename or not contents:
        return 'No file selected'
    else:
        # Write the contents to a temporary file
        _, file_extension = os.path.splitext(filename)
        temp_file_path = f'/tmp/{filename}'
        with open(temp_file_path, 'wb') as f:
            f.write(contents.encode('utf8'))

        # Load the model and make predictions
        model_path = 'path/to/model.pkl'
        model = joblib.load(model_path)
        df = pd.read_csv(temp_file_path)
        predictions = model.predict(df)

        # Render the results using a Jinja2 template
        template = jinja2.Template('''
            <table>
            <thead>
                <tr>
                    {% for col in predictions.columns %}
                        <th>{{ col }}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for index, row in predictions.iterrows() %}
                <tr>
                    {% for col in predictions.columns %}
                        <td>{{ row[col] }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </tbody>
        </table>
        ''')
        html_table = template.render(predictions=predictions)
        
        # Remove the temporary file
        os.remove(temp_file_path)

        # Return the results
        return html_table

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

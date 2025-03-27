from flask import Flask, jsonify, render_template
import plotly.express as px
import plotly.io as pio


app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_data():
    fig = px.scatter(x=[1, 2, 3, 4, 5], y=[10, 11, 12, 13, 14], title="Simple Plotly Graph")

    # Convert the plot to HTML
    graph_html = pio.to_html(fig, full_html=False)

    # Pass the graph HTML to the template
    return render_template('index.html', graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
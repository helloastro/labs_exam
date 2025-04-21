import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import io

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure

from flask import request, render_template, Response, redirect, url_for, make_response, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

from src_web.webapp2 import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../lab.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://madang:madang@localhost:3306/madangdb'
db = SQLAlchemy(app)

@app.route('/iris/list')
def iris_list():
    return render_template('/iris/list.html')

@app.route('/iris/ajax/list', methods=['POST'])
def iris_ajax_list():
    sql = 'select * from t_iris'
    df = pd.read_sql(sql, db.get_engine())

    return '{"data":' + df.to_json(orient = 'values') + '}'

@app.route('/iris/ajax/model', methods=['POST'])
def iris_ajax_model():
    jsons = request.form.to_dict(flat=False)

    iris_names = joblib.load('webapp2/ml/iris_names.pkl')
    df_clf = joblib.load('webapp2/ml/iris_model.pkl')
    label = df_clf.predict([[jsons['sl'][0], jsons['sw'][0], jsons['pl'][0], jsons['pw'][0]]])

    return {'result':iris_names[label][0]} 

@app.route('/iris/chart')
def iris_chart():
    return render_template('/iris/chart.html')

@app.route('/iris/chart/pie.png')
def iris_chart_pie():
    sql = 'select * from t_iris'
    df = pd.read_sql(sql, db.get_engine())

    species = df['species'].value_counts()
    keys = species.index
    data = species.values
    palette_color = sns.color_palette('bright')

    plt.rcParams['font.size'] = '20'

    fig = plt.figure()
    plt.pie(data, labels=keys, colors=palette_color, autopct='%.0f%%')
    plt.tight_layout()
    output = io.BytesIO()
    # FigureCanvasAgg(fig).print_png(output)

    # return Response(output.getvalue(), mimetype="image/png")

    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")

@app.route('/iris/chart/datas', methods=['POST'])
def iris_chart_datas():
    df = pd.DataFrame({'year':[n for n in range(2000,2010)], 'sales':np.random.randint(2000, 10000, size=10)})

    result = {
        'labels': df['year'].tolist(),
        'datas': df['sales'].tolist()
    }
    return result    

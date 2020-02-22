
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
import pandas as pd

use_col = "     -----     "
use_key = "     -----     "

data_xlsx = pd.ExcelFile('data/database.xlsx').parse()
data_dic_original = {ind: [v for v in data_xlsx.loc[ind].values] for ind in data_xlsx.index}
data_col = list(data_xlsx.columns)

def getRefineDic(pd_main):
    search_dic = {}
    group_list = []

    for c, col in enumerate(data_col):
        data_temp = pd_main.iloc[:, c]
        key_list = [v for v in set(data_temp) if v != "-"]
        key_list = sorted([k for k in key_list if str(k) != "<"])

        if c == 0:
            group_list = key_list
        else:
            search_dic[col] = key_list

    return search_dic, group_list


search_dic, group_list = getRefineDic(pd_main=data_xlsx)

"""
box = []
for ind in data_xlsx.index:
    for No, v in enumerate(data_xlsx.loc[ind].values):
        if No == 4:
            if (str(v) != "nan") and ("(" in v):
                name = v.split("(")[0]
                hospital = v.split("(")[1].split(")")[0]
            else:
                name = v
                hospital = ""

            print(name, hospital)
            box += [name]

temp = pd.DataFrame(box)
temp.to_csv("a.csv", encoding="cp932")
"""

app = Flask(__name__, static_url_path="")
bootstrap = Bootstrap(app)

DATA_DIR = "./data"
@app.route('/data/<path:path>')
def send_js(path):
    return send_from_directory(DATA_DIR, path)


@app.route('/')
def index():
    app.config['data_dic'] = data_dic_original
    app.config['search_dic'] = search_dic
    app.config['use_col'] = use_col
    app.config['use_key'] = use_key
    app.config['use_group'] = None
    app.config['group_list'] = group_list

    return render_template('index_bootStrap.html',
                           data_dic=app.config['data_dic'], search_dic=app.config['search_dic'],
                           use_col=app.config['use_col'], use_key=app.config['use_key'],
                           group_list=app.config['group_list'], use_group=app.config['use_group'])


@app.route('/data_group', methods=['POST', 'GET'])
def data_group():
    app.config['use_group'] = request.form["btn"]
    pd_temp = data_xlsx[data_xlsx.iloc[:, 0] == app.config['use_group']]
    app.config['search_dic'], group_list = getRefineDic(pd_main=pd_temp)
    # app.config['search_dic'].update({"aa": aaa})

    index_use = list(data_xlsx[data_xlsx.iloc[:, 0] == app.config['use_group']].index)
    app.config['data_dic'] = {ind: [v for v in data_xlsx.loc[ind].values] for ind in index_use}

    return render_template('index_bootStrap.html',
                           data_dic=app.config['data_dic'], search_dic=app.config['search_dic'],
                           use_col=app.config['use_col'], use_key=app.config['use_key'],
                           group_list=app.config['group_list'], use_group=app.config['use_group'])


@app.route('/data_refine', methods=['POST', 'GET'])
def data_refine():
    print("A", request.form["btn"])
    if request.form["btn"] == "全て表示":
        app.config['data_dic'] = data_dic_original
        app.config['use_col'] = use_col
        app.config['use_key'] = use_key
        app.config['use_group'] = None

    elif request.form["btn"] == "絞り込む":
        app.config['use_col'] = request.form.get('select_refine1')
        app.config['use_key'] = request.form.get('select_refine2')
        index_use = [ind for ind in list(data_xlsx.index) if data_xlsx.loc[ind, app.config['use_col']] == app.config['use_key']]
        app.config['data_dic'] = {ind: [v for v in data_xlsx.loc[ind].values] for ind in index_use}

    return render_template('index_bootStrap.html',
                           data_dic=app.config['data_dic'], search_dic=app.config['search_dic'],
                           use_col=app.config['use_col'], use_key=app.config['use_key'],
                           group_list=app.config['group_list'], use_group=app.config['use_group'])


if __name__ == '__main__':
    app.run(debug=True)

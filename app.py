

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
import pandas as pd

path_excel = 'data/database.xlsx'
data_pd = pd.ExcelFile(path_excel).parse()


"""

box = []
for ind in data_xlsx.index:
    value =  data_xlsx.iloc[ind, 3]
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


class antiDoping:
    def __init__(self, path_excel):
        # stable parameter
        self.data_pd = None
        self.data_col = None
        self.data_group = None
        self.data_dic_original = None
        self.path_excel = path_excel
        self.additional_column = "全部"

        # variable parameter
        self.data_dic = None
        self.data_pd_display = None
        self.data_pd_use = None
        self.data_num = None
        self.search_dic = None
        self.step = None
        self.popup_message = None

        self.use_col = None
        self.use_key = None
        self.use_group = self.additional_column

        # Start
        self.read_excel()
        self.data_dic_original, self.search_dic_all = self.getRefineDic()
        self.setInitConfigure()
        self.step = 0

    def read_excel(self):
        self.data_pd = pd.ExcelFile(self.path_excel).parse()
        self.data_col = list(self.data_pd.columns)
        self.data_group = list(set(self.data_pd.iloc[:, 0]))
        self.data_group = self.data_group + [self.additional_column]

        self.data_pd_use = self.data_pd
        self.data_pd_display = self.data_pd

    def setInitConfigure(self):
        self.data_dic = self.data_dic_original
        self.data_pd_use = self.data_pd
        self.data_pd_display = self.data_pd
        self.search_dic = self.search_dic_all
        self.data_num = len(self.data_dic)

    def getRefineDic(self):
        self.step = 1
        self.data_dic = {ind: list(self.data_pd_use.loc[ind].values) for ind in self.data_pd_use.index}

        self.search_dic = {}
        for c, col in enumerate(self.data_col):
            data_temp = self.data_pd_use.iloc[:, c]
            key_list = [v for v in set(data_temp) if v != "-"]
            key_list = sorted([k for k in key_list if str(k) != "<"])
            self.search_dic[col] = key_list
        return self.data_dic, self.search_dic


app = Flask(__name__, static_url_path="")
bootstrap = Bootstrap(app)

DATA_DIR = "./data"
@app.route('/data/<path:path>')
def send_js(path):
    return send_from_directory(DATA_DIR, path)


@app.route('/')
def index():
    ad = antiDoping(path_excel=path_excel)
    app.config['ad'] = ad
    return render_template('index_bootStrap.html', ad=app.config['ad'])


@app.route('/data_group', methods=['POST', 'GET'])
def data_group():
    ad = app.config['ad']
    ad.use_group = request.form["btn"]

    if ad.use_group == "全部":
        ad.setInitConfigure()

    else:
        ad.data_pd_use = ad.data_pd[ad.data_pd.iloc[:, 0] == ad.use_group]
        ad.getRefineDic()

    ad.data_num = len(ad.data_dic)
    app.config['ad'] = ad

    return render_template('index_bootStrap.html', ad=app.config['ad'])


@app.route('/data_refine', methods=['POST', 'GET'])
def data_refine():
    ad = app.config['ad']
    ad.data_pd_use = ad.data_pd if ad.use_group == "全部" else ad.data_pd[ad.data_pd.iloc[:, 0] == ad.use_group]

    ad.use_col = request.form.get('select_refine1')
    ad.use_key = request.form.get('select_refine2')

    print("use_col: ", ad.use_col)
    print("use_key: ", ad.use_key)

    if (not ad.use_col) or (not ad.use_key):
        ad.popup_message = "選択されていない情報があります"
    else:
        ad.data_pd_display = ad.data_pd_use[ad.data_pd_use.loc[:, ad.use_col] == ad.use_key]
        ad.data_dic = {ind: list(ad.data_pd_display.loc[ind].values) for ind in ad.data_pd_display.index}
        ad.data_num = len(ad.data_dic)
        ad.popup_message = None

    print("ad.popup_message: ", ad.popup_message)

    return render_template('index_bootStrap.html', ad=app.config['ad'])


if __name__ == '__main__':
    app.run(debug=True)

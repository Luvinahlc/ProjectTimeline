from flask import render_template
from app import app
from random import choice
import pyodbc

Color = ['red', 'green', 'orange', 'magenta', 'default']

def initData():
    cnxn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=tcp:t-luhua.database.windows.net,1433;Database=projectInfoDB;Uid=t-luhua@t-luhua;Pwd={Luvina&921109};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
    cursor.execute("use projectInfoDB")
    cursor.execute("select * from ProjectInfo")
    rows = cursor.fetchall()
    data = []
    for row in rows:
        content = row.name_P + '--' + row.milestone
        
        lineData = {#'start': row.startDate,
                    #'end': row.endDate,
                    'start': row.endDate,
                    'content': content,
                    'className': choice(Color)
                    }
        '''
        [{'key': 'ID', 'value': row.ID_P},
        {'key': 'name', 'value': row.name_P},
        {'key': 'startDate', 'value': row.startDate},
        {'key': 'endDate', 'value': row.endDate},
        {'key': 'milestone', 'value': row.milestone},
        {'key': 'priority', 'value': row.priority_p}]
        '''
        data.append(lineData)
    return data



@app.route('/')
@app.route('/index')
def index():
    initalData = initData()
    return render_template("index.html",
        title = 'Home', initalData = initalData
        )

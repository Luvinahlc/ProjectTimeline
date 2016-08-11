from flask import render_template, request, jsonify
from app import app
from random import choice
import pyodbc

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
        title = 'Home')


@app.route('/get')
def get():
    cnxn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=tcp:t-luhua.database.windows.net,1433;Database=projectInfoDB;Uid=t-luhua@t-luhua;Pwd={Luvina&921109};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
    cursor.execute("use projectInfoDB")
    cursor.execute("select * from ProjectInfo")
    rows = cursor.fetchall()
    data = []
    for row in rows:
        lineData = {'DT_RowId': "row_"+str(row.ID_P),
                    #'ID_P': row.ID_P,
                    'name_P': row.name_P,
                    'start_date': row.startDate,
                    'end_date': row.endDate,
                    'milestone': row.milestone,
                    'priority_p': row.priority_p
                    }
        data.append(lineData)
    table = {"data": data}
    cursor.close()
    cnxn.close()
    return jsonify(table)


@app.route('/post', methods = ['POST'])
def post():
    formData = request.form
    #id_p = formData['data[0][ID_P]']
    name_p = formData['data[0][name_P]']
    start_date = formData['data[0][start_date]']
    end_date = formData['data[0][end_date]']
    milestone = formData['data[0][milestone]']
    priority_p = formData['data[0][priority_p]']

    cnxn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=tcp:t-luhua.database.windows.net,1433;Database=projectInfoDB;Uid=t-luhua@t-luhua;Pwd={Luvina&921109};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
    cursor.execute("use projectInfoDB")

    sql = "insert into ProjectInfo (name_P, startDate, endDate, milestone, priority_p) values(?, ?, ?, ?, ?)"
    param = [name_p, start_date, end_date, milestone, priority_p]

    cursor.execute(sql, param)

    cnxn.commit()

    sql_query = "select * from ProjectInfo where name_P = ? and startDate = ? and endDate = ? and milestone = ? and priority_p = ?"
    cursor.execute(sql_query, param)
    rows = cursor.fetchall()
    id_p = rows[0].ID_P

    addData = {'DT_RowId': 'row_'+str(id_p),
               #'ID_P': id_p,
               'name_P': name_p,
               'start_date': start_date,
               'end_date': end_date,
               'milestone': milestone,
               'priority_p': priority_p
    }
    newItem = {"data": [addData]}
    cursor.close()
    cnxn.close()
    return jsonify(newItem)


@app.route('/put', methods = ['PUT'])
def put():
    formData = request.form
    temp_str = request.form.keys()[1]
    print(temp_str)
    temp_str_list = temp_str.split('[');
    print(temp_str_list)
    row_id = temp_str_list[1][0:(len(temp_str_list[1])-1)]
    id_p = int(row_id[4:(len(row_id))])
    name_p = formData['data['+row_id+'][name_P]']
    start_date = formData['data['+row_id+'][start_date]']
    end_date = formData['data['+row_id+'][end_date]']
    milestone = formData['data['+row_id+'][milestone]']
    priority_p = formData['data['+row_id+'][priority_p]']

    cnxn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=tcp:t-luhua.database.windows.net,1433;Database=projectInfoDB;Uid=t-luhua@t-luhua;Pwd={Luvina&921109};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
    cursor.execute("use projectInfoDB")


    sql = "update ProjectInfo set name_P = ? , startDate = ? , endDate = ? , milestone = ? , priority_p = ? where ID_P = ?"
    param = [name_p, start_date, end_date, milestone, priority_p, id_p]

    cursor.execute(sql, param)

    cnxn.commit()

    editData = {'DT_RowId': 'row_'+str(id_p),
               #'ID_P': id_p,
               'name_P': name_p,
               'start_date': start_date,
               'end_date': end_date,
               'milestone': milestone,
               'priority_p': priority_p
    }
    editItem = {"data": [editData]}

    cursor.close()
    cnxn.close()
    return jsonify(editItem)

@app.route('/delete', methods = ['DELETE'])
def delete_entry():
    deleteData = request.args.to_dict()
    temp_str = request.args.to_dict().keys()[0]
    temp_str_list = temp_str.split('[');
    row_id = temp_str_list[1][0:(len(temp_str_list[1])-1)]
    id_p = int(row_id[4:(len(row_id))])
    '''
    name_p = deleteData['data['+row_id+'][name_P]']
    start_date = deleteData['data['+row_id+'][start_date]']
    end_date = deleteData['data['+row_id+'][end_date]']
    milestone = deleteData['data['+row_id+'][milestone]']
    priority_p = deleteData['data['+row_id+'][priority_p]']
    '''
    cnxn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=tcp:t-luhua.database.windows.net,1433;Database=projectInfoDB;Uid=t-luhua@t-luhua;Pwd={Luvina&921109};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
    cursor.execute("use projectInfoDB")

    sql = "delete from ProjectInfo where ID_P = ?"# and name_P = ? and startDate = ? and endDate = ? and milestone = ? and priority_p = ?"
    param = [id_p]#, name_p, start_date, end_date, milestone, priority_p]

    cursor.execute(sql, param)

    cnxn.commit()

    cursor.close()
    cnxn.close()

    return jsonify({"data": []})
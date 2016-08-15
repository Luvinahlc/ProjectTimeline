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
                    'name_P': row.name_P,
                    'end_date': row.endDate,
                    'milestone': row.milestone,
                    'level': row.level,
                    'missed': row.missed
                    }
        data.append(lineData)

    cursor.execute("select distinct name_P from ProjectInfo")
    rows = cursor.fetchall()
    projectNames = []
    for row in rows:
        projectNames.append(row.name_P)

    table = {"data": data, "projectNames": projectNames}
    cursor.close()
    cnxn.close()
    return jsonify(table)


@app.route('/post', methods = ['POST'])
def post():
    formData = request.form
    name_p = formData['data[0][name_P]']
    end_date = formData['data[0][end_date]']
    milestone = formData['data[0][milestone]']
    level = formData['data[0][level]']
    missed = formData['data[0][missed]']

    cnxn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=tcp:t-luhua.database.windows.net,1433;Database=projectInfoDB;Uid=t-luhua@t-luhua;Pwd={Luvina&921109};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
    cursor.execute("use projectInfoDB")

    sql = "insert into ProjectInfo (name_P, endDate, milestone, level, missed) values(?, ?, ?, ?, ?)"
    param = [name_p, end_date, milestone, level, missed]

    cursor.execute(sql, param)

    cnxn.commit()

    sql_query = "select * from ProjectInfo where name_P = ? and endDate = ? and milestone = ? and level = ? and missed = ? "
    cursor.execute(sql_query, param)
    rows = cursor.fetchall()
    id_p = rows[0].ID_P

    addData = {'DT_RowId': 'row_'+str(id_p),
               'name_P': name_p,
               'end_date': end_date,
               'milestone': milestone,
               'level': level,
               'missed': missed
    }
    newItem = {"data": [addData]}
    cursor.close()
    cnxn.close()
    return jsonify(newItem)


@app.route('/put', methods = ['PUT'])
def put():
    formData = request.form
    temp_str = formData.keys()[1]
    temp_str_list = temp_str.split('[');
    row_id = temp_str_list[1][0:(len(temp_str_list[1])-1)]
    id_p = int(row_id[4:(len(row_id))])
    name_p = formData['data['+row_id+'][name_P]']
    end_date = formData['data['+row_id+'][end_date]']
    milestone = formData['data['+row_id+'][milestone]']
    level = formData['data['+row_id+'][level]']
    missed = formData['data['+row_id+'][missed]']

    cnxn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=tcp:t-luhua.database.windows.net,1433;Database=projectInfoDB;Uid=t-luhua@t-luhua;Pwd={Luvina&921109};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
    cursor.execute("use projectInfoDB")


    sql = "update ProjectInfo set name_P = ? , endDate = ? , milestone = ? , level = ? , missed = ? where ID_P = ?"
    param = [name_p, end_date, milestone, level, missed, id_p]

    cursor.execute(sql, param)

    cnxn.commit()

    editData = {'DT_RowId': 'row_'+str(id_p),
               'name_P': name_p,
               'end_date': end_date,
               'milestone': milestone,
               'level': level,
               'missed': missed
    }
    editItem = {"data": [editData]}

    cursor.close()
    cnxn.close()
    return jsonify(editItem)

@app.route('/delete', methods = ['DELETE'])
def delete_entry():
    cnxn = pyodbc.connect('Driver={SQL Server Native Client 11.0};Server=tcp:t-luhua.database.windows.net,1433;Database=projectInfoDB;Uid=t-luhua@t-luhua;Pwd={Luvina&921109};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    cursor = cnxn.cursor()
    cursor.execute("use projectInfoDB")

    deleteData = request.args.to_dict()

    for temp_str in deleteData.keys():
        temp_str_list = temp_str.split('[');
        if len(temp_str_list) > 1 :
            row_id = temp_str_list[1][0:(len(temp_str_list[1])-1)]
            id_p = int(row_id[4:(len(row_id))])
            sql = "delete from ProjectInfo where ID_P = ?"
            param = [id_p]
            cursor.execute(sql, param)
    
    cnxn.commit()

    cursor.close()
    cnxn.close()

    return jsonify({"data": []})
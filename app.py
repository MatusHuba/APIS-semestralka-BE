"""
Created on Tue Dec 21 20:41:37 2021

@author: matus
"""

HOST="147.232.40.14" 
USER="jd850be"
PASSWD="booTha8p"
DB="jd850be"


from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import mysql.connector as MYSQL

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def main():
    return "Works",200

@app.route("/CreateDriver", methods = ["POST"])
def CreateDriver():
    data = request.get_json(force = True)
    driver_dict = dict(data)
    with open ('DB/create/create_driver.sql') as ddl_file:
        sql = ddl_file.read()
        # sql = sql[:-1] + "'{}','{}','{}'" # takto to nemoze byt ... sql je values("pname", "pphone", "pcar", "pspz");
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    cursor = myDB.cursor()
    sql = sql.replace("pname", driver_dict["pname"]) 
    sql = sql.replace("pphone", driver_dict["pphone"])
    sql = sql.replace("pcar", driver_dict["pcar"])
    sql = sql.replace("pspz", driver_dict["pspz"])
    cursor.execute(sql)
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("created"),201

@app.route("/CreateTransaction", methods = ["POST"])
def CreateTransaction():
    data = request.get_json(force = True)
    transaction_dict = dict(data)
    with open ('DB/create/create_transaction.sql') as ddl_file:
        sql = ddl_file.read()
        #sql = sql[:-1] + "'{}','{}','{}','{}'"
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    cursor = myDB.cursor()
    sql = sql.replace("pcustomer_id", transaction_dict["pcustomer_id"])
    sql = sql.replace("pdriver_id", transaction_dict["pdriver_id"])
    sql = sql.replace("pkm_traveled", transaction_dict["pkm_traveled"])
    sql = sql.replace("pkm_fee", transaction_dict["pkm_fee"])
    cursor.execute(sql)
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("created"),201

@app.route('/GetFreeDrivers', methods=["GET"])
def GetFreeDriver():
    with open ('DB/read/read_free_drivers.sql') as ddl_file:
        sql = ddl_file.read()
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    cursor = myDB.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in result:
        insertObject.append( dict( zip( columnNames , record )))
    cursor.close()
    myDB.close()
    return jsonify(insertObject),200

@app.route('/GetTransactions', methods=["GET"])
def GetTransactions():
    with open ('DB/read/read_number_of_transactions_of_driver_using_time.sql') as ddl_file:
        sql = ddl_file.read()
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    cursor = myDB.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in result:
        insertObject.append( dict( zip( columnNames , record )))
    cursor.close()
    myDB.close()
    return jsonify(insertObject),200


@app.route("/UpdateDriverPersonal", methods = ["PUT"])
def UpdateDriverPersonal():
    _json = request.json
    id  = _json['pid']
    name = _json['pname']
    car = _json['pcar']
    spz = _json['pspz'] 
    with open ('DB/update/update_driver_personal.sql') as ddl_file:
        sql = ddl_file.read()
    #data = (name, car, spz, id,)
    sql = sql.replace("pname", name)
    sql = sql.replace("pcar", car)
    sql = sql.replace("pspz", spz)
    sql = sql.replace("pid", id)
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    cursor = myDB.cursor()
    cursor.execute(sql)
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("updated"),201

@app.route("/UpdateDriverPosition", methods = ["PUT"])
def UpdateDriverPosition():
    _json = request.json
    id  = _json['pid']
    driver_coord = _json['pdriver_coord']
    with open ('DB/update/update_driver_position.sql') as ddl_file:
        sql = ddl_file.read()
    #data = (driver_coord, id,)
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    sql = sql.replace("pdriver_coord", driver_coord)
    sql = sql.replace("pid", id)
    cursor = myDB.cursor()
    cursor.execute(sql)
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("updated"),201

@app.route("/UpdateDriverState", methods = ["PUT"])
def UpdateDriverState():
    _json = request.json
    id  = _json['pid']
    busy =  _json['pbusy']
    with open ('DB/update/update_driver_state.sql') as ddl_file:
        sql = ddl_file.read()
    #data = (busy, id,)
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    sql = sql.replace("pbusy", busy)
    sql = sql.replace("pid", id)
    cursor = myDB.cursor()
    cursor.execute(sql)
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("updated"),201

@app.route("/UpdateDriverStatus", methods = ["PUT"])
def UpdateDriverStatus():
    _json = request.json
    id  = _json['pid']
    online =  _json['ponline']
    with open ('DB/update/update_driver_status.sql') as ddl_file:
        sql = ddl_file.read()
    #data = (online, id,)
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    sql = sql.replace("ponline", online)
    sql = sql.replace("pid", id)
    cursor = myDB.cursor()
    cursor.execute(sql)
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("updated"),201


@app.route("/DeleteCustomer/<id>", methods = ["DELETE"])
def DeleteCustomer(id):
    with open ('DB/delete/delete_customer.sql') as ddl_file:
        sql = ddl_file.read()
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    sql = sql.replace("pid", id)
    cursor = myDB.cursor()
    cursor.execute(sql)
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("deleted"),204

@app.route("/DeleteDriver/<id>", methods = ["DELETE"])
def DeleteDriver(id):
    with open ('DB/delete/delete_driver.sql') as ddl_file:
        sql = ddl_file.read()
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    sql = sql.replace("pid", id)
    cursor = myDB.cursor()
    cursor.execute(sql)
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("deleted"),204

@app.route("/DeleteTransaction/<id>", methods = ["DELETE"])
def DeleteTransaction(id):
    with open ('DB/delete/delete_transaction.sql') as ddl_file:
        sql = ddl_file.read()
        myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
        sql = sql.replace("pid", id)
        cursor = myDB.cursor()
        cursor.execute(sql)
        myDB.commit()
        cursor.close()
        myDB.close()  
        return jsonify("deleted"),204

if __name__ == "__main__":
    app.run()
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
    sql = sql.replace("pname", driver_dict["pname"]) # skus takto
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
    with open ('content/create/create_transaction.ddl') as ddl_file:
        sql = ddl_file.read()
        sql = sql[:-1] + "'{}','{}','{}','{}'"
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    cursor = myDB.cursor()
    cursor.execute(sql.format(transaction_dict["pcustomer_id"], transaction_dict["pdriver_id"], transaction_dict["pkm_traveled"], transaction_dict["pkm_fee"]))
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("created"),201

@app.route('/GetFreeDrivers', methods=["GET"])
def GetFreeDriver():
    with open ('content/read_free_drivers.ddl') as ddl_file:
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
    with open ('content/read_number_of_transactions_of_driver_using_time.ddl') as ddl_file:
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
    with open ('content/update_driver_personal.ddl') as ddl_file:
        sql = ddl_file.read()
    data = (name, car, spz, id,)
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    cursor = myDB.cursor()
    cursor.execute(sql, data)
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("updated"),201

@app.route("/UpdateDriverPosition", methods = ["PUT"])
def UpdateDriverPosition():
    _json = request.json
    id  = _json['pid']
    driver_coord = _json['pdriver_coord']
    with open ('content/update_driver_position.ddl') as ddl_file:
        sql = ddl_file.read()
    data = (driver_coord, id,)
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    cursor = myDB.cursor()
    cursor.execute(sql, data)
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("updated"),201

@app.route("/UpdateDriverState", methods = ["PUT"])
def UpdateDriverState():
    _json = request.json
    id  = _json['pid']
    busy =  _json['pbusy']
    with open ('content/update_driver_state.ddl') as ddl_file:
        sql = ddl_file.read()
    data = (busy, id,)
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    cursor = myDB.cursor()
    cursor.execute(sql, data)
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("updated"),201

@app.route("/UpdateDriverStatus", methods = ["PUT"])
def UpdateDriverStatus():
    _json = request.json
    id  = _json['pid']
    online =  _json['ponline']
    with open ('content/update_driver_status.ddl') as ddl_file:
        sql = ddl_file.read()
    data = (online, id,)
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    cursor = myDB.cursor()
    cursor.execute(sql, data)
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("updated"),201


@app.route("/DeleteCustomer/<id>", methods = ["DELETE"])
def DeleteCustomer(id):
    with open ('content/delete_customer.ddl') as ddl_file:
        sql = ddl_file.read()
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    cursor = myDB.cursor()
    cursor.execute(sql, (id,))
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("deleted"),204

@app.route("/DeleteDriver/<id>", methods = ["DELETE"])
def DeleteDriver(id):
    with open ('content/delete_driver.ddl') as ddl_file:
        sql = ddl_file.read()
    myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
    cursor = myDB.cursor()
    cursor.execute(sql, (id,))
    myDB.commit()
    cursor.close()
    myDB.close()
    return jsonify("deleted"),204

@app.route("/DeleteTransaction/<id>", methods = ["DELETE"])
def DeleteTransaction(id):
    with open ('content/delete_transaction.ddl') as ddl_file:
        sql = ddl_file.read()
        myDB = MYSQL.connect(host=HOST, user=USER, passwd=PASSWD, database=DB)
        cursor = myDB.cursor()
        cursor.execute(sql, (id,))
        myDB.commit()
        cursor.close()
        myDB.close()  
        return jsonify("deleted"),204

if __name__ == "__main__":
    app.run()

from ast import Not
from cgi import print_arguments
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
from utils.connection import postgre_conn
from model import User, Info, Pembayar
from datetime import datetime, timedelta

user = "snqsrxlsxeuzht"
passw = "f2e9ea320454937994d242d196fb285ab7aba6683a5c603812bc3f9bd73592d0"
dtbs = "d54bvqvugsvm71"
host = "ec2-52-3-2-245.compute-1.amazonaws.com"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{}:{}@{}/{}'.format(user,passw,host,dtbs)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def index():
        return jsonify({"message":"Welcome to my site"})

# MODUL USER
@app.route('/user',methods=['GET'])
def getuser():
        all_user = []
        user = User.query.all()
        for usr in user:
                results = {
                        "id_user":usr.id_user,
                        "username":usr.username,
                        "passw":usr.passw,
                        "email":usr.email }
                all_user.append(results)
        return jsonify(
                {
                        "status_code": 200,
                        "data": all_user,
                        "total": len(user),
                        }
                )

@app.route('/signup',methods=['POST'])
def signup():
        try:
                conn = postgre_conn()
                cursor = conn.cursor()
                username = request.json['username']
                passw = request.json['passw']
                email = request.json['email']
                usern = User.query.filter_by(username=username).all()
                mail = User.query.filter_by(email=email).all()
                print(usern, mail)
                if usern:
                        return jsonify({"message": "Username already exists","status_code": 409})
                elif mail:
                        return jsonify({"message": "Email already exists","status_code": 409})
                else:
                        query = "INSERT INTO public.user (username, passw, email) VALUES ('{}','{}','{}')".format(username, passw, email)
                        cursor.execute(query)
                        conn.commit()
                        return jsonify({"message": "User successfully created","status_code": 200})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})
        finally:
                conn.close()

@app.route('/user',methods=['PUT'])
def updateuser():
        try:
                id_user = request.args.get('id_user')
                passw = request.json['passw']
                conn = postgre_conn()
                cursor = conn.cursor()
                query = "UPDATE public.user SET passw='{}' WHERE id_user = {}".format(passw, id_user)
                cursor.execute(query)
                conn.commit()
                return jsonify({"message": "User succesfully updated","status_code": 200})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})
        finally:
                conn.close()

@app.route('/login',methods=['POST'])
def login():
        try:
                username = request.json['username']
                passw = request.json['passw']
                verifikasi = User.query.filter_by(username=username, passw=passw).first()
                if verifikasi:
                        return jsonify({"message": "User succesfully login","status_code": 200})
                else:
                        return jsonify({"message": "Username or password is wrong","status_code": 401})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})


# MODUL INFO
@app.route('/info',methods=['GET'])
def getinfo():
        try:
                info = Info.query.all()
                if info:
                        all_info = []
                        for i in info:
                                results = {
                                        "id_info":i.id_info,
                                        "judul":i.judul,
                                        "keterangan":i.deskripsi }
                                all_info.append(results)
                                
                        return jsonify(
                                {
                                        "status_code": 200,
                                        "data": all_info,
                                        "total": len(info),
                                        }
                                )
                else:
                        return jsonify({'message': 'Data not found', 'status_code': 404})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})

@app.route('/info',methods=['POST'])
def createinfo():
        try:
                judul = request.json['judul']
                deskripsi = request.json['deskripsi']
                conn = postgre_conn()
                cursor = conn.cursor()
                query = "INSERT INTO info (judul, deskripsi) VALUES ('{}','{}')".format(judul, deskripsi)
                cursor.execute(query)
                conn.commit()
                return jsonify({"message": "Data succesfully saved","status_code": 200})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})
        finally:
                conn.close()

@app.route('/info',methods=['PUT'])
def updateinfo():
        try:
                id_info = request.args.get('id_info')
                judul = request.json['judul']
                deskripsi = request.json['deskripsi']
                conn = postgre_conn()
                cursor = conn.cursor()
                query = "UPDATE info SET judul='{}', deskripsi='{}' WHERE id_info = {}".format(judul, deskripsi, id_info)
                cursor.execute(query)
                conn.commit()
                return jsonify({"message": "Data succesfully updated","status_code": 200})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})
        finally:
                conn.close()

@app.route('/info',methods=['DELETE'])
def deleteinfo():
        try:
                id_info = request.args.get('id_info')
                conn = postgre_conn()
                cursor = conn.cursor()
                query = "DELETE from info where id_info = {} ".format(id_info)
                cursor.execute(query)
                conn.commit()
                return jsonify({"message": "Data succesfully deleted","status_code": 200})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})
        finally:
                conn.close()


# MODUL PEMBAYARAN
@app.route('/administrasi',methods=['GET'])
def getpembayaran():
        try:
                dataList = Pembayar.query.all()
                print(dataList)
                if dataList:
                        all_data = []
                        for data in dataList:
                                results = {
                                        "id_bayar":data.id_bayar,
                                        "id_user":data.id_user,
                                        "tgl_bayar":data.tgl_bayar,
                                        "status_bayar":data.status_bayar,
                                        "bukti_tf":str(data.bukti_tf)
                                        }
                                all_data.append(results)
                                print(results)
                                
                        return jsonify(
                                {
                                        "status_code": 200,
                                        "data": all_data,
                                        "total": len(all_data),
                                        }
                                )
                else:
                        return jsonify({'message': 'Data not found', 'status_code': 404})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})

@app.route('/administrasi',methods=['POST'])
def createpembayaran():
        try:
                id_user = request.json['id_user']
                tgl_bayar = request.json['tgl_bayar']
                status_bayar = request.json['status_bayar']
                bukti_tf = request.json['bukti_tf']
                conn = postgre_conn()
                cursor = conn.cursor()
                query = "INSERT INTO pembayar (id_user, tgl_bayar, status_bayar, bukti_tf) VALUES ({},'{}','{}','{}')".format(id_user, tgl_bayar, status_bayar, bukti_tf)
                cursor.execute(query)
                conn.commit()
                return jsonify({"message": "Data payment successfully saved","status_code": 200})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})
        finally:
                conn.close()

@app.route('/administrasi',methods=['PUT'])
def updatepembayaran():
        try:
                id_user = request.args.get('id_user')
                tgl_bayar = request.json['tgl_bayar']
                status_bayar = request.json['status_bayar']
                bukti_tf = request.json['bukti_tf']
                conn = postgre_conn()
                cursor = conn.cursor()
                query = "UPDATE pembayar SET tgl_bayar=TO_DATE('{}', 'DD-MM-YYYY'), status_bayar='{}', bukti_tf='{}' WHERE id_user = {}".format(tgl_bayar, status_bayar, bukti_tf, id_user)
                cursor.execute(query)
                conn.commit()
                return jsonify({"message": " Data payment successfully updated","status_code": 200})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})
        finally:
                conn.close()

@app.route('/administrasi/verify',methods=['PUT'])
def verify_pembayaran():
        try:
                id_user = request.args.get('id_user')
                status_bayar = request.json['status_bayar']
                conn = postgre_conn()
                cursor = conn.cursor()
                query = "UPDATE pembayar SET status_bayar='{}' WHERE id_user = {}".format(status_bayar, id_user)
                cursor.execute(query)
                conn.commit()
                return jsonify({"message": "Payment status successfully updated","status_code": 200})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})
        finally:
                conn.close()

# MODUL PENDAFTARAN
@app.route('/registrasi',methods=['GET'])
def getpendaftar():
        try:
                conn = postgre_conn()
                cursor = conn.cursor()
                query = "SELECT * FROM pendaftar"
                cursor.execute(query)
                dataList = cursor.fetchall()
                if dataList:
                        all_data = []
                        for data in dataList:
                                results = {
                                        "id_reg":data[0],
                                        "id_user":data[1],
                                        "nama":data[2],
                                        "ttl":data[3],
                                        "jenis_kel":data[4],
                                        "agama":data[5],
                                        "no_hp":data[6],
                                        "alamat":data[7],
                                        "asal_sekolah":data[8],
                                        "jurusan_sekolah":data[9],
                                        "nisn":data[10],
                                        "prodi":data[11],
                                        "status_daftar":data[12],
                                        "nama_ayah":data[13],
                                        "status_ortu":data[14],
                                        "pekerjaan":data[15],
                                        "penghasilan":data[16],
                                        "no_hp_ortu":data[17],
                                        "nilai_ijazah":data[18],
                                        "nilai_transkip":data[19],
                                        "foto":str(data[20]),
                                        }
                                all_data.append(results)
                                print(results)
                                
                        return jsonify(
                                {
                                        "status_code": 200,
                                        "data": all_data,
                                        "total": len(all_data),
                                        }
                                )
                else:
                        return jsonify({'message': 'Data not found', 'status_code': 404})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})
        finally:
                conn.close()

@app.route('/registrasi/verify',methods=['PUT'])
def verify_pendaftar():
        try:
                id_reg = request.args.get('id_reg')
                status_daftar = request.json['status_daftar']
                conn = postgre_conn()
                cursor = conn.cursor()
                query = "UPDATE pendaftar SET status_daftar='{}' WHERE id_reg = {}".format(status_daftar, id_reg)
                cursor.execute(query)
                conn.commit()
                return jsonify({"message": "Registry status successfully updated","status_code": 200})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})
        finally:
                conn.close()

@app.route('/registrasi',methods=['POST'])
def registrasi():
        try:
                id_user  = request.json['id_user']
                nama  = request.json['nama']
                ttl  = request.json['ttl']
                jenis_kel  = request.json['jenis_kel']
                agama  = request.json['agama']
                no_hp  = request.json['no_hp']
                alamat  = request.json['alamat']
                asal_sekolah  = request.json['asal_sekolah']
                jurusan_sekolah  = request.json['jurusan_sekolah']
                nisn  = request.json['nisn']
                prodi = request.json['prodi']
                status_daftar = request.json['status_daftar']
                nama_ayah = request.json['nama_ayah']
                status_ortu = request.json['status_ortu']
                pekerjaan = request.json['pekerjaan']
                penghasilan = request.json['penghasilan']
                no_hp_ortu = request.json['no_hp_ortu']
                nilai_ijazah = request.json['nilai_ijazah']
                nilai_transkip = request.json['nilai_transkip']
                foto = request.json['foto']
                conn = postgre_conn()
                cursor = conn.cursor()
                query = """
                        INSERT INTO pendaftar (id_user, nama, ttl, jenis_kel, agama, no_hp, alamat, asal_sekolah, jurusan_sekolah, nisn, 
                        prodi, status_daftar, nama_ayah, status_ortu, pekerjaan, penghasilan, no_hp_ortu, nilai_ijazah, nilai_transkip, foto) 
                        VALUES ({},'{}',TO_DATE('{}', 'DD-MM-YYYY'),'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                        """.format(id_user, nama, ttl, jenis_kel, agama, no_hp, alamat, asal_sekolah, jurusan_sekolah, nisn, prodi, 
                        status_daftar, nama_ayah, status_ortu, pekerjaan, penghasilan, no_hp_ortu, nilai_ijazah, nilai_transkip, foto)
                cursor.execute(query)
                conn.commit()
                return jsonify({"message": "Successfully registered","status_code": 200})

        except Exception as e:
                print(e)
                return jsonify({'message': 'Internal server error', 'status_code': 500})
        finally:
                conn.close()

if __name__ == '__main__':
  app.run(debug=True)

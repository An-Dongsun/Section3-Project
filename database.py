# 받아온 csv 파일을 읽고 Diabetes.db의 Diabetes테이블에 저장하는 파일이다.

# 필요한 라이브러리를 import 한다.
import sqlite3
import csv

# 당뇨병에 대한 데이터베이스가 없다면 데이터베이스를 만들고 접속해준다.
conn = sqlite3.connect('Diabetes.db')
# 커서를 만들어준다.
cur = conn.cursor()

# 테이블이 이미 존재하면 지워준다.
cur.execute("DROP TABLE IF EXISTS Diabetes;")

# Diabetes 테이블릉 만들어준다.
cur.execute("""CREATE TABLE Diabetes (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
				Diabetes_012 FLOAT,
                HighBP FLOAT,
                HighChol FLOAT,
                CholCheck FLOAT,
                BMI FLOAT,
                Smoker FLOAT,
                Stroke FLOAT,
                HeartDiseaseorAttack FLOAT,
                PhysActivity FLOAT,
                Fruits FLOAT,
                Veggies FLOAT,
                HvyAlcoholConsump FLOAT,
                AnyHealthcare FLOAT,
                NoDocbcCost FLOAT,
                GenHlth FLOAT,
                MentHlth FLOAT,
                PhysHlth FLOAT,
                DiffWalk FLOAT,
                Sex FLOAT,
                Age FLOAT,
                Education FLOAT,
                Income FLOAT
                );
			""")

# diabetes_2015.csv 파일을 읽어온다.
f = open("./diabetes_2015.csv", "r")
reader = csv.reader(f)

# 첫번째 행을 건너뛴다. (column name행이다.)
next(reader)

 # executemany를 이용해서 한번에 여러행을 데이터베이스에 입력해준다.
cur.executemany("""INSERT INTO Diabetes (Diabetes_012,
                                         HighBP,
                                         HighChol,
                                         CholCheck,
                                         BMI,
                                         Smoker,
                                         Stroke,
                                         HeartDiseaseorAttack,
                                         PhysActivity,
                                         Fruits,
                                         Veggies,
                                         HvyAlcoholConsump,
                                         AnyHealthcare,
                                         NoDocbcCost,
                                         GenHlth,
                                         MentHlth,
                                         PhysHlth,
                                         DiffWalk,
                                         Sex,
                                         Age,
                                         Education,
                                         Income) 
                                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);""",
                                         tuple(reader))

# 입력한 값들을 저장해준다.
conn.commit()
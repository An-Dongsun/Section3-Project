from flask import Flask, render_template, request, url_for

import pandas as pd
import pickle
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.impute import SimpleImputer
from lightgbm import LGBMClassifier
from sklearn.metrics import f1_score, log_loss

def create_app():
    app = Flask(__name__, static_url_path='/static')


    ## GET 방식으로 값을 전달받음. 
    ## num이라는 이름을 가진 integer variable를 넘겨받는다고 생각하면 됨. 
    ## 아무 값도 넘겨받지 않는 경우도 있으므로 비어 있는 url도 함께 mapping해주는 것이 필요함
    @app.route('/')
    def main_get(age=None):
        return render_template('resurch.html', age=age)

    @app.route('/calculate', methods=['POST', 'GET'])
    def calculate(age=None):
        ## 어떤 http method를 이용해서 전달받았는지를 아는 것이 필요함
        ## 아래에서 보는 바와 같이 어떤 방식으로 넘어왔느냐에 따라서 읽어들이는 방식이 달라짐
        if request.method == 'POST':
            #age = request.form['age']
            pass
        elif request.method == 'GET':
            ## 나이 정보를 받아온다. 
            age = request.args.get('age')
            age = float(age)
            if (age > 0) & (age < 25):
                age = 1
            elif (age >= 25) & (age < 30):
                age = 2
            elif (age >= 30) & (age < 35):
                age = 3
            elif (age >= 35) & (age < 40):
                age = 4
            elif (age >= 40) & (age < 45):
                age = 5
            elif (age >= 45) & (age < 50):
                age = 6
            elif (age >= 50) & (age < 55):
                age = 7
            elif (age >= 55) & (age < 60):
                age = 8
            elif (age >= 60) & (age < 65):
                age = 9
            elif (age >= 65) & (age < 70):
                age = 10
            elif (age >= 70) & (age < 75):
                age = 11
            elif (age >= 75) & (age < 80):
                age = 12
            else :
                age = 13
            # 나이 값을 데이터프레임에 집어 넣는다.
            x_test = pd.DataFrame({'age' : [age]})

            #성별을 받아서 x_test에 집어 넣는다.
            sex = request.args.get('sex')
            sex = int(sex)
            x_test['sex'] = sex

            # BMI수치를 받아서 x_test에 집어 넣는다.
            BMI = request.args.get('BMI')
            BMI = float(BMI)
            x_test['BMI'] = BMI

            # GenHlth를 받아서 x_test에 집어 넣는다.
            GenHlth = request.args.get('GenHlth')
            GenHlth = int(GenHlth)
            x_test['GenHlth'] = GenHlth

            # PhysHlth를 받아서 x_test에 집어 넣는다.
            PhysHlth = request.args.get('PhysHlth')
            PhysHlth = int(PhysHlth)
            x_test['PhysHlth'] = PhysHlth

            # MentHlth를 받아서 x_test에 집어 넣는다.
            MentHlth = request.args.get('MentHlth')
            MentHlth = int(MentHlth)
            x_test['MentHlth'] = MentHlth
            
            # PhysActivity를 받아서 x_test에 집어 넣는다.
            PhysActivity = request.args.get('PhysActivity')
            PhysActivity = int(PhysActivity)
            x_test['PhysActivity'] = PhysActivity
            
            # DiffWalk를 받아서 x_test에 집어 넣는다.
            DiffWalk = request.args.get('DiffWalk')
            DiffWalk = int(DiffWalk)
            x_test['DiffWalk'] = DiffWalk
            
            # Smoker를 받아서 x_test에 집어 넣는다.
            Smoker = request.args.get('Smoker')
            Smoker = int(Smoker)
            x_test['Smoker'] = Smoker
            
            # Fruits를 받아서 x_test에 집어 넣는다.
            Fruits = request.args.get('Fruits')
            Fruits = int(Fruits)
            x_test['Fruits'] = Fruits
            
            # Veggies를 받아서 x_test에 집어 넣는다.
            Veggies = request.args.get('Veggies')
            Veggies = int(Veggies)
            x_test['Veggies'] = Veggies
            
            # HighBP를 받아서 x_test에 집어 넣는다.
            HighBP = request.args.get('HighBP')
            HighBP = int(HighBP)
            x_test['HighBP'] = HighBP
            
            # HighChol를 받아서 x_test에 집어 넣는다.
            HighChol = request.args.get('HighChol')
            HighChol = int(HighChol)
            x_test['HighChol'] = HighChol
            
            # Stroke를 받아서 x_test에 집어 넣는다.
            Stroke = request.args.get('Stroke')
            Stroke = int(Stroke)
            x_test['Stroke'] = Stroke
            
            # HeartDiseaseorAttack를 받아서 x_test에 집어 넣는다.
            HeartDiseaseorAttack = request.args.get('HeartDiseaseorAttack')
            HeartDiseaseorAttack = int(HeartDiseaseorAttack)
            x_test['HeartDiseaseorAttack'] = HeartDiseaseorAttack

            # 머신러닝 모델 역피클링
            pipe_LGBM = None
            with open('model.pkl','rb') as pickle_file:
                pipe_LGBM = pickle.load(pickle_file)

            # x_test를 가지고 model에 넣어서 예측을 한다.
            result = pipe_LGBM.predict(x_test)[0]

            if result == 0.0 :
                text = '당뇨병이 아닙니다.'
            elif result == 1.0 :
                text = '당뇨병 전증 입니다.'
            else :
                text = '당뇨병 입니다.'

            ## 넘겨받은 값을 원래 페이지로 리다이렉트
            return render_template('resurch.html', text=text)
        ## else 로 하지 않은 것은 POST, GET 이외에 다른 method로 넘어왔을 때를 구분하기 위함
    return app

if __name__ == '__main__':
    # threaded=True 로 넘기면 multiple plot이 가능해짐
  app.run(debug=True, threaded=True)
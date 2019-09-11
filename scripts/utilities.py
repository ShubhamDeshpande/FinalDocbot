import math
import random
import re
import pandas as pd
def CalculateBMI(height,weight):
	bmi = round(weight/ (height * height), 1)
	if bmi <= 18.5:
		return 'Your BMI is '+str(bmi)+' which means you are underweight.'
	elif bmi > 18.5 and bmi < 25:
		return 'Your BMI is '+str(bmi)+' which means you are normal.'
	elif bmi > 25 and bmi < 30:
		return 'Your BMI is '+str(bmi)+' which means you are overweight.'
	elif bmi > 30:
		return 'Your BMI is '+str(bmi)+' which means you are obese. You should do some intensive workouts.'
	else:
		return 'There is an error with your input'

def GreetUser(name,greetings):
    greeting=random.choice(greetings)
    return re.sub('\w*__name__',name,greeting)

def CalculateBAI(height,hip_circum):
    bai=((hip_circum)/(height*math.sqrt(height)))-18
    return 'Your Body Adiposity Index :'+str(bai)+"."

def CalculateDetailedBAI(height,hip_circum,age,gender): 
	bai=((hip_circum)/(height*math.sqrt(height)))-18
	if gender=="male":
		df=pd.read_csv('/home/shubham/Desktop/Docbot/datasets/raw/bai_male',sep='\t')
	else:
		df=pd.read_csv('/home/shubham/Desktop/Docbot/datasets/raw/bai_female',sep='\t')
	df=df[(df.Age_f<=age)&(df.Age_t>=age)]
	if (df['Underweight_f']<=bai).values[0] and (df['Underweight_t']>=bai).values[0]:
		return 'Your Body Adiposity Index :'+str(bai)+'. You are underweight.'
	if (df['Healthy_f']<=bai).values[0] and (df['Healthy_t']>=bai).values[0]:
		return 'Your Body Adiposity Index :'+str(bai)+'. You are fit.'
	if (df['Overweight_f']<=bai).values[0] and (df['Overweight_t']>=bai).values[0]:
		return 'Your Body Adiposity Index :'+str(bai)+'. You are overweight.'
	if (df['Obese_f']<=bai).values[0] and (df['Obese_t']>=bai).values[0]:
		return 'Your Body Adiposity Index :'+str(bai)+'. You are obese.'

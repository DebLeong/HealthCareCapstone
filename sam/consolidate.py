import pandas as pd 
import numpy as np 
from datetime import datetime


def consolidate():

	#################################################################################
	# Read in Data
	bene_train = pd.read_csv('./data/Train_Beneficiary.csv')
	inpat_train = pd.read_csv('./data/Train_Inpatient.csv')
	outpat_train = pd.read_csv('./data/Train_Outpatient.csv')
	target_train = pd.read_csv('./data/Train.csv')


	bene_test = pd.read_csv('./data/Test_Beneficiary.csv')
	inpat_test = pd.read_csv('./data/Test_Inpatient.csv')
	outpat_test = pd.read_csv('./data/Test_Outpatient.csv')
	target_test = pd.read_csv('./data/Test.csv')

	#################################################################################
	# Add flags for identifying train or test data
	bene_train['Set'] = 'Train'
	inpat_train['Set'] = 'Train'
	outpat_train['Set'] = 'Train'
	target_train['Set'] = 'Train'

	bene_test['Set'] = 'Test'
	inpat_test['Set'] = 'Test'
	outpat_test['Set'] = 'Test'
	target_test['Set'] = 'Test'

	#################################################################################
	# Add flags for identifying train or test dat

	bene = pd.concat([bene_train,bene_test]).reset_index(drop=True)
	inpat = pd.concat([inpat_train,inpat_test]).reset_index(drop=True)
	outpat = pd.concat([outpat_train,outpat_test]).reset_index(drop=True)
	target = pd.concat([target_train,target_test]).reset_index(drop=True)

	# Add '?' for missing target test data
	target.fillna('?',inplace=True)


	#################################################################################
	# Clean Beneficiary Data
	bene = bene_eng(bene)
	

	#################################################################################
	# Add Flags for inpatient and outpatient data
	inpat['Status'] = 'in'
	outpat['Status'] = 'out'

	#################################################################################
	# Merge inpatient and outpatient
	mediCare = pd.merge(inpat, outpat, 
		left_on = [ x for x in outpat.columns if x in inpat.columns], 
		right_on = [ x for x in outpat.columns if x in inpat.columns], 
		how = 'outer')

	#################################################################################
	# Clean medicare and beneficiary data
	data = pd.merge(mediCare, bene,
		left_on=['BeneID','Set'],
		right_on=['BeneID','Set'], 
		how='inner')

	data = data_eng(data)


	#################################################################################
	# Create fake names for doctor IDs (Optional)

	#data = make_fake_names(data, columns = ['AttendingPhysician','OperatingPhysician','OtherPhysician'])

	#################################################################################
	# Merge features and target data (Optional)

	#data_complete = data.merge(target, on=['Provider','Set'], how='left')
	#data_complete.to_csv('./data/completeData.csv')

	#################################################################################
	# Write to CSV

	data.to_csv('./data/combinedData.csv')
	target.to_csv('./data/combinedTarget.csv')



def bene_eng(bene):
	#################################################################################
	# Clean Beneficiary Data
	bene = bene.replace({'ChronicCond_Alzheimer': 2, 'ChronicCond_Heartfailure': 2, 'ChronicCond_KidneyDisease': 2,
                           'ChronicCond_Cancer': 2, 'ChronicCond_ObstrPulmonary': 2, 'ChronicCond_Depression': 2, 
                           'ChronicCond_Diabetes': 2, 'ChronicCond_IschemicHeart': 2, 'ChronicCond_Osteoporasis': 2, 
                           'ChronicCond_rheumatoidarthritis': 2, 'ChronicCond_stroke': 2, 'Gender': 2 }, 0)
	bene = bene.replace({'RenalDiseaseIndicator': 'Y'}, 1).astype({'RenalDiseaseIndicator': 'int64'})

	#################################################################################
	# Rename chronic conditions
	bene.rename(columns = {"ChronicCond_Alzheimer":"Alzheimer",
             "ChronicCond_Heartfailure":"HeartFailure",
             "ChronicCond_KidneyDisease":"KidneyDisease",
             "ChronicCond_Diabetes":"Diabetes",
             "ChronicCond_IschemicHeart":"IschemicHeart",
             "ChronicCond_Osteoporasis":"Osteoporasis",
             "ChronicCond_rheumatoidarthritis":"RheumatoidArthritis",
             "ChronicCond_stroke":"Stroke",
             "ChronicCond_Cancer":"Cancer",
             "ChronicCond_ObstrPulmonary":"ObstrPulmonary",
             "ChronicCond_Depression":"Depression"}, inplace=True)



	#################################################################################
	# Feature Engineering: Check if beneficiary is dead or not at time of claim

	bene['WhetherDead']= 0
	bene.loc[bene.DOD.notna(),'WhetherDead'] = 1

	#################################################################################
	# Feature Engineering: Count number of chronic conditions of the beneficiary

	chronicConds = bene[['Alzheimer', 'HeartFailure', 'KidneyDisease',\
	'Cancer', 'ObstrPulmonary', 'Depression', 'Diabetes', 'IschemicHeart',\
	'Osteoporasis', 'RheumatoidArthritis', 'Stroke']]

	bene['NumChronics'] = chronicConds.sum(axis = 1)

	return bene

def data_eng(data):

	
	#################################################################################
	# Feature Engineering: Count number of procedures listed on claim


	ClmProcedure_vars = ['ClmProcedureCode_{}'.format(x) for x in range(1,7)]
	data['NumProc'] = data[ClmProcedure_vars].notnull().to_numpy().sum(axis = 1)

	
	#################################################################################
	# Feature Engineering: Count number of diagnoses listed on claim

	ClmDiagnosisCode_vars =['ClmAdmitDiagnosisCode'] + ['ClmDiagnosisCode_{}'.format(x) for x in range(1, 11)]
	data['NumDiag'] = data[ClmDiagnosisCode_vars].notnull().to_numpy().sum(axis = 1)



	#################################################################################
	# Feature Engineering: Datetime Features

	data['AdmissionDt'] = pd.to_datetime(data['AdmissionDt'] , format = '%Y-%m-%d')
	data['DischargeDt'] = pd.to_datetime(data['DischargeDt'],format = '%Y-%m-%d')

	data['ClaimStartDt'] = pd.to_datetime(data['ClaimStartDt'] , format = '%Y-%m-%d')
	data['ClaimEndDt'] = pd.to_datetime(data['ClaimEndDt'],format = '%Y-%m-%d')

	data['DOB'] = pd.to_datetime(data['DOB'] , format = '%Y-%m-%d')
	data['DOD'] = pd.to_datetime(data['DOD'],format = '%Y-%m-%d')

	### Number of hospitalization days
	data['AdmissionDays'] = ((data['DischargeDt'] - data['AdmissionDt']).dt.days) + 1
	### Number of claim days 
	data['ClaimDays'] = ((data['ClaimEndDt'] - data['ClaimStartDt']).dt.days) + 1

	data['Age'] = round(((data['ClaimStartDt'] - data['DOB']).dt.days + 1)/365.25)

	return data


def make_fake_names(data, columns = ['AttendingPhysician','OperatingPhysician','OtherPhysician']):
	from faker import Faker
	
	#################################################################################
	# Clean features

	data[columns] = data[columns].fillna('')
	data[columns] = data[columns].apply(lambda x: x.str.strip())

	#################################################################################
	# Clean features
	ids = np.unique(data[columns].values.flatten())

	#################################################################################
	# Create random names
	random.seed(1) # don't change - ensures reproducibility

	fake = Faker(['en_CA', 'de_DE', 'en_US','es_MX'])
	a = set()
	L=0

	while L < ids.shape[0]:
	    name = 'Dr. ' + fake.first_name() + ' ' + fake.last_name()
	    a.add(name)
	    L = len(a)
	    
	names = np.array(list(a))

	id_lookup = pd.DataFrame({'Names': names}, index = ids)

	id_lookup.loc[''][0] = ''

	for col in columns:
		data[col] = data[col].apply(lambda x: id_lookup.loc[x][0])

	id_lookup.to_csv('./data/doc_lookup.csv')

	return data


consolidate()

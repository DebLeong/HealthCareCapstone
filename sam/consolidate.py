import pandas as pd 
import numpy as np 
from datetime import datetime
import os

try:
    os.mkdir('./data')
except:
    pass

try:
    os.mkdir('./data/provData')
except:
    pass


state_dict = {
 1: 'Alabama',
 2: 'Alaska',
 3: 'Arizona',
 4: 'Arkansas',
 5: 'California',
 6: 'Colorado',
 7: 'Connecticut',
 8: 'Delaware',
 9: 'District of Columbia',
 10: 'Florida',
 11: 'Georgia',
 12: 'Hawaii',
 13: 'Idaho',
 14: 'Illinois',
 15: 'Indiana',
 16: 'Iowa',
 17: 'Kansas',
 18: 'Kentucky',
 19: 'Louisiana',
 20: 'Maine',
 21: 'Maryland',
 22: 'Massachusetts',
 23: 'Michigan',
 24: 'Minnesota',
 25: 'Mississippi',
 26: 'Missouri',
 27: 'Montana',
 28: 'Nebraska',
 29: 'Nevada',
 30: 'New Hampshire',
 31: 'New Jersey',
 32: 'New Mexico',
 33: 'New York',
 34: 'North Carolina',
 35: 'North Dakota',
 36: 'Ohio',
 37: 'Oklahoma',
 38: 'Oregon',
 39: 'Pennsylvania',
 41: 'Rhode Island',
 42: 'South Carolina',
 43: 'South Dakota',
 44: 'Tennessee',
 45: 'Texas',
 46: 'Utah',
 47: 'Vermont',
 49: 'Virginia',
 50: 'Washington',
 51: 'West Virginia',
 52: 'Wisconsin',
 53: 'Wyoming',
 54: 'Puerto Rico'}


def consolidate():
	'''
	Code to consolidate all the data and generate data for EDA and modeling
	'''

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

	provData(data,target)

	data.to_csv('./data/combinedData.csv')
	target.to_csv('./data/combinedTarget.csv')



def bene_eng(bene):
	'''
	Feature Engineering for the Beneficiary dataset
	'''
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
	bene['State'] = bene['State'].apply(lambda x: state_dict[x])

	return bene

def data_eng(data):
	'''
	Feature engineering for the data dataset
	'''

	
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

def provData(data, target):
	'''
	Creates aggregate provider dataframe
	'''

	def rangeFunc(feature):
		return max(feature) - min(feature)
	p = data.groupby(['Provider','Set']).agg({
		'Age': 'mean',
		'Gender' : 'mean', # proportion of claims involving males (Gender=1) (not unique to Beneificiaries)
		'BeneID':'nunique',
		'ClaimID' : 'count',
		'State' : 'nunique',
		'AttendingPhysician': 'nunique',
		'OperatingPhysician': 'nunique',
		'OtherPhysician': 'nunique',
		'NumProc': 'mean',
		'NumDiag' : 'mean',
		'NumChronics': 'mean',
		'InscClaimAmtReimbursed' : 'mean',
		'DeductibleAmtPaid' : 'mean',
		'ClaimDays' : 'mean',
		'AdmissionDays' : 'mean',
		'WhetherDead': 'mean', # proportion of dead patients (might need to take negative log to get anything large)
		'Alzheimer' : 'mean',
		'HeartFailure': 'mean', 
		'KidneyDisease' : 'mean',
		'Cancer': 'mean', 
		'ObstrPulmonary': 'mean',
		'Depression': 'mean', 
		'Diabetes': 'mean', 
		'IschemicHeart': 'mean', 
		'Osteoporasis': 'mean',
	    'RheumatoidArthritis': 'mean',
	     'Stroke': 'mean'
		}).reset_index()

	p['logClaim'] = np.log(p['ClaimID'])
	p['logBene'] = np.log(p['BeneID'])


	#####
	# Create ranges 
	p_range = data.groupby(['Provider','Set']).agg({
		'Age' : rangeFunc,
		'NumProc': rangeFunc,
		'NumDiag' : rangeFunc,
		'NumChronics': rangeFunc,
		'InscClaimAmtReimbursed' : rangeFunc,
		'ClaimDays' : rangeFunc
		}).reset_index()

	p_range.columns += '_Range'

	## No need to merge on Provider AND Set since Provider can only be in either Train or Test
	p = pd.merge(p,p_range, on = ['Provider'], how='left')

	#################################################################################
	# Number of Unique Inpatients and Outpatients
	d = data.groupby(['Provider','Status']).agg({
		'ClaimID': 'count',
		'BeneID' : 'nunique'}).reset_index().pivot_table(
		values=['ClaimID','BeneID'], 
		index = 'Provider', 
		columns='Status').fillna(0)

	d = d.reset_index()
	d.columns = d.columns.map(''.join)

	p = pd.merge(p,d, on = ['Provider'], how='left')

	#################################################################################
	# Number of Unique Doctors Associated With Provider
	docs = data.melt(
		id_vars = 'Provider', 
		value_vars = ['AttendingPhysician','OperatingPhysician','OtherPhysician'], 
		var_name='Type', 
		value_name='Doctor').dropna(axis=0)

	docs = docs[['Provider','Doctor']].drop_duplicates()

	p['Doctors'] = docs.groupby('Provider')['Doctor'].count().values

	p = pd.merge(p, target, on = ['Provider','Set'], how = 'left')

	######
	# Rename columns. Be careful if you add a feature make sure to put the new name in the right place!
	#provData.columns = ['Provider','Set', 'Patients','Claims','States','Doctors','Fraud']

	x_train = p[p.Set == 'Train'].drop(columns = ['Set'])
	x_train['PotentialFraud'] = (x_train['PotentialFraud'] == 'Yes') + 0 # Convert to binary
	x_test = p[p.Set == 'Test'].drop(columns = ['Set','PotentialFraud'])

	x_train.to_csv('./data/provData/x_train.csv')
	x_test.to_csv('./data/provData/x_test.csv')
	return

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

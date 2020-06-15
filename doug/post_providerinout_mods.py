# import pandas and numpy for operations
import pandas as pd
import numpy as np

# read in output file from provider_inout
x_train_inout = pd.read_csv('./data/provData/x_train_inout.csv')

# take out columns I won't use
x_train_inout = x_train_inout.drop(columns = ['Alzheimer_in','Alzheimer_out','Cancer_in',
        'Cancer_out', 'Depression_in', 'Depression_out', 'Diabetes_in', 'Diabetes_out','HeartFailure_in', 
        'HeartFailure_out','IschemicHeart_in', 'IschemicHeart_out','KidneyDisease_in','KidneyDisease_out',
        'ObstrPulmonary_in','ObstrPulmonary_out','Osteoporasis_in','Osteoporasis_out','RheumatoidArthritis_in',
        'RheumatoidArthritis_out','Stroke_in','Stroke_out','Unnamed: 0','Unnamed: 0.1'])

# calcualate claims per physician and per patient
x_train_inout['ClmsPerPhysician_in'] = x_train_inout['ClaimID_in']/x_train_inout['AttendingPhysician_in']
x_train_inout['ClmsPerPhysician_out'] = x_train_inout['ClaimID_out']/x_train_inout['AttendingPhysician_out']
x_train_inout['ClmsPerPatient_in'] = x_train_inout['ClaimID_in']/x_train_inout['BeneID_in']
x_train_inout['ClmsPerPatient_out'] = x_train_inout['ClaimID_out']/x_train_inout['BeneID_out']

# calculate ratio of attendings to patients
x_train_inout['DrPerPatient_in'] = x_train_inout['AttendingPhysician_in']/x_train_inout['BeneID_in']
x_train_inout['DrPerPatient_out'] = x_train_inout['AttendingPhysician_out']/x_train_inout['BeneID_out']

# use log patients instead of raw patient per provider to reduce leverage
x_train_inout['LogPatients_in']=np.log(x_train_inout['BeneID_in']+0.1)
x_train_inout['LogPatients_out']=np.log(x_train_inout['BeneID_out']+0.1)
x_train_inout = x_train_inout.drop(columns=['BeneID_in','BeneID_out'])

# same with number of claims per provider, to reduce leverage of high claim counts
x_train_inout['LogClaims_in']=np.log(x_train_inout['ClaimID_in']+0.1)
x_train_inout['LogClaims_out']=np.log(x_train_inout['ClaimID_out']+0.1)
x_train_inout = x_train_inout.drop(columns=['ClaimID_in','ClaimID_out'])

# same idea with operating and other physicians, to reduce leverage
x_train_inout['LogOpPhys_in']=np.log(x_train_inout['OperatingPhysician_in']+0.1)
x_train_inout['LogOpPhys_out']=np.log(x_train_inout['OperatingPhysician_out']+0.1)
x_train_inout = x_train_inout.drop(columns=['OperatingPhysician_in','OperatingPhysician_out'])
x_train_inout['LogOtherPhys_in']=np.log(x_train_inout['OtherPhysician_in']+0.1)
x_train_inout['LogOtherPhys_out']=np.log(x_train_inout['OtherPhysician_out']+0.1)
x_train_inout = x_train_inout.drop(columns=['OtherPhysician_in','OtherPhysician_out'])

# need to read in original files to get age ranges
in_patient_train = pd.read_csv('./data/Train_Inpatient.csv')
out_patient_train = pd.read_csv('./data/Train_Outpatient.csv')
inpt_provider = pd.DataFrame(in_patient_train['Provider'].unique())
inpt_provider.columns = ['Provider']
outpt_provider = pd.DataFrame(out_patient_train['Provider'].unique())
outpt_provider.columns = ['Provider']
in_patient_train['ClaimStartDt'] = pd.to_datetime(in_patient_train['ClaimStartDt'] , format = '%Y-%m-%d')
out_patient_train['ClaimStartDt'] = pd.to_datetime(out_patient_train['ClaimStartDt'] , format = '%Y-%m-%d')

# read in beneficiary information to get beneficiary age at service, and ranges
bene_train = pd.read_csv('./data/Train_Beneficiary.csv')
in_patient_train = pd.merge(in_patient_train, bene_train, on = 'BeneID')
out_patient_train = pd.merge(out_patient_train, bene_train, on = 'BeneID')
in_patient_train['DOB'] = pd.to_datetime(in_patient_train['DOB'] , format = '%Y-%m-%d')
out_patient_train['DOB'] = pd.to_datetime(out_patient_train['DOB'] , format = '%Y-%m-%d')
in_patient_train['Age'] = round(((in_patient_train['ClaimStartDt'] - in_patient_train['DOB']).dt.days + 1)/365.25)
out_patient_train['Age'] = round(((out_patient_train['ClaimStartDt'] - out_patient_train['DOB']).dt.days + 1)/365.25)
a = in_patient_train.groupby('Provider')['Age'].max()-in_patient_train.groupby('Provider')['Age'].min()
a = pd.DataFrame(a.index,a)
a = a.reset_index()
a.columns = ['AgeRange','Provider']
inpt_provider = pd.merge(inpt_provider, a, on = 'Provider')
a = out_patient_train.groupby('Provider')['Age'].max()-out_patient_train.groupby('Provider')['Age'].min()
a = pd.DataFrame(a.index,a)
a = a.reset_index()
a.columns = ['AgeRange','Provider']
outpt_provider = pd.merge(outpt_provider, a, on = 'Provider')

# making the fraction of each specialty for each provider.  for in_patient it's about 5-10 min
diag_codes = ['ClmDiagnosisCode_1', 'ClmDiagnosisCode_2', 'ClmDiagnosisCode_3',
       'ClmDiagnosisCode_4', 'ClmDiagnosisCode_5', 'ClmDiagnosisCode_6',
       'ClmDiagnosisCode_7', 'ClmDiagnosisCode_8', 'ClmDiagnosisCode_9',
       'ClmDiagnosisCode_10']

specialty_dict = {'cardiology':'sum','urology':'sum','endocrinology':'sum',
    'emergency':'sum','general':'sum','infectious':'sum','oncology':'sum',
    'hematology':'sum','psychiatry':'sum','neurology':'sum','pulmonology':'sum',
    'gastroenterology':'sum','ob-gyn':'sum','dermatology':'sum','orthopedics':'sum',
    'congenital':'sum','neonatology':'sum'}

for spec in specialty_dict.keys():
    in_patient_train[spec]=[0]*in_patient_train.shape[0]

for diag in diag_codes:
    for idx in in_patient_train.index:
        clm = in_patient_train.loc[idx,diag]
        if type(clm)==str:
        #     look for letters which signify emergency/injury or other unspecific
            if (clm[0]=='E'):
                in_patient_train.loc[idx,'emergency']=in_patient_train.loc[idx,'emergency']+1
                clm=clm[1:]
            elif (clm[0]=='V'):
                in_patient_train.loc[idx,'general']=in_patient_train.loc[idx,'general']+1
                clm=clm[1:]
        #     if the code is 5 digits, truncate to 4
            elif len(clm)==5:
                clm = clm[:4]
        #     start bucketing by code number
            if int(clm)<1400:
                in_patient_train.loc[idx,'infectious']=in_patient_train.loc[idx,'infectious']+1
            elif (int(clm)>1400 and int(clm)<2400):
                in_patient_train.loc[idx,'oncology']=in_patient_train.loc[idx,'oncology']+1
            elif (int(clm)>2400 and int(clm)<2800):
                in_patient_train.loc[idx,'endocrinology']=in_patient_train.loc[idx,'endocrinology']+1
            elif (int(clm)>2800 and int(clm)<2900):
                in_patient_train.loc[idx,'hematology']=in_patient_train.loc[idx,'hematology']+1
            elif (int(clm)>2900 and int(clm)<3200):
                in_patient_train.loc[idx,'psychiatry']=in_patient_train.loc[idx,'psychiatry']+1
            elif (int(clm)>3200 and int(clm)<3900):
                in_patient_train.loc[idx,'neurology']=in_patient_train.loc[idx,'neurology']+1
            elif (int(clm)>3900 and int(clm)<4600):
                in_patient_train.loc[idx,'cardiology']=in_patient_train.loc[idx,'cardiology']+1
            elif (int(clm)>4600 and int(clm)<5200):
                in_patient_train.loc[idx,'pulmonology']=in_patient_train.loc[idx,'pulmonology']+1
            elif (int(clm)>5200 and int(clm)<5800):
                in_patient_train.loc[idx,'gastroenterology']=in_patient_train.loc[idx,'gastroenterology']+1
            elif (int(clm)>5800 and int(clm)<6300):
                in_patient_train.loc[idx,'urology']=in_patient_train.loc[idx,'urology']+1
            elif (int(clm)>6300 and int(clm)<6800):
                in_patient_train.loc[idx,'ob-gyn']=in_patient_train.loc[idx,'ob-gyn']+1
            elif (int(clm)>6800 and int(clm)<7100):
                in_patient_train.loc[idx,'dermatology']=in_patient_train.loc[idx,'dermatology']+1
            elif (int(clm)>7100 and int(clm)<7400):
                in_patient_train.loc[idx,'orthopedics']=in_patient_train.loc[idx,'orthopedics']+1
            elif (int(clm)>7400 and int(clm)<7600):
                in_patient_train.loc[idx,'congenital']=in_patient_train.loc[idx,'congenital']+1
            elif (int(clm)>7600 and int(clm)<7800):
                in_patient_train.loc[idx,'neonatology']=in_patient_train.loc[idx,'neonatology']+1
            elif (int(clm)>7800 and int(clm)<8000):
                in_patient_train.loc[idx,'general']=in_patient_train.loc[idx,'general']+1
            elif (int(clm)>8000 and int(clm)<9999):
                in_patient_train.loc[idx,'emergency']=in_patient_train.loc[idx,'emergency']+1
            else:
                pass
        else:
            pass

# I had thought this way would be faster as it is a list comprehension and not a for loop; no dice
# specialty_code_dict = {'cardiology':[4600,5200],'urology':[5800,6300],'endocrinology':[2800,2900],
#     'emergency':[8000,9999],'general':[7800,8000],'infectious':[0,2400],'oncology':[2400,2800],
#     'hematology':[2900,3200],'psychiatry':[3200,3900],'neurology':[3900,4600],'pulmonology':[4600,5200],
#     'gastroenterology':[5200,5800],'ob-gyn':[6300,6800],'dermatology':[6800,7100],'orthopedics':[7100,7400],
#     'congenital':[7400,7600],'neonatology':[7600,7800]}
# for spec in specialty_code_dict.keys():
#     if spec=='general':
#         in_patient_train[spec]=[np.count_nonzero([0 if type(clm)!=str else 0 if ((clm[0]=='E')) else 1 if (clm[0]=='V')\
#             else 0 if ((int(clm[:4])<specialty_code_dict[spec][0] or int(clm[:4])>specialty_code_dict[spec][1])) \
#             else 1 for clm in in_patient_train.loc[idx,diag_codes]]) for idx in in_patient_train.index]
#     elif spec=='emergency':
#         in_patient_train[spec]=[np.count_nonzero([0 if type(clm)!=str else 0 if ((clm[0]=='V')) else 1 if (clm[0]=='E')\
#             else 0 if ((int(clm[:4])<specialty_code_dict[spec][0] or int(clm[:4])>specialty_code_dict[spec][1])) \
#             else 1 for clm in in_patient_train.loc[idx,diag_codes]]) for idx in in_patient_train.index]
#     else:
#         in_patient_train[spec]=[np.count_nonzero([0 if type(clm)!=str else 0 if ((clm[0]=='V') or (clm[0]=='E')) \
#             else 0 if ((int(clm[:4])<specialty_code_dict[spec][0] or int(clm[:4])>specialty_code_dict[spec][1])) \
#             else 1 for clm in in_patient_train.loc[idx,diag_codes]]) for idx in in_patient_train.index]

# groupby to get counts of codes in each specialty
a = in_patient_train.groupby('Provider').agg(specialty_dict)

inpt_provider = pd.merge(inpt_provider, a, on = 'Provider')
# found I needed to create a separate column to be able to calculate fractions
v = list(specialty_dict.keys())
inpt_provider['dcodesum'] = np.sum(inpt_provider[v], axis=1)
# convert counts to fractions
for spec in specialty_dict.keys():
    inpt_provider[spec] = inpt_provider[spec]/inpt_provider['dcodesum']
# drop column as it isn't needed anymore
inpt_provider = inpt_provider.drop(columns = ['dcodesum'])
# write out to file, just to make sure we don't lose it
inpt_provider.to_csv('inpatnt_provider_attributes.csv')

# this is for out-patient and it is brutally slow, about 75 minutes
for spec in specialty_dict.keys():
    out_patient_train[spec]=[0]*out_patient_train.shape[0]

for spec in specialty_dict.keys():
    out_patient_train[spec]=[0]*out_patient_train.shape[0]
for diag in diag_codes:
    for idx in out_patient_train.index:
        clm = out_patient_train.loc[idx,diag]
        if type(clm)==str:
        #     look for letters which signify emergency/injury or other unspecific
            if (clm[0]=='E'):
                out_patient_train.loc[idx,'emergency']=out_patient_train.loc[idx,'emergency']+1
                clm=clm[1:]
            elif (clm[0]=='V'):
                out_patient_train.loc[idx,'general']=out_patient_train.loc[idx,'general']+1
                clm=clm[1:]
        #     if the code is 5 digits, truncate to 4
            elif len(clm)==5:
                clm = clm[:4]
        #     start bucketing by code number and assign to summation column
            if int(clm)<1400:
                out_patient_train.loc[idx,'infectious']=out_patient_train.loc[idx,'infectious']+1
            elif (int(clm)>1400 and int(clm)<2400):
                out_patient_train.loc[idx,'oncology']=out_patient_train.loc[idx,'oncology']+1
            elif (int(clm)>2400 and int(clm)<2800):
                out_patient_train.loc[idx,'endocrinology']=out_patient_train.loc[idx,'endocrinology']+1
            elif (int(clm)>2800 and int(clm)<2900):
                out_patient_train.loc[idx,'hematology']=out_patient_train.loc[idx,'hematology']+1
            elif (int(clm)>2900 and int(clm)<3200):
                out_patient_train.loc[idx,'psychiatry']=out_patient_train.loc[idx,'psychiatry']+1
            elif (int(clm)>3200 and int(clm)<3900):
                out_patient_train.loc[idx,'neurology']=out_patient_train.loc[idx,'neurology']+1
            elif (int(clm)>3900 and int(clm)<4600):
                out_patient_train.loc[idx,'cardiology']=out_patient_train.loc[idx,'cardiology']+1
            elif (int(clm)>4600 and int(clm)<5200):
                out_patient_train.loc[idx,'pulmonology']=out_patient_train.loc[idx,'pulmonology']+1
            elif (int(clm)>5200 and int(clm)<5800):
                out_patient_train.loc[idx,'gastroenterology']=out_patient_train.loc[idx,'gastroenterology']+1
            elif (int(clm)>5800 and int(clm)<6300):
                out_patient_train.loc[idx,'urology']=out_patient_train.loc[idx,'urology']+1
            elif (int(clm)>6300 and int(clm)<6800):
                out_patient_train.loc[idx,'ob-gyn']=out_patient_train.loc[idx,'ob-gyn']+1
            elif (int(clm)>6800 and int(clm)<7100):
                out_patient_train.loc[idx,'dermatology']=out_patient_train.loc[idx,'dermatology']+1
            elif (int(clm)>7100 and int(clm)<7400):
                out_patient_train.loc[idx,'orthopedics']=out_patient_train.loc[idx,'orthopedics']+1
            elif (int(clm)>7400 and int(clm)<7600):
                out_patient_train.loc[idx,'congenital']=out_patient_train.loc[idx,'congenital']+1
            elif (int(clm)>7600 and int(clm)<7800):
                out_patient_train.loc[idx,'neonatology']=out_patient_train.loc[idx,'neonatology']+1
            elif (int(clm)>7800 and int(clm)<8000):
                out_patient_train.loc[idx,'general']=out_patient_train.loc[idx,'general']+1
            elif (int(clm)>8000 and int(clm)<9999):
                out_patient_train.loc[idx,'emergency']=out_patient_train.loc[idx,'emergency']+1
            else:
                pass
        else:
            pass

# again, I had thought this would be faster, but no dice
# for spec in specialty_code_dict.keys():
#     if spec=='general':
#         out_patient_train[spec]=[np.count_nonzero([0 if type(clm)!=str else 0 if ((clm[0]=='E')) else 1 if (clm[0]=='V')\
#             else 0 if ((int(clm[:4])<specialty_code_dict[spec][0] or int(clm[:4])>specialty_code_dict[spec][1])) \
#             else 1 for clm in out_patient_train.loc[idx,diag_codes]]) for idx in out_patient_train.index]
#     elif spec=='emergency':
#         out_patient_train[spec]=[np.count_nonzero([0 if type(clm)!=str else 0 if ((clm[0]=='V')) else 1 if (clm[0]=='E')\
#             else 0 if ((int(clm[:4])<specialty_code_dict[spec][0] or int(clm[:4])>specialty_code_dict[spec][1])) \
#             else 1 for clm in out_patient_train.loc[idx,diag_codes]]) for idx in out_patient_train.index]
#     else:
#         out_patient_train[spec]=[np.count_nonzero([0 if type(clm)!=str else 0 if ((clm[0]=='V') or (clm[0]=='E')) \
#             else 0 if ((int(clm[:4])<specialty_code_dict[spec][0] or int(clm[:4])>specialty_code_dict[spec][1])) \
#             else 1 for clm in out_patient_train.loc[idx,diag_codes]]) for idx in out_patient_train.index]

# same deal as with inpatient above
b = out_patient_train.groupby('Provider').agg(specialty_dict)
outpt_provider = pd.merge(outpt_provider, b, on = 'Provider')

outpt_provider['dcodesum'] = np.sum(outpt_provider[v], axis=1)

for spec in specialty_dict.keys():
    outpt_provider[spec] = outpt_provider[spec]/outpt_provider['dcodesum']

outpt_provider = outpt_provider.drop(columns = ['dcodesum'])
outpt_provider.to_csv('outpt_provider_attributes.csv')

# rename columns of groupbys we just created
inpt_col_dict = {x:(x+'_inpt') for x in inpt_provider.columns[1:]}
inpt_provider = inpt_provider.rename(inpt_col_dict, axis=1)
outpt_col_dict = {x:(x+'_otpt') for x in outpt_provider.columns[1:]}
outpt_provider = outpt_provider.rename(outpt_col_dict, axis=1)

# merge inpt and outpt into single df
provider_attributes = pd.merge(outpt_provider, inpt_provider, how='outer', on = 'Provider')

# merge into provider_inout df
x_train_inout_mod = pd.merge(x_train_inout,provider_attributes, on = 'Provider')

# write out to file for analysis next steps
x_train_inout_mod.to_csv('x_train_inout_mod.csv')
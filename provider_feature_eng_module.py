def num_providers(in_patient_train):
    '''
    count number of unique providers in training dataset
    returns a new dataframe with providers as the key
    '''
    inpt_provider = pd.DataFrame(in_patient_train['Provider'].unique())
    inpt_provider.columns = ['Provider']
    inpt_provider = pd.merge(inpt_provider,train_label, on = 'Provider')
    return inpt_provider

def count_attndng(in_patient_train, inpt_provider):
    '''
    input is training dataset and provider attribute dataset
    returns provider attribute dataframe with number of unique attending physicians for each provider
    '''
    a = in_patient_train[['Provider','AttendingPhysician']].groupby('Provider').nunique()
    b = pd.DataFrame(a.index,a['AttendingPhysician'])
    b = b.reset_index()
    inpt_provider = pd.merge(inpt_provider, b, on = 'Provider')
    inpt_provider['logattnd'] = np.log(inpt_provider['AttendingPhysician']+1)
    return inpt_provider

def count_patients(in_patient_train, inpt_provider):
    '''
    input is training dataset and provider attribute dataset
    returns provider attribute dataframe with number of unique patients per provider
    '''
    c = in_patient_train[['Provider','BeneID']].groupby('Provider').nunique()
    d = pd.DataFrame(c.index,c['BeneID'])
    d = d.reset_index()
    inpt_provider = pd.merge(inpt_provider, d, on = 'Provider')
    inpt_provider['logpts'] = np.log(inpt_provider['BeneID']+1)
    return inpt_provider

def mean_codes(in_patient_train, inpt_provider):
    '''
    input is training dataset and provider attribute dataset. Run this after calculating the 
    number of diagnostic and procedural codes per claim in 'consolidate' on training dataset
    returns provider attribute dataframe with mean number of diag and proc codes on provider's clms
    '''
    e = in_patient_train.groupby('Provider').agg('mean')['NumDiagCodes']
    f = pd.DataFrame(e.index,e)
    f = f.reset_index()
    f.columns = ['meanDiagCodes','Provider']
    inpt_provider = pd.merge(inpt_provider, f, on = 'Provider')
    g = in_patient_train.groupby('Provider').agg('mean')['NumProcCodes']
    h = pd.DataFrame(g.index,g)
    h = h.reset_index()
    h.columns = ['meanProcCodes','Provider']
    inpt_provider = pd.merge(inpt_provider, h, on = 'Provider')
    return inpt_provider

def range_codes(in_patient_train, inpt_provider):
    '''
    input is training dataset and provider attribute dataset. Run this after calculating the 
    number of diagnostic and procedural codes per claim in 'consolidate' on training dataset
    returns provider attribute dataframe with min-max range of diag and proc codes on provider's clms
    '''
    e = in_patient_train.groupby('Provider')['NumDiagCodes'].max() - in_patient_train.groupby('Provider')['NumDiagCodes'].min()
    f = pd.DataFrame(e.index,e)
    f = f.reset_index()
    f.columns = ['DiagcodesRange','Provider']
    inpt_provider = pd.merge(inpt_provider, f, on = 'Provider')
    e = out_patient_train.groupby('Provider')['NumDiagCodes'].max() - out_patient_train.groupby('Provider')['NumDiagCodes'].min()
    f = pd.DataFrame(e.index,e)
    f = f.reset_index()
    f.columns = ['DiagcodesRange','Provider']
    outpt_provider = pd.merge(outpt_provider, f, on = 'Provider')
    return inpt_provider

def reimbursement(in_patient_train, inpt_provider):
    '''
    input is training dataset and provider attribute dataset. 
    returns provider attribute dataframe with mean reimbursement and range of reimbursement
    '''
    m = in_patient_train.groupby('Provider').agg('mean')['InscClaimAmtReimbursed']
    n = pd.DataFrame(m.index,m)
    n = n.reset_index()
    n.columns = ['MeanReimburse','Provider']
    inpt_provider = pd.merge(inpt_provider, n, on = 'Provider')
    m = in_patient_train.groupby('Provider')['InscClaimAmtReimbursed'].max() - in_patient_train.groupby('Provider')['InscClaimAmtReimbursed'].min()
    n = pd.DataFrame(m.index,m)
    n = n.reset_index()
    n.columns = ['ReimburseRange','Provider']
    inpt_provider = pd.merge(inpt_provider, n, on = 'Provider')
    return inpt_provider

def claim_count(in_patient_train, inpt_provider):
    '''
    input is training dataset and provider attribute dataset. 
    returns provider attribute dataframe total claims/provider, and count per physician and pt
    '''
    m = in_patient_train.groupby('Provider')['ClaimID'].count()
    n = pd.DataFrame(m.index,m)
    n = n.reset_index()
    n.columns = ['ClaimCount','Provider']
    inpt_provider = pd.merge(inpt_provider, n, on = 'Provider')
    inpt_provider['logClmCount'] = np.log(inpt_provider['ClaimCount']+1)
    inpt_provider['LogClmsPerPhysician'] = np.log(inpt_provider['ClaimCount']/(inpt_provider['AttendingPhysician']+0.01)+0.1)
    inpt_provider['LogClmsPerPatnt'] = np.log(inpt_provider['ClaimCount']/(inpt_provider['BeneID']+0.01)+0.1)
    return inpt_provider

def claim_date_ranges(in_patient_train, inpt_provider):
    '''
    input is training dataset and provider attribute dataset. Run this after calculating claim dates
    returns provider attribute dataframe with mean and range of range of claim days
    '''
    aa = in_patient_train.groupby('Provider')['ClaimDays'].max() - in_patient_train.groupby('Provider')['ClaimDays'].min()
    ab = pd.DataFrame(aa.index,aa)
    ab = ab.reset_index()
    ab.columns = ['ClmDurationRange','Provider']
    inpt_provider = pd.merge(inpt_provider, ab, on = 'Provider')
    return inpt_provider

def age_range(in_patient_train, inpt_provider):
    '''
    input is training dataset and provider attribute dataset. Run this after calculating ages of
    patients and converting claim date strings to datezs
    returns provider attribute dataframe with range of ages at provider
    '''
    a = in_patient_train.groupby('Provider')['Age'].max()-in_patient_train.groupby('Provider')['Age'].min()
    a = pd.DataFrame(a.index,a)
    a = a.reset_index()
    a.columns = ['AgeRange','Provider']
    inpt_provider = pd.merge(inpt_provider, a, on = 'Provider')
    return inpt_provider

def num_chronics(in_patient_train, inpt_provider):
    '''
    input is training dataset and provider attribute dataset. Run this after calculating ages of
    patients and converting claim date strings to datezs
    returns provider attribute dataframe mean chronics/patient and max/min range of num of chronics
    '''
    e = in_patient_train.groupby('Provider').agg('mean')['NumChronics']
    f = pd.DataFrame(e.index,e)
    f = f.reset_index()
    f.columns = ['AveNumChronicPerPt','Provider']
    inpt_provider = pd.merge(inpt_provider, f, on = 'Provider')
    a = in_patient_train.groupby('Provider')['NumChronics'].max()-in_patient_train.groupby('Provider')['NumChronics'].min()
    a = pd.DataFrame(a.index,a)
    a = a.reset_index()
    a.columns = ['NumChronicsRange','Provider']
    inpt_provider = pd.merge(inpt_provider, a, on = 'Provider')
    return inpt_provider

def specialties(in_patient_train, inpt_provider):
    '''
    input is training dataset and provider attribute dataset. calculates number of codes and
    buckets them per specialty in ICD
    returns provider attribute dataframe with proportions of each specialty for each provider
    '''
    diag_codes = ['ClmDiagnosisCode_1', 'ClmDiagnosisCode_2', 'ClmDiagnosisCode_3',\
       'ClmDiagnosisCode_4', 'ClmDiagnosisCode_5', 'ClmDiagnosisCode_6',\
       'ClmDiagnosisCode_7', 'ClmDiagnosisCode_8', 'ClmDiagnosisCode_9',\
       'ClmDiagnosisCode_10']
    specialty_dict = {'cardiology':'sum','urology':'sum','endocrinology':'sum',\
        'emergency':'sum','general':'sum','infectious':'sum','oncology':'sum',\
        'hematology':'sum','psychiatry':'sum','neurology':'sum','pulmonology':'sum',\
        'gastroenterology':'sum','ob-gyn':'sum','dermatology':'sum','orthopedics':'sum',\
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
    a = in_patient_train.groupby('Provider').agg(specialty_dict)
    inpt_provider = pd.merge(inpt_provider, a, on = 'Provider')
    v = list(specialty_dict.keys())
    inpt_provider['dcodesum'] = np.sum(inpt_provider[v], axis=1)
    for spec in specialty_dict.keys():
        inpt_provider[spec] = inpt_provider[spec]/inpt_provider['dcodesum']
    return inpt_provider

def gendersum(grp):
    '''
    used in gender prop function
    '''
    return np.sum(grp==0)

def gender_prop(in_patient_train, inpt_provider):
    '''
    input is training dataset and provider attribute dataset. proportion of gender 0 for providers
    returns provider attribute dataframe with proportions of each specialty for each provider
    '''
    c = in_patient_train.groupby('Provider').agg({'Gender':[gendersum, 'count']})
    c.columns = ['Num0','Total']
    c['Pct0gend'] = c['Num0']/c['Total']
    c = pd.DataFrame(c['Pct0gend']).reset_index()
    inpt_provider = pd.merge(inpt_provider, c, on = 'Provider')
    return inpt_provider

Medical Detectives: Team Notes
===

###### tags: `Mentor` `MedicalFraud`


:dart: MD Goal
---

- Identify Fraud within a medical network
    - Raise F1 Score on Fraudulent Providers to 0.70 for Logistic Model
        - ==0.62 achieved with LASSO feature selection and CV==
    - Raise F1 Score on Fraudulent Providers to 0.75 for Random Forest
        - ==0.64 achieved==
- Target Large Providers
- Decompose Fraud classification down to the doctor and beneficiary level
- Provide investigative tool for insurance companies
    - ==R Shiny App V.1 Completed==
___

:books: MD Backlog (stuff we haven't started on)
---
- Presentation Draft
- MBA Analysis
- More types of Models and Combinations
    - PCA -> Logistiic
    - Clustering -> SVM
    - Neural Network

:books: Meeting Notes
---

Daily Meeting
---
### Doug:
#### - DecisionTrees
    - false neg rate in RF is lower than LogReg, but false pos is higher
    - considering adding in features from LogReg
    - 90% of frauds caught by RF
    - Using RFECV
    - More False Positives from changing diagnostic code mapping
    - Wrote own min-max scaling since sklearn version not working
#### - GradientBoost
    - Worse performance than Random Forest
    - Experimenting on best weighting for positives

### Sam:
#### - R Shiny App
    - Slow for large networks 
        - for really large ones it crashes
    - want to incorporate SQL calls to offload computation
#### - Feature Engineering
    - creation of fraud specific link features from network data
    - creation of size binary feature
    - creation of county density feature
#### - Network Modeling
    - Exploring Nearest Neighbor Prediction models - "Guilt by Association"
    

### Deborah:
#### - SQL
#### - MBA


Luke Meeting
---


- Visualizations
    - Networks
        - Cluster Analysis of Networks
    - Aggregate Graphs
- Modeling
    - Tree Based Models
    - Interaction Terms in Lasso LogReg or step wise AIC/BIC selection. 
        - Dummified inpat/outpat with patient attributes
        - LASSO loses confidence interval
        - Still preserves beta change





:mag: MD Retro
---
### What we can start Doing
- Modeling
    - Start developing Logistic Lasso
        - What features to develop interactions for? 
        - Cross Validation on lambda
    - AIC/BIC stepwise 
    - GAM Model
- Networks
    - Develop simple metric
    - Test metric in prediction

:closed_book: Tasks
--

### Visualization:
- Doug
    - [ ] Consolidates plots 
- Sam
    - [ ] Merge graphics that we generated into coherent message
- Deborah
    - [ ] Provide critical feedback on images 
        - Are images clear?
        - Is point well taken
        - Design, etc

### Feature Engineering:

- Sam
    - [x] Add linkages per beneficiary network and doctor network
    - [x] Finish consolidate file
    - [ ] Number of patients per physician (doctor:patient ratio)

### Modeling:
- Doug
    - [x] Tree Based Modeling
        - [x] [6/13] Random Forest
            - [x] Dummification of Variables
            - [x] Upsampling / Class Balance
        - [ ] [6/16] Gradient Boost
    - [ ] [6/17] SVM 
- Sam
    - [x] Logistic Regression
        - [x] [6/13] Lasso Penalty Multivariable Logistic
            - [x] Dummification of Variables
        - [ ] [6/17] AIC Stepwise Selection on Features
    - [ ] [6/16] NN Network Model


### SQL Server: Deborah :
- [x] [6/12] Where to host
    - [x] AWS RDS
- [x] [6/12] How to set up server / testing
    - [x] Input dataset and test basic queries
- [x] [6/13] Working Server
- [ ] [6/16] MBA Overview
    - [ ] [6/17] Incorporation of Insights

## Notes 
<!-- Other important details discussed during the meeting can be entered here. -->

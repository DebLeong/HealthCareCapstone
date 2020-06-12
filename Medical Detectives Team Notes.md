Medical Detectives: Team Notes
===

###### tags: `Mentor` `MedicalFraud`


:dart: MD Goal
---
- Identify Fraud within a medical network
- Decompose Fraud classification down to the doctor and beneficiary level
- Provide investigative tool for insurance companies
___

:books: MD Backlog
---
- Basic Model Setup
- Extract metrics from Network Graphs
- Setup SQL server
- Setup Shiny APP

:books: Meeting Notes
---

Daily Meeting
---

Luke Meeting
---


- Visualizations
    - Networks
        - Simple metric to Start
            - Density
            - Connectivity
            - Limited amount of time
        - Cluster Analysis of Networks
    - Aggregate Graphs
- Modeling
    - Tree Based Models
    - Interaction Terms in Lasso LogReg or step wise AIC/BIC selection. 
        - Dummified inpat/outpat with patient attributes
        - LASSO loses confidence interval
        - Still preserves beta change
    - NLP Work on Diagnostic Codes?
        - Problems:
            - Lack of large data set
            - Words very specific and rare
        - Already have bins for diagnostic code buckets
        - Term Frequency better metric



3. Final Product
    - Shiny App
        - No discussion
    - Presentation





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
    - [ ] Add linkages per beneficiary network and doctor network
    - [ ] Finish consolidate file
    - [ ] Number of patients per physician (doctor:patient ratio)

### Modeling:
- Doug
    - [ ] Tree Based Modeling
        - [ ] [6/13] Random Forest
            - [ ] Dummification of Variables
            - [ ] Upsampling / Class Balance
        - [ ] [6/14] Parameter Tuned RF 
- Sam
    - [ ] Logistic Regression
        - [ ] [6/12] Single Variable Logistic Series
        - [ ] [6/13] Lasso Penalty Multivariable Logistic
            - [ ] Dummification of Variables


### SQL Server: Deborah :
- [ ] [6/12] Where to host
    - [ ] Heroku
    - [ ] MySQL
- [ ] [6/12] How to set up server / testing
    - [ ] Input dataset and test basic queries
- [ ] [6/13] Working Server

## Notes 
<!-- Other important details discussed during the meeting can be entered here. -->

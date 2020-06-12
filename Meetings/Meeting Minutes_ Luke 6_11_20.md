Meeting Minutes: Luke 6/11/20
===

###### tags: `Mentor` `MedicalFraud`


1. Notes`45min`

    - Visualizations
        - 
        - Networks
            - Simple metric to Start
                - Density
                - Connectivity
                - Limited amount of time
            - Cluster Analysis of Networks
        - Aggregate Graphs
    - Modeling
        - 
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



2. Work Scheduling `45min`


3. Final Product `20min`
- Shiny App
    - No discussion
- 

:::


:dart: MD Goal
---
- Identify Fraud within a medical network
- Decompose Fraud classification down to the doctor and beneficiary level
- Provide investigative tool for insurance companies

:books: MD Backlog
---
- Basic Model Setup
- Extract metrics from Network Graphs
- Setup SQL server
- Setup Shiny APP

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
==Importance== (1 - 5) / Name / **Estimate** (1, 2, 3, 5, 8, 13)

### TEMPLATE
### Visualization:
- [ ] ==5== Email invite
  - [x] ==4== Email registration page **5**
  - [ ] ==5== Email invitees **3**
- [ ] ==4== Setup e2e test in production **1**

### Modeling:
- [ ] ==4== Interview users **8**
- [ ] ==5== Build roll-up display content **5**
- [ ] ==5== Help user discover new features **5**

## Notes 
<!-- Other important details discussed during the meeting can be entered here. -->

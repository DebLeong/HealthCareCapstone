

propat = function(data, state, county){
  if(county == 'all'){
    county = data %>%
      filter(State %in% state) %>%
      distinct(County) %>% pull
  }
  
  data.filt = 
    data %>% 
    filter(State %in% state, County %in% county) %>% 
    dplyr::select(Provider, PotentialFraud, ClaimID, BeneID, WhetherDead) %>% 
    group_by(Provider, PotentialFraud, BeneID, WhetherDead) %>% 
    tally() %>% 
    rename('weights' = 'n') %>% 
    data.frame()
  
  ## Get Provider | Beneficiary
  connections = data.filt %>% dplyr::select(Provider,BeneID,weights)
  
  ## Create bipartite graph
  Bnet <- graph.data.frame(connections,directed=FALSE)
  
  ## Add attributes
  shapes <- c(21,15)
  
  # dead = data.filt %>% 
  #   distinct(BeneID, WhetherDead)
  
  fraud = data.filt %>% select(Provider,PotentialFraud)
  
  V(Bnet)$type <- V(Bnet)$name %in% connections[,1]
  
  V(Bnet)$actor <- ifelse(V(Bnet)$name %in% connections[,1],'Provider','Patient')
  
  V(Bnet)$fraud <- ifelse(V(Bnet)$name %in% fraud[,1],fraud[,2],'Patient')
  
  V(Bnet)$size <- degree(Bnet)
  
  #V(Bnet)$dead <- ifelse(V(Bnet)$name %in% dead[,1], dead[,2], 0)
  
  # Add node attribute for dead or not
  
  #E(Bnet)$weight <- 
  
  V(Bnet)$shape <- shapes[V(Bnet)$type+1]
  
  # Create 4 new features for connectivity of providers based on bipartite projection graphs based on 
  # doctor and patient networks
  
  return(Bnet)
}

prodoc = function(data, state, county){
  if(county == 'all'){
    county = data %>% 
      filter(State %in% state) %>% 
      distinct(County) %>% pull
  }
  
  data.filt = 
    data %>% 
    filter(State %in% state, County %in% county) %>% 
    dplyr::select(Provider, PotentialFraud, ClaimID, 
           AttendingPhysician, OperatingPhysician, OtherPhysician) %>% 
    pivot_longer(cols=c(AttendingPhysician,OperatingPhysician,OtherPhysician), 
                 names_to = "Type", values_to = "Doctor") %>%
    filter(complete.cases(.)) %>% 
    group_by(Provider, PotentialFraud, Doctor) %>% 
    tally() %>% 
    rename('weights' = 'n') %>% 
    data.frame()
  
  ## Get Provider | Beneficiary
  connections = data.filt %>% dplyr::select(Provider,Doctor,weights)
  
  ## Create bipartite graph
  Bnet <- graph.data.frame(connections,directed=FALSE)
  
  ## Add attributes
  shapes <- c(25,15)
  
  
  fraud = data.filt %>% select(Provider,PotentialFraud)
  
  V(Bnet)$type <- V(Bnet)$name %in% connections[,1]
  
  V(Bnet)$actor <- ifelse(V(Bnet)$name %in% connections[,1],'Provider','Patient')
  
  V(Bnet)$fraud <- ifelse(V(Bnet)$name %in% fraud[,1],fraud[,2],'Doctor')
  
  V(Bnet)$size <- degree(Bnet)
  
  # Add node attribute for dead or not
  
  #E(Bnet)$weight <- 
  
  V(Bnet)$shape <- shapes[V(Bnet)$type+1]
  
  # Create 4 new features for connectivity of providers based on bipartite projection graphs based on 
  # doctor and patient networks
  
  return(Bnet)
}

patdoc = function(data, state, county){
  if(county == 'all'){
    county = data %>% 
      filter(State %in% state) %>% 
      distinct(County) %>% pull
  }
  
  data.filt = 
    data %>% 
    filter(State %in% state, County %in% county) %>% 
    dplyr::select(ClaimID, BeneID, 
                  AttendingPhysician, OperatingPhysician, OtherPhysician) %>% 
    pivot_longer(cols=c(AttendingPhysician,OperatingPhysician,OtherPhysician), 
                 names_to = "Type", values_to = "Doctor") %>%
    filter(complete.cases(.)) %>% 
    group_by(BeneID, Doctor) %>% 
    tally() %>% 
    rename('weights' = 'n') %>% 
    data.frame()
  
  ## Get Provider | Beneficiary
  connections = data.filt %>% dplyr::select(BeneID,Doctor,weights)
  
  ## Create bipartite graph
  Bnet <- graph.data.frame(connections,directed=FALSE)
  
  ## Add attributes
  shapes <- c(25,21)
  
  
  #fraud = data.filt %>% select(Provider,PotentialFraud)
  
  V(Bnet)$type <- V(Bnet)$name %in% connections[,1]
  #V(Bnet)$actor <- ifelse(V(Bnet)$name %in% connections[,1],'Provider','Patient')
  
  #V(Bnet)$fraud <- ifelse(V(Bnet)$name %in% fraud[,1],fraud[,2],'Doctor')
  
  V(Bnet)$size <- degree(Bnet)
  
  # Add node attribute for dead or not
  
  #E(Bnet)$weight <- 
  
  V(Bnet)$shape <- shapes[V(Bnet)$type+1]
  
  # Create 4 new features for connectivity of providers based on bipartite projection graphs based on 
  # doctor and patient networks
  
  return(Bnet)
}
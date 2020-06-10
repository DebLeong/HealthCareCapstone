

get_Bnet = function(data, state, county){
  
  data.filt = 
    data %>% 
    dplyr::select(State, County, Provider, PotentialFraud, ClaimID, BeneID) %>% 
    group_by(State, County, Provider, PotentialFraud, BeneID) %>% 
    tally() %>% 
    filter(State %in% state, County %in% county) %>% 
    rename('weights' = 'n') %>% 
    data.frame()
  
  ## Get Provider | Beneficiary
  connections = data.filt %>% dplyr::select(Provider,BeneID,weights)
  
  ## Create bipartite graph
  Bnet <- graph.data.frame(connections,directed=FALSE)
  
  ## Add attributes
  shapes <- c(21,15)
  
  
  fraud = data.filt %>% select(Provider,PotentialFraud)
  
  V(Bnet)$type <- V(Bnet)$name %in% connections[,1]
  
  V(Bnet)$actor <- ifelse(V(Bnet)$name %in% connections[,1],'Provider','Patient')
  
  V(Bnet)$fraud <- ifelse(V(Bnet)$name %in% fraud[,1],fraud[,2],'Patient')
  
  V(Bnet)$size <- degree(Bnet)
  
  # Add node attribute for dead or not
  
  #E(Bnet)$weight <- 
  
  V(Bnet)$shape <- shapes[V(Bnet)$type+1]
  
  # Create 4 new features for connectivity of providers based on bipartite projection graphs based on 
  # doctor and patient networks
  
  return(Bnet)
}
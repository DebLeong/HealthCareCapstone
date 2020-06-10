source("getNet.R")
source("plotNet.R")
require(tidyverse)
require(network)
require(ggraph)
require(igraph)
require(graphlayouts)

netAnal = function(data, state, county, 
                   type = 'propat', layout = 'stress', 
                   saveFile = FALSE){
  
  if (type == 'propat'){
    bnet = propat(data, state, county)
    plotProPat(bnet, layout = layout, save = saveFile)
  } else if (type == 'prodoc') {
    bnet = prodoc(data, state, county)
    plotProDoc(bnet, layout = layout, save = saveFile)
  } else if (type == 'patdoc') {
    bnet = patdoc(data, state, county)
    plotPatDoc(bnet, layout = layout, save = saveFile)
  } else if (type == 'all') {
    propat_net = propat(data, state, county)
    prodoc_net = prodoc(data, state, county)
    patdoc_net = patdoc(data, state, county)
    
    
    plotProPat(propat_net, layout = layout, save = saveFile)
    print("")
    plotProDoc(prodoc_net, layout = layout, save = saveFile)
    print("")
    plotPatDoc(patdoc_net, layout = layout, save = saveFile)
    
    
    
    
  }
}
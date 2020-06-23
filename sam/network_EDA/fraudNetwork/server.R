#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#


# Define server logic required to draw a histogram
shinyServer(function(input, output, session) {
    
    net = reactive({
        type = input$network_type_select
        
        if (type == 'Provider-Patient'){
            propat(data, input$state_select, input$county_select, input$status_select)
        } else if (type == 'Provider-Doctor') {
            prodoc(data, input$state_select, input$county_select, input$status_select)
        } else if (type == 'Patient-Doctor') {
            patdoc(data, input$state_select, input$county_select, input$status_select)
        } 
    })
    
    
    output$plot = renderPlot({
        type = input$network_type_select
        bnet = net()
        if (type == 'Provider-Patient'){
            plotProPat(bnet, input$state_select, input$county_select, layout = input$layout_select)
        } else if (type == 'Provider-Doctor') {
            plotProDoc(bnet, input$state_select, input$county_select, layout = input$layout_select)
        } else if (type == 'Patient-Doctor') {
            plotPatDoc(bnet, input$state_select, input$county_select, layout = input$layout_select)
        } 
    })
    
    output$actor1_plot = renderPlot({
        projection = bipartite.projection(net())
        bn.actor1 = projection$proj1
        
        if (grepl('PRV',V(bn.actor1)$name[1], fixed=TRUE)){
            plotActor(bn.actor1, 
                      paste0("Provider Network: ",input$state_select,
                             ', County: ',input$county_select),
                      actor='provider',
                      layout = 'tree')
        } else if (grepl('PHYS',V(bn.actor1)$name[1], fixed=TRUE)){
            plotActor(bn.actor1, 
                      paste0("Doctor Network: ",input$state_select,
                             ', County: ',input$county_select),
                      actor='doctor',
                      layout = 'tree')
        } else {
            plotActor(bn.actor1, 
                      paste0("Patient Network: ",input$state_select,
                             ', County: ',input$county_select),
                      actor='patient',
                      layout = 'mds')
        }
    })
    
    output$actor2_plot = renderPlot({
        projection = bipartite.projection(net())
        bn.actor2 = projection$proj2
        
        if (grepl('PRV',V(bn.actor2)$name[1], fixed=TRUE)){
            plotActor(bn.actor2, 
                      paste0("Provider Network: ",input$state_select,
                             ', County: ',input$county_select),
                      actor='provider',
                      layout = 'tree')
        } else if (grepl('PHYS',V(bn.actor2)$name[1], fixed=TRUE)){
            plotActor(bn.actor2, 
                      paste0("Doctor Network: ",input$state_select,
                             ', County: ',input$county_select),
                      actor='doctor',
                      layout = 'tree')
        } else {
            plotActor(bn.actor2, 
                      paste0("Patient Network: ",input$state_select,
                             ', County: ',input$county_select),
                      actor='patient',
                      layout = 'mds')
        }
    })
    
    
    output$duplicates_plot = renderPlot({
        #type = input$dnet_type_select
        plotDnet(Dnet, layout = input$dup_layout_select)
    })
    
    observeEvent(input$state_select, {
        choices =
            data %>%
            filter(State == input$state_select) %>%
            distinct(County)
        
        updatePickerInput(session = session, inputId = 'county_select', 
                          choices = sort(choices[[1]]), selected = 0)
    })
    
    output$table <- DT::renderDataTable({
        df = claimTrack %>% select(-c(ClaimMultiplier,TotalClaim_S,
                                      ClaimDays_S,State_S,State_R,
                                      ClaimDays_R,DiffLengthOfStay,
                                      SimolClaim,Status_R,Status_S))
        DT::datatable(df, escape = FALSE)
    },
    options = list(
        autoWidth = TRUE,
        columnDefs = list(list(targets = "_all")))
    )



})

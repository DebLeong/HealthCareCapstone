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
            propat(data, input$state_select, input$county_select)
        } else if (type == 'Provider-Doctor') {
            prodoc(data, input$state_select, input$county_select)
        } else if (type == 'Patient-Doctor') {
            patdoc(data, input$state_select, input$county_select)
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
            plotActor(bn.actor1, "Provider Network" ,provider = TRUE)
        } else if (grepl('PHYS',V(bn.actor1)$name[1], fixed=TRUE)){
            plotActor(bn.actor1, "Doctor Network",provider = FALSE)
        } else {
            plotActor(bn.actor1, "Patient Network",provider = FALSE)
        }
    })
    
    output$actor2_plot = renderPlot({
        projection = bipartite.projection(net())
        bn.actor2 = projection$proj2
        
        if (grepl('PRV',V(bn.actor2)$name[1], fixed=TRUE)){
            plotActor(bn.actor2, "Provider Network" ,provider = TRUE)
        } else if (grepl('PHYS',V(bn.actor2)$name[1], fixed=TRUE)){
            plotActor(bn.actor2, "Doctor Network",provider = FALSE)
        } else {
            plotActor(bn.actor2, "Patient Network",provider = FALSE)
        }
    })
    
    observeEvent(input$state_select, {
        choices =
            data %>%
            filter(State == input$state_select) %>%
            distinct(County)
        
        updatePickerInput(session = session, inputId = 'county_select', 
                          choices = sort(choices[[1]]), selected = 0)
    })



})

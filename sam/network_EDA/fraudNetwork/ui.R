#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#
if(!require(shinyWidgets)) install.packages("shinyWidgets", repos = "http://cran.us.r-project.org")
if(!require(shinydashboard)) install.packages("shinydashboard", repos = "http://cran.us.r-project.org")
if(!require(shinythemes)) install.packages("shinythemes", repos = "http://cran.us.r-project.org")

bootstrapPage(
  navbarPage(theme = "bootstrap.min.css",collapsible=TRUE, "Medical Fraud", id="nav",
             tabPanel("Affiliation Network",
                      div(
                        tags$style(type = "text/css", "#plot {height: calc(100vh - 80px) !important;}"),
                        absolutePanel(id='controls',
                                      top = 100, left = 40, width = "200px", fixed=TRUE,
                                      draggable = FALSE, height = "500px",
                                      
                                      style = "font-size: 16px !important;",
                                      
                                      pickerInput("network_type_select", h4("Select Network:"),   
                                                  choices = c("Provider-Doctor","Provider-Patient","Patient-Doctor"), 
                                                  selected = "Provider-Patient",
                                                  options = list(`actions-box` = TRUE,
                                                                 inline = TRUE),
                                                  multiple = FALSE),
                                      pickerInput("state_select", h4("State:"),   
                                                  choices = states, 
                                                  selected = "New York",
                                                  options = list(`actions-box` = TRUE,
                                                                 inline = TRUE),
                                                  multiple = FALSE),
                                      pickerInput("county_select", h4("County:"),   
                                                  choices = NULL, 
                                                  selected = NULL,
                                                  options = list(`actions-box` = TRUE,
                                                                 inline = TRUE),
                                                  multiple = TRUE),
                                      pickerInput("layout_select", h4("Graph Layout:"),
                                                choices = c('sugiyama','stress','kk'), 
                                                selected = "stress",
                                                options = list(`actions-box` = TRUE,
                                                                inline = TRUE),
                                                multiple = FALSE)
                        ),
                        plotOutput("plot", width="100%", height = "100%")
                      )
                      
             ),
             tabPanel("Bipartite Projection",
                      fluidRow(
                        column(6,
                               plotOutput("actor1_plot")
                               ),
                        column(6,
                               plotOutput("actor2_plot")
                               )
                      )
             )
  ) # end of navbar page
) # end of bootstrap page

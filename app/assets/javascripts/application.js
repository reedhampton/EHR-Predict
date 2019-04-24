// This is a manifest file that'll be compiled into application.js, which will include all the files
// listed below.
//
// Any JavaScript/Coffee file within this directory, lib/assets/javascripts, or any plugin's
// vendor/assets/javascripts directory can be referenced here using a relative path.
//
// It's not advisable to add code directly here, but if you do, it'll appear at the bottom of the
// compiled file. JavaScript code in this file should be added after the last require_* statement.
//
// Read Sprockets README (https://github.com/rails/sprockets#sprockets-directives) for details
// about supported directives.
//
//= require rails-ujs
//= require turbolinks
//= require_tree .
//= require Chart.bundle
//= require chartkick
//= require jquery3
//= require popper
//= require bootstrap


function ShowHide(evt, ID)
{
    
    var i, graphs, toggles;
    
    // Get all elements and hide them all
    graphs = document.getElementsByClassName("col-md-12");
    for (i = 0; i < graphs.length; i++) 
    {
        graphs[i].style.display = "none";
    }
    
    toggles = document.getElementsByClassName("btn btn-primary");
    for (i = 0; i < toggles.length; i++) 
    {
        toggles[i].className = toggles[i].className.replace(" active", "");
    }
    
    document.getElementById(ID).style.display = "block";
    evt.currentTarget.className += " active";
}  
    
    
function OpenNotes(evt, ID) 
{
    
    var i, tabcontent, tablinks;
    
    tabcontent = document.getElementsByClassName("tab-pane");
    for (i = 0; i < tabcontent.length; i++)
    {
        tabcontent[i].style.display = "none";
    }
    
    tablinks = document.getElementsByClassName("btn btn-primary");
    for (i = 0; i < tablinks.length; i++)
    {   
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    
    document.getElementById(ID).style.display = "block";
    evt.currentTarget.className += " active";
}
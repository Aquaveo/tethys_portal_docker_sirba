/*****************************************************************************
 * FILE:    sirba_forecast MAIN JS
 * DATE:    September 2021
 * AUTHOR: Bernard Minoungou, adapted from Spencer McDonald codes
 * COPYRIGHT:
 * LICENSE:
 *****************************************************************************/

/*****************************************************************************
 *                      LIBRARY WRAPPER
 *****************************************************************************/

 var LIBRARY_OBJECT = (function() {
    // Wrap the library in a package function
    "use strict"; // And enable strict mode for this library

    /************************************************************************
     *                      MODULE LEVEL / GLOBAL VARIABLES
     *************************************************************************/

    var public_interface,			// Object returned by the module
        gs_workspace = 'sirbaforecast';


    /************************************************************************
     *                    PRIVATE FUNCTION DECLARATIONS
     *************************************************************************/
    var historicalrun,
    validateQuery,
    init_all,
    clear_selection,
    getCookie;




    /************************************************************************
     *                    PRIVATE FUNCTION IMPLEMENTATIONS
     *************************************************************************/

    //Get a CSRF cookie for request
    getCookie = function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    //find if method is csrf safe
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    //add csrf token to appropriate ajax requests
    $(function() {
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
                }
            }
        });
    }); //document ready

    //send data to database with error messages
    function ajax_update_database(ajax_url, ajax_data) {
        //backslash at end of url is required
        if (ajax_url.substr(-1) !== "/") {
            ajax_url = ajax_url.concat("/");
        }
        //update database
        var xhr = jQuery.ajax({
            type: "POST",
            url: ajax_url,
            dataType: "json",
            data: ajax_data
        });
        xhr.done(function(data) {
            if("success" in data) {
                // console.log("success");
            } else {
                console.log(xhr.responseText);
            }
        })
        .fail(function(xhr, status, error) {
            console.log(xhr.responseText);
        });

        console.log(xhr)

        return xhr;
        
    }
        //send data to database with error messages
    function ajax_update_database(ajax_url, ajax_data) {
        //backslash at end of url is required
        if (ajax_url.substr(-1) !== "/") {
            ajax_url = ajax_url.concat("/");
        }
        //update database
        var xhr = jQuery.ajax({
            type: "POST",
            url: ajax_url,
            dataType: "json",
            data: ajax_data
        });
        xhr.done(function(data) {
            if("success" in data) {
                // console.log("success");
            } else {
                console.log(xhr.responseText);
            }
        })
        .fail(function(xhr, status, error) {
            console.log(xhr.responseText);
        });

        console.log(xhr)

        return xhr;
        
    }

    //send data to database with error messages

    init_all = function(){

    };



    historicalrun = function() {
//      Get the values from the nasaaccess form and pass them to the run_nasaaccess python controller
        var start = $('#start_pick').val();
        var end = $('#end_pick').val();
        var select_variable = $('#select_variable').val();
        var select_comid = $('#select_comid').val();
        var email = $('#id_email').val();
        $.ajax({
            type: 'POST',
            url: run,
            //method: 'POST',
            //dataType:
            data: {
                'select_variable': select_variable,
                'select_comid': select_comid,
                'startDate': start,
                'endDate': end,
                'email': email,
            },   
            }).done(function(data) {
                console.log(data)
                if (data.Result === 'The historical discharge is saved') {
                    $('#job_init').removeClass('hidden')
                    setTimeout(function () {
                        $('#job_init').addClass('hidden')
                    }, 10000);
                }
    
            });

        //});
    }

    validateQuery = function() {
        var start = $('#start_pick').val();
        var end = $('#end_pick').val();
        var select_variable = $('#select_variable').val();
        var select_comid = $('#select_comid').val();
        if (start === undefined || end === undefined || select_variable === undefined) {
        //if (start === undefined || end === undefined || select_variable === undefined || select_comid === undefined ) {
            $("#cont-modal").modal('show');
            //alert('Please be sure you have selected a variable, COMID, start and end dates')
            //alert(select_comid)
        } else {
            $("#cont-modal").modal('show');
            //alert('Please be sure you have selected a variable, COMID, start and end dates')
            //alert(end)
        }
    }


    /************************************************************************
     *                        DEFINE PUBLIC INTERFACE
     *************************************************************************/

    public_interface = {

    };

    /************************************************************************
     *                  INITIALIZATION / CONSTRUCTOR
     *************************************************************************/

    // Initialization: jQuery function that gets called when
    // the DOM tree finishes loading

    $(function() {
        init_all();
//        $("#help-modal").modal('show');
        $('#loading').addClass('hidden')

        $('#return_period').click(function() {
            validateQuery();
            //historicalrun();
        });

        $('#submit_form').click(function() {
            //$("#cont-modal").modal('hide');
            //validateQuery();
            //historicalrun();
            $("#cont-modal").modal('hide');
            historicalrun();
        });

        $('#download_data').click(function() {
            $("#download-modal").modal('show');
        });
    });




    return public_interface;


}());// End of package wrapper
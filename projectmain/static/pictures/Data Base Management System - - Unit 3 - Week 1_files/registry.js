/**
 * @fileoverview Utility to add AJAX handler to pages.
 */

function element(id) {
  return document.getElementById(id);
}

// Update a particular HTML element with a new value
function updateInnerHTML(elmId, value) {
  element(elmId).innerHTML = value;
}

function updateValue(elmId, value) {
  element(elmId).value = value;
}

function parseAjaxResponse(s) {
  // console.log(s);
  var xssiPrefix = ")]}'";
  if (s)
  return JSON.parse(String(s).replace(xssiPrefix, ''));
  else return;
}


function getSelectValue(id) {
  var selectEl = element(id);
  return selectEl.options[selectEl.selectedIndex].value;
}


function my_error( jqXHR,  textStatus,  errorThrown ){
console.log(textStatus);
console.log(errorThrown);
}

// Server object that will contain the callable methods
ajax_server = {};

// Adds a stub function that will pass the arguments to the AJAX call
//
// functionName: the name of the server's AJAX function to call
// callback: function to run after completion of ajax request
// xsrf_token: XSRF token to be passed for POST requests. If this is not present
// then we assume that the ajax request is a GET request.
function installFunction(end_point, functionName, callback, xsrf_token) {
  ajax_server[functionName] = function(opt_arg) {
    var type = xsrf_token ? 'POST' : 'GET';
    var async = (callback != null);

    var data = {};
    data.action = functionName;
    if (xsrf_token) {
      data.xsrf_token = xsrf_token;
    }
    data.time = new Date().getTime();
    if (opt_arg) {
      $.extend(data, opt_arg);
    }
    $.ajax(end_point, {
      type: type,
      async: async,
      data: data,
      dataType:"text",
      success: function(data){
        json_data = parseAjaxResponse(data);
        callback(json_data);
      },
      error: function (request, status, error) {
        console.log(status);
        console.log(error);
      }
    });
  };
}

function noopCallback() {}

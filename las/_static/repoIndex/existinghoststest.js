$(document).ready(function() { 
    $.ajax({
        url: "/repoIndex/existingHostsTest/",
        type: "POST",
        contentType: "application/json",
        dataType: "json",
        success: function(data){
            $.each(data, function(i, item) {
                console.log(item)
                if ( item['status'] == "UP" ) {
                    // $('<td>').value("<td><span class=\"badge badge-pill badge-success\">UP</span></td>");
                    item.status = "<span class=\"badge badge-pill badge-success\">UP</span>"
                } else if ( item['status'] == "PATH" ) {
                    // $('<td>').value("<td><span class=\"badge badge-pill badge-warning\">PATH</span></td>");
                    item.status = "<span class=\"badge badge-pill badge-warning\">PATH</span>"
                } else {
                    // $('<td>').value("<td><span class=\"badge badge-pill badge-danger\">DOWN</span></td>");
                    item.status = "<span class=\"badge badge-pill badge-danger\">DOWN</span>"
                }

                // var csrf_token = '{{ csrf_token }}'
                var csrftoken2 = document.getElementsByName('csrfmiddlewaretoken')[0].value;
                var edit_form_html = "<form id=\"host_edit\" name=\"myform\" action=\"/repoIndex/landhostEdit/\" method=\"POST\">"
                + "<input type=\"hidden\" name=\"host_edit_address\" value=\""+ item.address +"\"/>"
                + "<input type=\"hidden\" name=\"host_edit_toggle\" value=\"ENABLED\"/>"
                + "<input type=\"hidden\" name=\"csrfmiddlewaretoken\" value=\""+ csrftoken2 +"\"/>"
                + "<input type=\"hidden\" name=\"host_edit_path\" value=\""+ item.path +"\"/>"
                + "<input type=\"hidden\" name=\"host_edit_description\" value=\""+ item.description +"\"/>"
                + "<input type=\"submit\" value=\"Edit\" class=\"btn btn-primary btn-sm\"/></td></form></tr>"

                var host_row_html = "<tr><td>"+ item.status +"</td><td>"+ item.address +"</td><td>"+ item.path +"</td><td>"
                var html_string = host_row_html + edit_form_html

                var $tr = $(html_string).appendTo('#existing_hosts');
            });
        },
        error: function (xhr, ajaxOptions, thrownError) {
            var errorMsg = 'Ajax request failed: ' + xhr.responseText;
            $('#content').html(errorMsg);
            alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
          }
    });
});
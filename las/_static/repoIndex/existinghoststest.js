function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

// function submitForm(){
//     var frm = document.getElementById("host_edit");
//     // frm.action = '/repoIndex/landhostEdit/';
//     var inputElem = document.createElement('input');
//     inputElem.type = 'hidden';
//     inputElem.name = 'csrfmiddlewaretoken';
//     // inputElem.value = getCookie('csrftoken');
//     inputElem.value = getCSRFTokenValue();
//     console.log("inputElem.value is: ", inputElem.value)
//     // frm.appendChild(inputElem);
//     // if(document.myform.onsubmit()){
//     //     document.myform.submit();
//     // }
//     // return true;
// }

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
                var edit_form_html = "<form id=\"host_edit\" name=\"myform\" action=\"/repoIndex/landhostEdit/\" method=\"POST\">"
                + "<input type=\"hidden\" name=\"host_edit_address\" value=\""+ item.address +"\"/>"
                + "<input type=\"hidden\" name=\"host_edit_toggle\" value=\"ENABLED\"/>"
                + "<input type=\"hidden\" name=\"csrfmiddlewaretoken\" value=\""+ getCookie('csrftoken') +"\"/>"
                + "<input type=\"hidden\" name=\"host_edit_path\" value=\""+ item.path +"\"/>"
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


// {/* <form id="host_edit" action="{% url 'landhostEdit' %}" method="POST">
// {%csrf_token%}
// <input type="hidden" id="host_edit-address" name="host_edit_address" value="{{ q.address }}"/>
// <input type="hidden" id="host_edit-path" name="host_edit_path" value="{{ q.path }}"/>
// <td><input type="submit" id="host_edit-submit" value="Edit" class="btn btn-primary btn-sm"/></td>
// </form> */}

// {/* <tr>
// {% if " + data[i]['status'] + " == "UP" %}
    
// {% elif " + data[i]['status'] + " == "PATH" %}
//     <td><span class="badge badge-pill badge-warning">PATH</span></td>
// {% else %}
//     <td><span class="badge badge-pill badge-danger">DOWN</span></td>
// {% endif %}
// <td>{{ " + data[i]['address'] + " }}</td>
// <td>{{ " + data[i]['path'] + " }}</td>
// <form id="host_edit" action="{% url 'landhostEdit' %}" method="POST">
//     {%csrf_token%}
//     <input type="hidden" id="host_edit-address" name="host_edit_address" value="{{ " + data[i]['address'] + " }}"/>
//     <input type="hidden" id="host_edit-path" name="host_edit_path" value="{{ " + data[i]['path'] + " }}"/>
//     <td><input type="submit" id="host_edit-submit" value="Edit" class="btn btn-primary btn-sm"/></td>
// </form>
// </tr>   */}
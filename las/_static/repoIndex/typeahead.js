$.typeahead({
    input: '.js-typeahead-hosts_v1',
    minLength: 1,
    order: "asc",
    dynamic: true,
    delay: 500,
    backdrop: {
        "background-color": "#fff"
    },
    template: function (query, item) {
        
        var color = "#777";

        return  '<span class="row">' +
                '<span class="hostname">  {{host_username}}@{{hostname}} <br><small style="color: ' + color + ';">  ({{host_path}})</small></span>' +
                '</span>'
    },
    emptyTemplate: "no result for {{query}}",
    source: {
        host: {
            display: "hostname",
            ajax: function (query) {
                return {
                    type: "GET",
                    url: "/repoIndex/autocompleteHostsAddExperiment/",
                    // path: "data.host",
                    data: {
                        q: "{{query}}"
                    },
                    callback: {
                        done: function (data) {
                            console.log("data TOT is: "+data)
                            console.log("datalen is: "+data.length)
                            for (var i = 0; i < data.length; i++) {
                                console.log("data[i] is: "+JSON.stringify(data[i].hostname))
                                console.log("data[i] is: "+JSON.stringify(data[i].host_username))
                                console.log("data[i] is: "+JSON.stringify(data[i].host_path))
                            }
                            return data;
                        }
                    },
                    error: function(xhr){
                        // alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
                        alert('Error during hosts retrieval for autocomplete')
                    }
                }
            },
        }
    },
    callback: {
        onClick: function (node, a, item, event) {
 
            var username = $('#add_exp-host-username');
            username.val(item.host_username);
            var path = $('#add_exp-host-path');
            path.val(item.host_path);
 
        },
        onSendRequest: function (node, query) {
            console.log('request is sent')
        },
        onReceiveRequest: function (node, query) {
            console.log('request is received')
        }
    },
    debug: true
});

$.typeahead({
    input: '.js-typeahead-types_v2',
    minLength: 1,
    order: "asc",
    dynamic: true,
    delay: 500,
    backdrop: {
        "background-color": "#fff"
    },
    template: function (query, item) {
 
        var color = "#777";

        return '<span class="row">' +
            '<span class="Name">  {{Name}}<small style="color: ' + color + ';">  ({{Description}})</small></span>' +
        "</span>"
    },
    emptyTemplate: "no result for {{query}}",
    source: {
        type: {
            display: "Name",
            ajax: function (query) {
                return {
                    type: "GET",
                    url: "/repoIndex/landqueryExperimentType/",
                    // path: "data.host",
                    data: {
                        q: "{{query}}"
                    },
                    callback: {
                        done: function (data) {
                            console.log("data TOT is: "+data)
                            console.log("datalen is: "+data.length)
                            for (var i = 0; i < data.length; i++) {
                                console.log("data[i] is: "+JSON.stringify(data[i].Name))
                            }
                            return data;
                        }
                    },
                    error: function(xhr){
                        alert('Error during experiment types retrieval for autocomplete')
                    }
                }
            },
        }
    },
    callback: {
        onSendRequest: function (node, query) {
            console.log('request is sent')
        },
        onReceiveRequest: function (node, query) {
            console.log('request is received')
        }
    },
    debug: true
});

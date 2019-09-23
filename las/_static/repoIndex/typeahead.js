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
                        alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
                    }
                }
            },
        }
    },
    callback: {
        onClick: function (node, a, item, event) {
 
            var cane = $('#add_exp-host-username');
            cane.val(item.host_username);
 
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
                        alert('Request Status: ' + xhr.status + ' Status Text: ' + xhr.statusText + ' ' + xhr.responseText);
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

$.typeahead({
    input: '.js-typeahead-country_v2',
    order: "desc",
    source: {
        data: [
            "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
            "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh",
            "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia",
            "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burma",
            "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Central African Republic", "Chad",
            "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic", "Congo, Republic of the",
            "Costa Rica", "Cote d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti",
            "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador",
            "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Gabon",
            "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Greenland", "Grenada", "Guatemala", "Guinea",
            "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hong Kong", "Hungary", "Iceland", "India",
            "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan",
            "Kazakhstan", "Kenya", "Kiribati", "Korea, North", "Korea, South", "Kuwait", "Kyrgyzstan", "Laos",
            "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg",
            "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands",
            "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Mongolia", "Morocco", "Monaco",
            "Mozambique", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger",
            "Nigeria", "Norway", "Oman", "Pakistan", "Panama", "Papua New Guinea", "Paraguay", "Peru",
            "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Samoa", "San Marino",
            "Sao Tome", "Saudi Arabia", "Senegal", "Serbia and Montenegro", "Seychelles", "Sierra Leone",
            "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "Spain",
            "Sri Lanka", "Sudan", "Suriname", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan",
            "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey",
            "Turkmenistan", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States",
            "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
        ]
    },
    callback: {
        onInit: function (node) {
            console.log('Typeahead Initiated on ' + node.selector);
        }
    }
});
// $.typeahead({
//     input: '.js-typeahead-user_v1',
//     minLength: 1,
//     order: "asc",
//     dynamic: true,
//     delay: 500,
//     backdrop: {
//         "background-color": "#fff"
//     },
//     template: function (query, item) {
 
//         var color = "#777";
//         if (item.status === "owner") {
//             color = "#ff1493";
//         }
 
//         return '<span class="row">' +
//             '<span class="avatar">' +
//                 '<img src="{{avatar}}">' +
//             "</span>" +
//             '<span class="username">{{username}} <small style="color: ' + color + ';">({{status}})</small></span>' +
//             '<span class="id">({{id}})</span>' +
//         "</span>"
//     },
//     emptyTemplate: "no result for {{query}}",
//     source: {
//         user: {
//             display: "username",
//             href: "https://www.github.com/{{username|slugify}}",
//             data: [{
//                 "id": 415849,
//                 "username": "an inserted user that is not inside the database",
//                 "avatar": "https://avatars3.githubusercontent.com/u/415849",
//                 "status":  "contributor"
//             }],
//             ajax: function (query) {
//                 return {
//                     type: "GET",
//                     url: "/jquerytypeahead/user_v1.json",
//                     path: "data.user",
//                     data: {
//                         q: "{{query}}"
//                     },
//                     callback: {
//                         done: function (data) {
//                             for (var i = 0; i < data.data.user.length; i++) {
//                                 if (data.data.user[i].username === 'running-coder') {
//                                     data.data.user[i].status = 'owner';
//                                 } else {
//                                     data.data.user[i].status = 'contributor';
//                                 }
//                             }
//                             return data;
//                         }
//                     }
//                 }
//             }
 
//         },
//         project: {
//             display: "project",
//             href: function (item) {
//                 return '/' + item.project.replace(/\s+/g, '').toLowerCase() + '/documentation/'
//             },
//             ajax: [{
//                 type: "GET",
//                 url: "/jquerytypeahead/user_v1.json",
//                 data: {
//                     q: "{{query}}"
//                 }
//             }, "data.project"],
//             template: '<span>' +
//                 '<span class="project-logo">' +
//                     '<img src="{{image}}">' +
//                 '</span>' +
//                 '<span class="project-information">' +
//                     '<span class="project">{{project}} <small>{{version}}</small></span>' +
//                     '<ul>' +
//                         '<li>{{demo}} Demos</li>' +
//                         '<li>{{option}}+ Options</li>' +
//                         '<li>{{callback}}+ Callbacks</li>' +
//                     '</ul>' +
//                 '</span>' +
//             '</span>'
//         }
//     },
//     callback: {
//         onClick: function (node, a, item, event) {
 
//             // You can do a simple window.location of the item.href
//             alert(JSON.stringify(item));
 
//         },
//         onSendRequest: function (node, query) {
//             console.log('request is sent')
//         },
//         onReceiveRequest: function (node, query) {
//             console.log('request is received')
//         }
//     },
//     debug: true
// });
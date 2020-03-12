function spinner(enable) {
    if (enable) {
        $('.loading-spinner').show();
    }
    else {
        $('.loading-spinner').hide();
    }
}

function api_meetings() {
    spinner(true);

    $.get("./api/meetings", function(data) {
        console.log("API request: /api/meetings");
        $("#meetings-body").empty();

        data.forEach(function(element, i) {
            let mods = element.moderators.join(" | ");

            let creation = new Date(Date.parse(element.creation));

            let markup = `<tr>
<td>${i + 1}</td>
<td>${element.name}</td>
<td>${element.noUsers}</td>
<td>${mods}</td>
<td>${creation.toLocaleString()}</td>
</tr>`;
            $("#meetings-body").append(markup);
        });

        spinner(false);
    });
}

function api_server() {
        console.log("API request: /api/server");
        $.get("./api/server", function(data) {
            $("#text-server").html(data.server);
        });
}


$(function() {
    api_server();
    api_meetings();
    setInterval(api_meetings, 5000);
});
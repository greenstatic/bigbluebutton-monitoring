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

            // Ugly hack to make JS accept CET datetime
            // Will break with daylight savings and/or different timezones.
            let creationDateRaw = element.creation.replace("CET", "");
            let creation = new Date(Date.parse(creationDateRaw));

            let originContext = "";
            if (element.metadata['origin-context']) {
                originContext = element.metadata['origin-context'];
            }

            let markup = `<tr>
<td>${i + 1}</td>
<td>${element.name}</td>
<td>${element.noUsers}</td>
<td>${mods}</td>
<td>${element.metadata['origin-server']}</td>
<td>${originContext}</td>
<td>${creation.toLocaleString()}</td>
</tr>`;
            $("#meetings-body").append(markup);
        });
        $("#text-last-refresh").html(new Date().toLocaleString());
        spinner(false);
    });
}

function api_server() {
        console.log("API request: /api/server");
        $.get("./api/server", function(data) {
            $("#text-server").html(data.server);
            $("#text-version").html(data.version);
        });
}


$(function() {
    api_server();
    api_meetings();
    setInterval(api_meetings, 15 * 1000);
});
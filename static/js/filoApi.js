function let_it_shine(device_uuid) {
    $.ajax({
        url: "/api/rest/front/light/" + device_uuid,
        type: "get",
        async: false,
        success: function (stat) {
            alert("Findlock event sent!");
        },
        error: function () {
            alert("Could not sent an event to the findlock!");
        }
    })
}
function change_state_findlock(device_uuid, state) {
    $.ajax({
        url: "/api/rest/front/change_state/" + device_uuid + "/" + state,
        type: "get",
        async: false,
        success: function (stat) {
            alert("Findlock event sent!");
        },
        error: function () {
            alert("Could not sent an event to the findlock!");
        }
    })



}

function query_current_state(device_uuid)
{
    $.ajax({
        url: "/api/rest/front/get_state/" + device_uuid,
        type: "get",
        async: false,
        success: function(stat) {
            document.getElementById("event_type").innerHTML = stat.data.type
            document.getElementById("event_executed").innerHTML = stat.data.executed
            document.getElementById("event_time").innerHTML = stat.data.created_at
        },
        error: function() {
            console.log("Error")
        }
    })
}


function start_query_timer(device_uuid){
    setInterval(function(){
        query_current_state(device_uuid);
        update_all_time_classes();
    }, 1000);
}

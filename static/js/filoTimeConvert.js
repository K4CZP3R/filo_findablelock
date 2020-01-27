function onlyNumbers(input) {
    return /^\d+$/.test(input);
}

function timeConverter(input) {
    var a = new Date(input * 1000);
    var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var year = a.getFullYear();
    var month = months[a.getMonth()];
    var date = a.getDate();
    var hour = a.getHours();
    var min = a.getMinutes();
    var sec = a.getSeconds();
    var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec;
    return time;
}


function update_all_time_classes() {
    var filoUnixTime = document.getElementsByClassName("filoUnixTime");
    for (i = 0; i < filoUnixTime.length; i++) {
        if (onlyNumbers(filoUnixTime[i].textContent)) {
            filoUnixTime[i].textContent = timeConverter(filoUnixTime[i].textContent)
        }
    }
}
function filoGoogle_onSignOut(logout_location)
{
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function(){
        window.location.href = logout_location;
    })
    window.location.href = logout_location;
}

function filoGoogle_onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    var id_token = googleUser.getAuthResponse().id_token;
    var email = profile.getEmail();
    var avatar_link = profile.getImageUrl();
    var client_id = "61071107086-i8cph2ic9u5qd99gt53nm1snhsdcbkb1.apps.googleusercontent.com";

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/auth/google_login');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.responseText === "yes") {
            location.reload();
        }
        if (xhr.responseText === "no") {
            alert("Logging in with Google is not available right now.");
        }
    }
    xhr.send('idtoken=' + id_token + "&email=" + email + "&client_id=" + client_id + "&avatar_link=" + avatar_link);
}
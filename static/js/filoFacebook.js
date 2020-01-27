window.fbAsyncInit = function () {
    FB.init({
        appId: '449426579290722',
        autoLogAppEvents: true,
        xfbml: true,
        version: 'v5.0'
    });
};
var failed = false;
function filoFacebook_checkIfPerformedLogin()
{
    var AR = FB.getAuthResponse();
    if(AR != null && AR != undefined)
    {
        console.log("User logged in...");
        FB.api("/me", function(response) {
            var userName = response.name;
            var accessToken = FB.getAccessToken();
            var userId = FB.getUserID();

            var xhr = new XMLHttpRequest();
            xhr.open("POST", '/auth/facebook_login');
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.onload = function()
            {
                if(xhr.responseText === "yes")
                {
                    location.reload();
                }
                alert("Logging in with Facebook is not available right now.");
                console.log(xhr.responseText);
                failed = true;
            }
            xhr.send('id='+userId+"&name="+userName+"&access_token="+accessToken)
        
        })
    }
}

var id = window.setInterval(function(){
    var res = filoFacebook_checkIfPerformedLogin();
  }, 1000);


window.setInterval(function()
{
    if(failed) clearInterval(id);
},750);
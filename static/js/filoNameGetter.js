console.log("executed!")
var per_elements = document.getElementsByClassName("permission");
var i;
for(i = 0; i < per_elements.length; i++)
{
    var element_content = per_elements[i].textContent
    var element_type = per_elements[i].id
    console.log(element_content)


    $.ajax({
        url: "/api/rest/get_name/"+element_content,
        type: "get",
        async: false,
        success: function(stat){

            per_elements[i].innerHTML = stat.data
            console.log(stat.data)
        },
        error: function(){
            console.log("error")
        }
    })
}
const selectAll = document.querySelector("#selectAll")
const span_check_on = document.getElementById("check_all_on");
const span_check_off = document.getElementById("check_all_off");
selectAll.addEventListener("click",function(){
    console.log("Select All checkbox clicked.");
    if(span_check_on.style.display === "none"){
        span_check_on.style.display = "block";
        span_check_off.style.display = "none";
    }else{
        span_check_on.style.display = "none";
        span_check_off.style.display = "block";
    }
    document.querySelector("#issue_form")
        .querySelectorAll("table tr input[type=checkbox]")
        .forEach(function (input){
            input.checked=selectAll.checked
        })

})

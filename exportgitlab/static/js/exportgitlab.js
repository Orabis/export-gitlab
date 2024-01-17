const selectAll = document.querySelector("#selectAll")
const span_check_on = document.getElementById("check_all_on");
const span_check_off = document.getElementById("check_all_off");
const ungroup_issue_radio = document.getElementById("ungroup_issue")
const group_issue_radio = document.getElementById("group_issue")
const download_button = document.getElementById("issue_dl_button")
const checkboxes = document.querySelectorAll("#issue_form table tr input[type=checkbox]");
selectAll.addEventListener("click", function () {
    if (span_check_on.style.display === "none") {
        span_check_on.style.display = "block";
        span_check_off.style.display = "none";
    } else {
        span_check_on.style.display = "none";
        span_check_off.style.display = "block";
    }
    checkboxes.forEach(function (input) {
        input.checked = selectAll.checked

    })
    updateStates();

})
checkboxes.forEach(function (checkbox) {
    checkbox.addEventListener("click", function () {
        updateStates();
    })
})

function updateStates() {
    const checkedCount = document.querySelectorAll("#issue_form table tr input[type=checkbox]:checked").length;
    switch (checkedCount) {
        case 0:
            ungroup_issue_radio.setAttribute("disabled", "disabled");
            download_button.setAttribute("disabled", "disabled");
            group_issue_radio.setAttribute("disabled", "disabled");
            break;
        case 1:
            download_button.removeAttribute("disabled");
            group_issue_radio.removeAttribute("disabled");
            ungroup_issue_radio.setAttribute("disabled", "disabled");
            break;
        default:
            ungroup_issue_radio.removeAttribute("disabled");
            download_button.removeAttribute("disabled");
            group_issue_radio.removeAttribute("disabled");
            break;
    }
}

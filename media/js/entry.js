$(document).ready(function() {
    $("#vision_other").hide();
    $("#gradyear").hide();

    $("#ur_student").click(function() {$("#gradyear").toggle();});
    $("#hearing_normal").click(function() {$("#hearing_problems").toggle();});

    if ($(':input#entrydate').val() === "") {
        var today = new Date();
        var year = today.getFullYear();
        var month = today.getMonth() + 1;
        var day = today.getDate();
        $(':input#entrydate').val(year + "-" + month + "-" + day);
    }
});

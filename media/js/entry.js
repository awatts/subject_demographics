$(document).ready(function() {
    $('#newsubject').html5form({async : true, messages: 'en',  responseDiv: '#response', allBrowsers: true}); 

    $("#vision_other").hide();
    $("#gradyear").hide();

    $("#ur_student").click(function() {$("#gradyear").toggle();});
    $("#hearing_normal").click(function() {$("#hearing_problems").toggle();});
    $("#vision_normal").change(function() {
        if ($(this).val() === "Other") {
            $("#vision_other").slideDown();
        } else {
            $("#vision_other").slideUp();
        }
    });

    if ($(':input#entrydate').val() === "") {
        var today = new Date();
        var year = today.getFullYear();
        var month = today.getMonth() + 1;
        $(':input#entrydate').datepicker({ dateFormat: 'yy-mm-dd', defaultDate: new Date() });
    }
});

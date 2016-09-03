django.jQuery(function($) {
    // button submit of a form
    var $btn_submit = $('#form_generate_report input[type="submit"]');

    var selector_checkboxes_themes = '#form_generate_report table td input[id^="subject_"]';

    // event listen on click on themes names
    $(selector_checkboxes_themes).click(function(event) {
        var count_checked_themes = $(selector_checkboxes_themes).filter(':checked').length;
        if (count_checked_themes === 0) {
            $btn_submit.prop('disabled', true);
        } else {
            $btn_submit.prop('disabled', false);
        }
    });
});

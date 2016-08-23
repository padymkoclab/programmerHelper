(function() {
  // btn for submit signal to make a report
  var $btn_submit_make_report_polls = django.jQuery('#btn_submit_make_report_polls');

  // a handler on change value all checkboxes for selecting subjects of the report

  django.jQuery('#table_radio_group_select_report input:checkbox').change(function() {
    console.log(1);
    alert();
    // check up count selected subjects
    var count_checked_subjects = $('#table_radio_group_select_report input:checkbox:checked').length;

    // if any subjects is not selected, then disabled btn for generation the report
    if (count_checked_subjects === 0) {
      $btn_submit_make_report_polls.attr('disabled', true);
    } else {
      $btn_submit_make_report_polls.attr('disabled', false);
    }
  });

  django.jQuery('#tita').click(function(event) {
    console.log('I am worked')
  });
}(django.jQuery));

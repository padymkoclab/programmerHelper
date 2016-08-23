
QUnit.module("apps.polls.admin.reports");

QUnit.test("Checked single a checkbox and a button is active", function(assert) {
  var $btn_submit_make_report_polls = django.jQuery('#btn_submit_make_report_polls');

  assert.equal(
        django.jQuery('#table_radio_group_select_report input:checkbox').filter(':checked').length,
        1, 'Checked a single checkbox'
    );

  assert.equal(django.jQuery('#btn_submit_make_report_polls').attr('disabled'), undefined);
});

QUnit.test("Checked all checkboxes and a button is active", function(assert) {
  var $btn_submit_make_report_polls = django.jQuery('#btn_submit_make_report_polls');
  django.jQuery('#table_radio_group_select_report input:checkbox')[3].click();
  django.jQuery('#table_radio_group_select_report input:checkbox').click();

  assert.equal(
        django.jQuery('#table_radio_group_select_report input:checkbox').filter(':checked').length,
        5, 'Checked a all checkboxes'
    );

  assert.equal(django.jQuery('#btn_submit_make_report_polls').attr('disabled'), undefined);
});

QUnit.test("Checked no-one checkboxes and a button is disabled", function(assert) {
  django.jQuery('#table_radio_group_select_report input:checkbox')[3].click();

  assert.equal(
        django.jQuery('#table_radio_group_select_report input:checkbox').filter(':checked').length,
        0, 'No checked checkboxes'
    );

  assert.equal(django.jQuery('#btn_submit_make_report_polls').attr('disabled'), 'disabled');
});

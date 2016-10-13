(function($, _){

    ValueError = function(msg){
        this.msg = (msg || '');
        this.name = "ValueError";
        this.stack = (new Error()).stack;
    }

    ValueError.prototype = new Error();
    ValueError.prototype.constructor = ValueError;

    $('.btn.open_all_panels').bind({
        click: function(){
            var $panels = $(this).parents('.tab-pane').find('.object_panel');
            var $collapsed_panels = $panels.find('.panel-collapse').filter(function(){
                var is_opened = $(this).hasClass('in');
                return is_opened ? false : true
            });
            $collapsed_panels.parent().find('.panel-heading a').trigger('click');
        },
    });

    $('.btn.collapse_all_panels').bind({
        click: function(){
            var $panels = $(this).parents('.tab-pane').find('.object_panel');
            var $opened_panels = $panels.find('.panel-collapse').filter(function(){
                return $(this).hasClass('in')
            });
            $opened_panels.parent().find('.panel-heading a').trigger('click');
        },
    });

    var change_count_total_form = function($input_total_forms, action){

        if (['added', 'deleted'].indexOf(action) === -1){
            throw new ValueError('Not suppoted value for action.')
        }

        var current_count_total_forms = $input_total_forms.val();
        current_count_total_forms = parseInt(current_count_total_forms);

        if (action === 'added'){
            current_count_total_forms++;
        } else if (action === 'deleted'){
            current_count_total_forms--;
        }

        $input_total_forms.val(current_count_total_forms);

        verify_toggle_link_add_another($input_total_forms, current_count_total_forms);
    }

    var verify_toggle_link_add_another = function($input_total_forms, current_count_total_forms){
        var max_count_forms = $input_total_forms.nextAll('input[name$="MAX_NUM_FORMS"]').val();
        max_count_forms = parseInt(max_count_forms);

        var $btn_add_another = $input_total_forms.parent().find('a.btn_add_another');

        if (max_count_forms <= current_count_total_forms){
            $btn_add_another.addClass('hidden');
        } else {
            $btn_add_another.removeClass('hidden');
        }

    };

    $('.btn_add_another').on({
        click: function(e){

            e.preventDefault();
            e.stopPropagation();

            var $current_fieldset = $(this).parents('.tab-pane');
            var $empty_form = $current_fieldset.find('.empty_form');
            var empty_form_id = $empty_form.find('.panel-collapse').attr('id');

            var $new_empty_form = $empty_form.clone();

            var $current_panel_group = $current_fieldset.find('.panel-group');

            var current_panel_group_id = $current_panel_group.attr('id');

            // all panels except a panel with this empty form
            var $panels = $current_panel_group.find('.panel-collapse').filter(function() {
                return $(this).attr('id').match(/\d+$/)
            });

            if ($panels.length > 0){
                var ids_panels = $panels.map(function() {
                    return $(this).attr('id')
                });
            }

            var ending_numbers_ids_panels = ids_panels.map(function(){
                var array = this.split('-');
                var last_el = array.pop();
                return last_el
            });

            var max_number_panel = Math.max.apply(null, ending_numbers_ids_panels);
            var new_empty_form_id = max_number_panel + 1;

            $new_empty_form.removeClass('hidden');
            $new_empty_form.removeClass('empty_form');

            var new_empty_form_html = $new_empty_form[0].outerHTML.replace(/__prefix__/g, new_empty_form_id)

            $current_panel_group.append(new_empty_form_html);

            var $input_total_forms = $(this).parents('.tab-inline').find('input[id$="TOTAL_FORMS"]')
            change_count_total_form($input_total_forms, 'added');

            var is_open = $new_empty_form.find('div.panel-collapse.collapse').hasClass('in');
            if (!is_open){

                $current_panel_group.find(
                    _.template('a[href="#<%= id1 %>-<%= id2 %>"]')({
                        id1: current_panel_group_id,
                        id2: new_empty_form_id,
                    })
                ).click();
            }
        },
    });

    $('.tab-inline').on('click', '.icon_close_inline_form', function(){
        $(this).parents('.panel').remove();

        var formset_id = $(this).parents('div.panel').find('a[data-toggle="collapse"]').attr('data-parent');
        var $input_total_forms = $(
            _.template('input[name="<%= id %>-TOTAL_FORMS"]')({id: formset_id})
        );

        change_count_total_form($input_total_forms, 'deleted');
    });

})(jQuery, _);

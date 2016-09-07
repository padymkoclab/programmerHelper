
from django.template.loader import get_template
from django.http import HttpResponse

from utils.django.test_utils import EnhancedTestCase

from apps.opinions.admin import OpinionGenericInline
from apps.comments.admin import CommentGenericInline

from apps.utilities.admin import UtilityCategoryAdmin, UtilityInline, UtilityAdmin
from apps.utilities.models import UtilityCategory, Utility


class UtilityCategoryAdminTest(EnhancedTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.call_command('factory_test_superusers', '1')
        cls.call_command('factory_test_categories_utilities', '3')

        cls.admin_model = UtilityCategoryAdmin(UtilityCategory, cls.admin_site)

        cls.superuser = cls.django_user_model._default_manager.first()
        cls.first_category = UtilityCategory.objects.first()

    def test_admin_url_changelist(self):

        url = self.reverse('admin:utilities_utilitycategory_changelist')
        self.client.force_login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_url_add(self):

        url = self.reverse('admin:utilities_utilitycategory_add')
        self.client.force_login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_url_change(self):

        url = self.reverse('admin:utilities_utilitycategory_change', args=(self.first_category.pk, ))
        self.client.force_login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_url_delete(self):

        url = self.reverse('admin:utilities_utilitycategory_delete', args=(self.first_category.pk, ))
        self.client.force_login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_queryset_presents_annotated_fields(self):

        qs = self.admin_model.get_queryset(self.mockrequest)
        qs.values('total_mark', 'total_count_opinions', 'total_count_comments')

    def test_get_fieldsets_if_obj_does_not_exists(self):

        self.assertListEqual(
            self.admin_model.get_fieldsets(self.mockrequest),
            [
                [
                    'Category of utilities', {
                        'fields': [
                            'name',
                            'slug',
                            'description',
                            'image',
                        ]
                    }
                ]
            ]
        )

    def test_get_fieldsets_if_obj_does_exists(self):

        self.assertListEqual(
            self.admin_model.get_fieldsets(self.mockrequest, self.first_category),
            [
                [
                    'Category of utilities', {
                        'fields': [
                            'name',
                            'slug',
                            'description',
                            'image',
                        ]
                    }
                ],
                [
                    'Additional information', {
                        'classes': ('collapse', ),
                        'fields': [
                            'get_total_mark',
                            'get_total_count_opinions',
                            'get_total_count_comments',
                            'get_count_utilities',
                            'date_modified',
                            'date_added',
                        ]
                    }
                ]
            ]
        )

    def test_get_inline_instances_if_obj_does_not_exists(self):

        self.assertListEqual(self.admin_model.get_inline_instances(self.mockrequest), [])

    def test_get_inline_instances_if_obj_does_exists(self):

        inlines = self.admin_model.get_inline_instances(self.mockrequest, self.first_category)
        self.assertEqual(len(inlines), 1)
        self.assertIsInstance(inlines[0], UtilityInline)

    def test_truncated_name_if_category_has_name_with_length_more_80_characters(self):

        self.first_category.name = "Harum est tempore neque suscipit eius ad perspiciatis autem et, corru. In aperiam"
        self.first_category.full_clean()
        self.first_category.save()

        url = self.reverse('admin:utilities_utilitycategory_change', args=(self.first_category.pk, ))
        self.client.force_login(self.superuser)
        response = self.client.get(url)

        self.assertContains(
            response,
            '<li class="active">' +
            'Harum est tempore neque suscipit eius ad perspiciatis autem et, corru. In ape...' +
            '</li>',
            count=1, status_code=200, html=True
        )

    def test_truncated_name_if_category_has_name_with_length_80_characters(self):

        self.first_category.name = "Harum est tempore neque suscipit eius ad perspiciatis autem et, corru. In aperia"
        self.first_category.full_clean()
        self.first_category.save()

        url = self.reverse('admin:utilities_utilitycategory_change', args=(self.first_category.pk, ))
        self.client.force_login(self.superuser)
        response = self.client.get(url)

        self.assertContains(
            response,
            '<li class="active">' +
            'Harum est tempore neque suscipit eius ad perspiciatis autem et, corru. In aperia' +
            '</li>',
            count=1, status_code=200, html=True
        )

    def test_truncated_name_if_category_has_name_with_length_less_80_characters(self):

        self.first_category.name = "Harum est tempore neque suscipit eius ad perspiciatis autem et, corru. In aperi"
        self.first_category.full_clean()
        self.first_category.save()

        url = self.reverse('admin:utilities_utilitycategory_change', args=(self.first_category.pk, ))
        self.client.force_login(self.superuser)
        response = self.client.get(url)

        self.assertContains(
            response,
            '<li class="active">' +
            'Harum est tempore neque suscipit eius ad perspiciatis autem et, corru. In aperi' +
            '</li>',
            count=1, status_code=200, html=True
        )


class UtilityAdminTest(EnhancedTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.call_command('factory_test_users', '10')
        cls.call_command('factory_test_categories_utilities', '3')
        cls.call_command('factory_test_utilities', '3')

        cls.admin_model = UtilityAdmin(Utility, cls.admin_site)

        cls.superuser = cls.django_user_model._default_manager.first()
        cls._make_user_as_active_superuser(cls.superuser)

        cls.first_utility = Utility.objects.first()

    def test_admin_url_changelist(self):

        url = self.reverse('admin:utilities_utility_changelist')
        self.client.force_login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_url_add(self):

        url = self.reverse('admin:utilities_utility_add')
        self.client.force_login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_url_change(self):

        url = self.reverse('admin:utilities_utility_change', args=(self.first_utility.pk, ))
        self.client.force_login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_url_delete(self):

        url = self.reverse('admin:utilities_utility_delete', args=(self.first_utility.pk, ))
        self.client.force_login(self.superuser)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_queryset_presents_annotated_fields(self):

        qs = self.admin_model.get_queryset(self.mockrequest)
        qs.values('mark', 'count_opinions', 'count_comments')

    def test_get_fieldsets_if_obj_does_not_exists(self):

        self.assertListEqual(
            self.admin_model.get_fieldsets(self.mockrequest),
            [
                [
                    'Utility', {
                        'fields': [
                            'name',
                            'description',
                            'category',
                            'web_link',
                        ]
                    }
                ]
            ]
        )

    def test_get_fieldsets_if_obj_does_exists(self):

        self.assertListEqual(
            self.admin_model.get_fieldsets(self.mockrequest, self.first_utility),
            [
                [
                    'Utility', {
                        'fields': [
                            'name',
                            'description',
                            'category',
                            'web_link',
                        ]
                    }
                ],
                [
                    'Additional information', {
                        'classes': ('collapse', ),
                        'fields': [
                            'get_mark',
                            'get_count_comments',
                            'get_count_opinions',
                            'date_modified',
                            'date_added',
                        ]
                    }
                ]
            ]
        )

    def test_get_inline_instances_if_obj_does_not_exists(self):

        self.assertListEqual(self.admin_model.get_inline_instances(self.mockrequest), [])

    def test_get_inline_instances_if_obj_does_exists(self):

        inlines = self.admin_model.get_inline_instances(self.mockrequest, self.first_utility)
        self.assertEqual(len(inlines), 2)
        self.assertIsInstance(inlines[0], OpinionGenericInline)
        self.assertIsInstance(inlines[1], CommentGenericInline)

    def test_truncated_name_if_utility_has_length_of_name_less_50_characters(self):

        self.first_utility.name = 'Dolor molestias accusantium at adipisci sit facer'
        self.first_utility.full_clean()
        self.first_utility.save()

        self.assertEqual(
            self.admin_model.truncated_name(self.first_utility),
            'Dolor molestias accusantium at adipisci sit facer'
        )

    def test_truncated_name_if_utility_has_length_of_name_equal_50_characters(self):

        self.first_utility.name = 'Dolor molestias accusantium at adipisci sit facere'
        self.first_utility.full_clean()
        self.first_utility.save()

        self.assertEqual(
            self.admin_model.truncated_name(self.first_utility),
            'Dolor molestias accusantium at adipisci sit facere'
        )

    def test_truncated_name_if_utility_has_length_of_name_more_50_characters(self):

        self.first_utility.name = 'Dolor molestias accusantium at adipisci sit facere odio minima velit aliasv'
        self.first_utility.full_clean()
        self.first_utility.save()

        self.assertEqual(
            self.admin_model.truncated_name(self.first_utility),
            'Dolor molestias accusantium at adipisci sit fac...'
        )

    def test_truncated_name_if_utility_has_name_with_length_more_80_characters(self):

        self.first_utility.name = "Asserts that a Response instance produced the given status_code and that text has"
        self.first_utility.full_clean()
        self.first_utility.save()

        url = self.reverse('admin:utilities_utility_change', args=(self.first_utility.pk, ))
        self.client.force_login(self.superuser)
        response = self.client.get(url)

        self.assertContains(
            response,
            '<li class="active">' +
            'Asserts that a Response instance produced the given status_code and that text...' +
            '</li>',
            count=1, status_code=200, html=True
        )

    def test_truncated_name_if_utility_has_name_with_length_80_characters(self):

        self.first_utility.name = "Asserts that a Response instance produced the given status_code and that text ha"
        self.first_utility.full_clean()
        self.first_utility.save()

        url = self.reverse('admin:utilities_utility_change', args=(self.first_utility.pk, ))
        self.client.force_login(self.superuser)
        response = self.client.get(url)

        self.assertContains(
            response,
            '<li class="active">' +
            'Asserts that a Response instance produced the given status_code and that text ha' +
            '</li>',
            count=1, status_code=200, html=True
        )

    def test_truncated_name_if_utility_has_name_with_length_less_80_characters(self):

        self.first_utility.name = "Asserts that a Response instance produced the given status_code and that text h"
        self.first_utility.full_clean()
        self.first_utility.save()

        url = self.reverse('admin:utilities_utility_change', args=(self.first_utility.pk, ))
        self.client.force_login(self.superuser)
        response = self.client.get(url)

        self.assertContains(
            response,
            '<li class="active">' +
            'Asserts that a Response instance produced the given status_code and that text h' +
            '</li>',
            count=1, status_code=200, html=True
        )


class UtilityInlineTests(EnhancedTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.FakeInlineAdminForm = type('FakeInlineAdminForm', (tuple, ), {})

    def test_truncated_name_in_inline_template_if_length_name_is_more_80_characters(self):

        self.FakeInlineAdminForm.original =\
            'Dots have a special meaning in template rendering. A dot in a variable name signi'

        template = get_template(UtilityInline.template)

        html = template.render({'inline_admin_formset': [self.FakeInlineAdminForm]})

        response = HttpResponse(html)
        self.assertContains(
            response,
            '<span class="inline_label">' +
            'Dots have a special meaning in template rendering. A dot in a variable name s...' +
            '</span>',
            count=1, html=True
        )

    def test_truncated_name_in_inline_template_if_length_name_is_equal_80_characters(self):

        self.FakeInlineAdminForm.original =\
            'Dots have a special meaning in template rendering. A dot in a variable name sign'

        template = get_template(UtilityInline.template)

        html = template.render({'inline_admin_formset': [self.FakeInlineAdminForm]})

        response = HttpResponse(html)
        self.assertContains(
            response,
            '<span class="inline_label">' +
            'Dots have a special meaning in template rendering. A dot in a variable name sign' +
            '</span>',
            count=1, html=True
        )

    def test_truncated_name_in_inline_template_if_length_name_is_less_80_characters(self):

        self.FakeInlineAdminForm.original =\
            'Dots have a special meaning in template rendering. A dot in a variable name sig'

        template = get_template(UtilityInline.template)

        html = template.render({'inline_admin_formset': [self.FakeInlineAdminForm]})

        response = HttpResponse(html)
        self.assertContains(
            response,
            '<span class="inline_label">' +
            'Dots have a special meaning in template rendering. A dot in a variable name sig' +
            '</span>',
            count=1, html=True
        )


from mylabour.test_utils import EnhancedTestCase

from apps.opinions.admin import OpinionGenericInline
from apps.comments.admin import CommentGenericInline

from apps.utilities.admin import UtilityCategoryAdmin, UtilityInline, UtilityAdmin
from apps.utilities.models import UtilityCategory, Utility


class UtilityCategoryAdminTest(EnhancedTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.call_command('factory_test_categories_utilities', '3')

        cls.admin_model = UtilityCategoryAdmin(UtilityCategory, cls.admin_site)

        cls.first_category = UtilityCategory.objects.first()

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


class UtilityAdminTest(EnhancedTestCase):

    @classmethod
    def setUpTestData(cls):

        cls.call_command('factory_test_users', '10')
        cls.call_command('factory_test_categories_utilities', '3')
        cls.call_command('factory_test_utilities', '3')

        cls.admin_model = UtilityAdmin(Utility, cls.admin_site)

        cls.first_utility = Utility.objects.first()

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

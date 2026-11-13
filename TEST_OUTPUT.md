# Test Output

Command: `python manage.py test -v 2`  (Python 3.12.3, Django 6.1.3, DRF 3.18.3)

```
Found 25 test(s).
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: messages, rest_framework, staticfiles
  Apply all migrations: admin, auth, contenttypes, sessions, shipping
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying shipping.0001_initial... OK
System check identified no issues (0 silenced).
test_duplicate_lines_are_merged (shipping.tests.test_api.ApiTests.test_duplicate_lines_are_merged) ... ok
test_empty_items_is_400 (shipping.tests.test_api.ApiTests.test_empty_items_is_400) ... ok
test_inactive_box_ignored (shipping.tests.test_api.ApiTests.test_inactive_box_ignored) ... ok
test_larger_order_needs_large_box (shipping.tests.test_api.ApiTests.test_larger_order_needs_large_box) ... ok
test_negative_dimension_rejected_on_create (shipping.tests.test_api.ApiTests.test_negative_dimension_rejected_on_create) ... ok
test_no_box_fits_response (shipping.tests.test_api.ApiTests.test_no_box_fits_response) ... ok
test_quantity_zero_is_400 (shipping.tests.test_api.ApiTests.test_quantity_zero_is_400) ... ok
test_recommend_small_box_for_mug (shipping.tests.test_api.ApiTests.test_recommend_small_box_for_mug) ... ok
test_saved_order_recommendation (shipping.tests.test_api.ApiTests.test_saved_order_recommendation) ... ok
test_unknown_product_is_400 (shipping.tests.test_api.ApiTests.test_unknown_product_is_400) ... ok
test_exact_fit (shipping.tests.test_packing.ItemFitTests.test_exact_fit) ... ok
test_fits_only_after_rotation (shipping.tests.test_packing.ItemFitTests.test_fits_only_after_rotation) ... ok
test_too_big_in_one_dimension (shipping.tests.test_packing.ItemFitTests.test_too_big_in_one_dimension) ... ok
test_eight_cubes_fill_cube_box (shipping.tests.test_packing.PackingTests.test_eight_cubes_fill_cube_box) ... ok
test_mixed_sizes (shipping.tests.test_packing.PackingTests.test_mixed_sizes) ... ok
test_nine_cubes_do_not_fit_cube_box (shipping.tests.test_packing.PackingTests.test_nine_cubes_do_not_fit_cube_box) ... ok
test_two_items_that_each_fit_but_not_together (shipping.tests.test_packing.PackingTests.test_two_items_that_each_fit_but_not_together) ... ok
test_empty_order_raises (shipping.tests.test_packing.RecommendTests.test_empty_order_raises) ... ok
test_equal_cost_prefers_smaller_volume (shipping.tests.test_packing.RecommendTests.test_equal_cost_prefers_smaller_volume) ... ok
test_no_box_fits (shipping.tests.test_packing.RecommendTests.test_no_box_fits) ... ok
test_picks_cheapest_fitting_box (shipping.tests.test_packing.RecommendTests.test_picks_cheapest_fitting_box) ... ok
test_quantity_expands_units_and_weight (shipping.tests.test_packing.RecommendTests.test_quantity_expands_units_and_weight) ... ok
test_too_many_units_guard (shipping.tests.test_packing.RecommendTests.test_too_many_units_guard) ... ok
test_volume_too_high_rejects_box (shipping.tests.test_packing.RecommendTests.test_volume_too_high_rejects_box) ... ok
test_weight_too_high_rejects_box (shipping.tests.test_packing.RecommendTests.test_weight_too_high_rejects_box) ... ok

----------------------------------------------------------------------
Ran 25 tests in 0.037s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
```

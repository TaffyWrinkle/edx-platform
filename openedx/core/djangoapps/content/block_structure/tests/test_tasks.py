"""
Unit tests for the Course Blocks tasks
"""

from mock import patch

from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase

from ..tasks import update_course_in_cache


class UpdateCourseInCacheTaskTest(ModuleStoreTestCase):
    """
    Ensures that the update_course_in_cache task runs as expected.
    """
    @patch('openedx.core.djangoapps.content.block_structure.tasks.update_course_in_cache.retry')
    @patch('openedx.core.djangoapps.content.block_structure.api.update_course_in_cache')
    def test_retry_on_error(self, mock_update, mock_retry):
        """
        Ensures that tasks will be retried if IntegrityErrors are encountered.
        """
        mock_update.side_effect = Exception("WHAMMY")
        update_course_in_cache.apply(args=["invalid_course_key raises exception 12345 meow"])
        self.assertTrue(mock_retry.called)

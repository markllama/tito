#
# Copyright (c) 2008-2009 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#
# Red Hat trademarks are not licensed under GPLv2. No permission is
# granted to use or replicate Red Hat trademarks that are incorporated
# in this software or its documentation.

"""Unit tests for tagger module"""

import unittest

BUILDCONFIG_SECTION = "buildconfig"

import tito.tagger

class TestConfig():

    def __init__(self):
        self._options = {
            BUILDCONFIG_SECTION: {
                'tag_suffix': "mytagsuffix"
            }
        }

    def sections(self):
        return []

    def has_option(self, sect_id, opt_name):
        return sect_id in self._options and opt_name in self._options[sect_id]

    def get(self, sect_id, opt_name):
        return self._options[sect_id][opt_name]

class TaggerTest(unittest.TestCase):

    def setUp(self):
        config = TestConfig()
        self.tagger = tito.tagger.VersionTagger(config)
        self.tagger.project_name = "myproject"
        
    def test_get_new_tag(self):

        input = "3.2.1-1"
        expected = "myproject-3.2.1mytagsuffix-1"
        actual = self.tagger._get_new_tag(input)
        self.assertEqual(actual, expected)

    def test_get_suffixed_version(self):

        input = 'hello'
        expected = 'hellomytagsuffix'
        actual = self.tagger._get_suffixed_version(input)
        self.assertEqual(actual, expected)

    def test_get_version(self):
        # The version part is the next-to-last field split by hyphens
        input = "package-name-3.2.1-a.b.c"
        expected = "3.2.1"

        actual = self.tagger._get_version(input)
        self.assertEqual(actual, expected)

    def test_get_release(self):
        # The release part is the last field split by hyphens
        input = "package-name-3.2.1-a.b.c"
        expected = "a.b.c"

        actual = self.tagger._get_release(input)
        self.assertEqual(actual, expected)

    def test_get_tag_for_version(self):

        input = {
            'version': "3.2.1",
            'release': "1"
        }

        expected = "myproject-3.2.1-1"
        actual = self.tagger._get_tag_for_version(
            input['version'],
            input['release']
        )
        self.assertEquals(expected, actual)

if __name__ == "__main__":
    unittest.main()

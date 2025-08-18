#    p4templates - custom tooling to quickly create Helix Core depot/stream/group/permission setups.
#    Copyright (C) 2024 Perforce Software, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pytest

from p4_scrubber.kernel.permissions import (
    validate_permission,
    find_permissions_by_depot,
    find_permissions_by_stream,
    delete_permission,
    get_protections_table,
    validate_protection,
    save_protections_table,

)


class MockP4(object):
    def __init__(
        self,
    ):
        self.protect = {
            "Protections": ["access type name host path  ## comment", "broken"]
        }

        self.fetch_called = 0
        self.save_called = 0

    def fetch_protect(self):
        self.fetch_called = 1
        return self.protect

    def save_protect(self, protect_spec):
        self.protect = protect_spec
        self.save_called = 1
        return [self.protect]


def test_get_protections_table():
    m_server = MockP4()

    expected_result = [
        {
            "access": "access",
            "type": "type",
            "name": "name",
            "host": "host",
            "path": "path",
            "comment": "comment",
        }
    ]

    result = get_protections_table(m_server)
    print(result)
    assert result == expected_result


@pytest.mark.parametrize(
    "protection,expected_result",
    [
        (
            {
                "access": "access",
                "type": "type",
                "name": "name",
                "host": "host",
                "path": "path",
                "comment": "comment",
            },
            True,
        ),
        ({"type": "type", "name": "name", "host": "host", "path": "path"}, False),
        ({"access": "access", "name": "name", "host": "host", "path": "path"}, False),
        ({"access": "access", "type": "type", "host": "host", "path": "path"}, False),
        ({"access": "access", "type": "type", "name": "name", "path": "path"}, False),
        ({"access": "access", "type": "type", "name": "name", "host": "host"}, False),
    ],
)
def test_validate_protection(protection, expected_result):
    result = validate_protection(protection)
    assert result == expected_result


@pytest.mark.parametrize(
    "protection_table,dryrun,expected_result",
    [
        (   [
                {
                    "access": "access",
                    "type": "type",
                    "name": "name",
                    "host": "host",
                    "path": "path",
                    "comment": "comment",
                }
            ],
            True,
            {'Protections': ['access type name host path  ## comment', 'broken']}
        ),
        (   [
                {
                    "access": "access",
                    "type": "type",
                    "name": "name",
                    "host": "host",
                    "path": "path",
                    "comment": "comment",
                }
            ],
            False,
            {'Protections': ['access type name host path ## comment']}
        ),
    ]
)
def test_save_protections_table(protection_table, dryrun, expected_result):
    m_server = MockP4()

    save_protections_table(protection_table, m_server, dryrun)

    assert m_server.protect == expected_result

@pytest.mark.parametrize(
    "protection_list,protection,expected_result",
    [
        (
            ['test_protection'],
            'test_protection',
            True
        ),
        (
            ['nope_protection'],
            'test_protection',
            False
        ),
    ]
)
def test_validate_permission(protection_list, protection, expected_result):
   result = validate_permission(protection_list, protection)
   assert result == expected_result


def test_find_permissions_by_depot():
    protection_list = [{'name':'yes', 'path':'//test_depot/...'},{'name': 'no', 'path':'//nope/...'}]
    expected_result = [{'name':'yes', 'path':'//test_depot/...'},]
    
    result = find_permissions_by_depot(protection_list, 'test_depot')
    
    assert result == expected_result


def test_find_permissions_by_stream():
    protection_list = [{'name':'yes', 'path':'//test_depot/main...'},{'name': 'no', 'path':'//nope/main...'}]
    expected_result = [{'name':'yes', 'path':'//test_depot/main...'},]
    
    result = find_permissions_by_stream(protection_list, '//test_depot/main')
    
    assert result == expected_result

def test_delete_permission():
    protection_list = [{'name':'yes'},{'name': 'no'}]
    expected_result = [{'name':'no'},]
    
    result = delete_permission(protection_list, {'name':'yes'})
    
    assert result == expected_result
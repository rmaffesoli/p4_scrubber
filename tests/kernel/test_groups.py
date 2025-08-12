#!/usr/bin/env python
#
#    p4_scrubber - custom tooling to quickly delete Helix Core depot/stream/group/permission setups.
#    Copyright (C) 2025 Perforce Software, Inc.
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

from p4_scrubber.kernel.groups import validate_group, delete_group

class MockP4(object):
    def __init__(self, ):
        self.group = {
            'Group': 'Existing',
            'Description': None,
            'MaxResults': None,
            'MaxScanRows': None,
            'MaxLockTime': None,
            'MaxOpenFiles': None,
            'MaxMemory': None,
            'Timeout': None,
            'PasswordTimeout': None,
            'Subgroups': None,
            'Owners': None,
            'Users': None,
        }


        self.run_args = ()
        self.iterate_called = 0
        self.run_called = 0

    def iterate_groups(self):
        self.iterate_called = 1
        return [self.group]

    def run(self, *args):
        self.run_called = 1
        self.run_args = args
        return [True]


@pytest.mark.parametrize(
    'group_name,iterate_called,expected_result',
    [
        ('Existing', 1, True),
        ('no_group', 1, False),
    ]
)
def test_validate_group(group_name, iterate_called, expected_result):
    m_server = MockP4()

    result = validate_group(m_server, group_name)

    assert result == expected_result
    assert m_server.iterate_called == iterate_called


@pytest.mark.parametrize(
    'group_name,dryrun,run_called,expected_run_args,expected_result',
    [
        ('Existing', 1, False, (), 'would have deleted group, Existing'),
        ('Existing', 0, True, ('group', '-d', '-F', 'Existing'), True),
    ]
)
def test_delete_group(group_name, dryrun, run_called, expected_run_args, expected_result):
    m_server = MockP4()

    result = delete_group(m_server, group_name, dryrun)

    assert result == expected_result
    assert m_server.run_args == expected_run_args
    assert m_server.run_called == run_called
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

from p4_scrubber.kernel.shelves import validate_shelve, find_shelves_by_user, find_shelves_by_client, delete_shelf


class MockP4(object):
    def __init__(self):
        self.shelves = {
            'change': '1',
        }

        self.run_args = ()
        self.run_called = 0

    def run(self, *args):
        self.run_called = 1
        self.run_args = args
        return [self.shelves]


@pytest.mark.parametrize(
    'client_name,run_called,expected_run_args,expected_result',
    [
        ('1', 1, ('changes', '-s', 'shelved'),True),
        ('2', 1, ('changes', '-s', 'shelved'), False,)
    ]
)
def test_validate_shelve(client_name, run_called, expected_run_args,expected_result):
    m_server = MockP4()

    result = validate_shelve(m_server, client_name)

    assert result == expected_result
    assert m_server.run_called == run_called
    assert m_server.run_args == expected_run_args

@pytest.mark.parametrize(
    'user,expected_run_args,expected_result',
    [
        ('test_user', ('changes', '-u', 'test_user', '-s', 'shelved'), {'1'}),
    ]
)
def test_find_shelves_by_user(user, expected_run_args, expected_result):
    m_server = MockP4()

    result = find_shelves_by_user(m_server, user)

    assert result == expected_result
    assert m_server.run_args == expected_run_args
    assert m_server.run_called == True


@pytest.mark.parametrize(
    'client,expected_run_args,expected_result',
    [
        ('test_client', ('changes', '-c', 'test_client', '-s', 'shelved'), {'1'}),
    ]
)
def test_find_shelves_by_client(client, expected_run_args, expected_result):
    m_server = MockP4()

    result = find_shelves_by_client(m_server, client)

    assert result == expected_result
    assert m_server.run_args == expected_run_args
    assert m_server.run_called == True



@pytest.mark.parametrize(
    'shelf_number,dryrun,run_called,expected_run_args,expected_result',
    [
        ('1', 1, False, (), 'would have deleted shelf, 1'),
        ('1', 0, True, ('shelve', '-f', '-d', '-c', '1', '//...'), {'change': '1'}),
    ]
)
def test_delete_shelf(shelf_number, dryrun, run_called, expected_run_args, expected_result):
    m_server = MockP4()

    result = delete_shelf(m_server, shelf_number, dryrun)

    assert result == expected_result
    assert m_server.run_args == expected_run_args
    assert m_server.run_called == run_called
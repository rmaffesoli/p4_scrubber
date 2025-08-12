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

from p4_scrubber.kernel.scrubber import run_scrubber

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
    'initial_manifest, dryrun, expected_result',
    [
        (
            {
                'users': ['test_user'],
                'depots': ['test_depot'],
                'streams': ['test_stream'],
                'clients': ['test_client'],
                'shelves': ['1'],
                'groups': ['test_group'],
                'permissions': ['test_permission']
            },
            1,
            {
                'users': ['test_user'], 
                'depots': ['test_depot'], 
                'streams': ['depot_stream', 'test_stream'], 
                'clients': ['stream_client', 'test_client', 'user_client'], 
                'shelves': ['1', '2', '3'], 
                'groups': ['test_group'], 
                'permissions': ['depot_permission', 'stream_permission', 'test_permission']
            }
        ),
        (
            {
                'users': ['test_user'],
                'depots': ['test_depot'],
                'streams': ['test_stream'],
                'clients': ['test_client'],
                'shelves': ['1'],
                'groups': ['test_group'],
                'permissions': ['test_permission']
            }, 
            0,             
            {
                'users': ['test_user'], 
                'depots': ['test_depot'], 
                'streams': ['depot_stream', 'test_stream'], 
                'clients': ['stream_client', 'test_client', 'user_client'], 
                'shelves': ['1', '2', '3'], 
                'groups': ['test_group'], 
                'permissions': ['depot_permission', 'stream_permission', 'test_permission']
            }
        )
    ]
)
def test_run_scrubber(mocker, initial_manifest, dryrun, expected_result):
    m_validate_user = mocker.patch("p4_scrubber.kernel.scrubber.validate_user", return_value=True)
    m_find_clients_by_user = mocker.patch("p4_scrubber.kernel.scrubber.find_clients_by_user", return_value={'user_client'})
    m_validate_shelve = mocker.patch("p4_scrubber.kernel.scrubber.validate_shelve", return_value=True)
    m_find_shelves_by_user = mocker.patch("p4_scrubber.kernel.scrubber.find_shelves_by_user", return_value={'2'})
    m_validate_depot = mocker.patch("p4_scrubber.kernel.scrubber.validate_depot", return_value=True)
    m_find_streams_from_depot = mocker.patch("p4_scrubber.kernel.scrubber.find_streams_from_depot", return_value={'depot_stream'})
    m_validate_stream = mocker.patch("p4_scrubber.kernel.scrubber.validate_stream", return_value=True)
    m_find_clients_by_stream = mocker.patch("p4_scrubber.kernel.scrubber.find_clients_by_stream", return_value={'stream_client'})
    m_validate_client = mocker.patch("p4_scrubber.kernel.scrubber.validate_client", return_value=True)
    m_find_shelves_by_client =mocker.patch("p4_scrubber.kernel.scrubber.find_shelves_by_client", return_value={'3'})
    m_get_protections_table = mocker.patch("p4_scrubber.kernel.scrubber.get_protections_table", return_value=['test_permission'])
    m_validate_permission = mocker.patch("p4_scrubber.kernel.scrubber.validate_permission", return_value=True)
    m_find_permissions_by_depot = mocker.patch("p4_scrubber.kernel.scrubber.find_permissions_by_depot", return_value={'depot_permission'})
    m_find_permissions_by_stream = mocker.patch("p4_scrubber.kernel.scrubber.find_permissions_by_stream", return_value={'stream_permission'})
    m_validate_group = mocker.patch("p4_scrubber.kernel.scrubber.validate_group", return_value=True)
    m_delete_shelf = mocker.patch("p4_scrubber.kernel.scrubber.delete_shelf")
    m_delete_client = mocker.patch("p4_scrubber.kernel.scrubber.delete_client")
    m_sort_stream_tiers = mocker.patch("p4_scrubber.kernel.scrubber.sort_stream_tiers", return_value={0:["test_stream", "depot_stream"]})
    m_delete_stream = mocker.patch("p4_scrubber.kernel.scrubber.delete_stream")
    m_delete_depot = mocker.patch("p4_scrubber.kernel.scrubber.delete_depot")
    m_delete_group = mocker.patch("p4_scrubber.kernel.scrubber.delete_group")
    m_delete_user = mocker.patch("p4_scrubber.kernel.scrubber.delete_user")

    m_server = MockP4()
    

    result = run_scrubber(m_server, initial_manifest, dryrun)

    validate_stream_calls = [
        mocker.call(m_server, 'test_stream'),
        mocker.call(m_server, 'depot_stream'),
    ]

    find_clients_by_stream_calls = [
        mocker.call(m_server, 'test_stream'),
        mocker.call(m_server, 'depot_stream'),
    ]

    validate_client_calls = [
        mocker.call(m_server, 'stream_client'),
        mocker.call(m_server, 'test_client'),
        mocker.call(m_server, 'user_client'),
    ]

    find_shelves_by_client_calls = [
        mocker.call(m_server, 'stream_client'),
        mocker.call(m_server, 'test_client'),
        mocker.call(m_server, 'user_client'),
    ]

    find_permissions_by_stream_calls = [
        mocker.call(['test_permission'], 'test_stream'),
        mocker.call(['test_permission'], 'depot_stream'),
    ]

    delete_shelf_calls = [
        mocker.call(m_server,'1', dryrun),
        mocker.call(m_server,'2', dryrun),
        mocker.call(m_server,'3', dryrun),
    ]

    delete_client_calls = [
        mocker.call(m_server, 'stream_client', dryrun),
        mocker.call(m_server, 'test_client', dryrun),
        mocker.call(m_server, 'user_client', dryrun),
    ]

    delete_stream_calls = [
        mocker.call(m_server, 'test_stream', dryrun),
        mocker.call(m_server, 'depot_stream', dryrun),
    ]
    assert result == expected_result
    m_validate_user.assert_called_once_with(m_server, 'test_user')
    m_find_clients_by_user.assert_called_once_with(m_server, 'test_user')
    m_validate_shelve.assert_called_once_with(m_server, '1')
    m_find_shelves_by_user.assert_called_once_with(m_server, 'test_user')
    m_validate_depot.assert_called_once_with(m_server, 'test_depot')
    m_find_streams_from_depot.assert_called_once_with(m_server, 'test_depot')
    m_validate_stream.assert_has_calls(validate_stream_calls, any_order=True)
    m_find_clients_by_stream.assert_has_calls(find_clients_by_stream_calls, any_order=True)
    m_validate_client.assert_has_calls(validate_client_calls, any_order=True)
    m_find_shelves_by_client.assert_has_calls(find_shelves_by_client_calls, any_order=True)
    m_get_protections_table.assert_called_with(m_server)
    m_validate_permission.assert_called_with(['test_permission'], 'test_permission')
    m_find_permissions_by_depot.assert_called_once_with(['test_permission'], 'test_depot')
    m_find_permissions_by_stream.assert_has_calls(find_permissions_by_stream_calls, any_order=True)
    m_validate_group.assert_called_once_with(m_server, 'test_group')
    m_delete_shelf.assert_has_calls(delete_shelf_calls, any_order=True)
    m_delete_client.assert_has_calls(delete_client_calls, any_order=True)
    m_sort_stream_tiers.assert_called_once_with(m_server, ['depot_stream', 'test_stream'])
    m_delete_stream.assert_has_calls(delete_stream_calls, any_order=True)
    m_delete_depot.assert_called_once_with(m_server, 'test_depot', dryrun)
    m_delete_group.assert_called_once_with(m_server, 'test_group', dryrun)
    m_delete_user.assert_called_once_with(m_server, 'test_user', dryrun)
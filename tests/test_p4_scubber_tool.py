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
from p4_scrubber.p4_scrubber_tool import main
from collections import namedtuple

args_tuple = namedtuple('ArgsTuple', ['config', 'manifest', 'yes'])

class MockArgumentParser(object):
    def __init__(self, args_dict=None):
        self.args_dict = args_dict or {}

    def add_argument(
        self, short_name, long_name, default=None, nargs=None, action=None
    ):
        pass

    def parse_args(self):
        return self.args_dict


@pytest.mark.parametrize(
    "given_args,config_values,dir_exists_values,frozen",
    [
        (args_tuple('config', 'manifest', 'yes'), {'server': {'port':'test'}}, [True, True], False),
        (args_tuple('config', 'manifest', 'yes'), {'server': {'port':'test'}}, [True, True], True),
        (args_tuple('config', 'manifest', 'yes'), {'server': {'port':'test'}}, [True, False], False),
        (args_tuple('config', 'manifest', 'yes'), {'server': {'port':'test'}}, [False, False], False),
    ],
)
def test_main(mocker, given_args, config_values, dir_exists_values, frozen):
    m_ArgumentParser = mocker.patch("p4_scrubber.p4_scrubber_tool.ArgumentParser", return_value=MockArgumentParser(given_args))
    m_os_path_exists = mocker.patch("p4_scrubber.p4_scrubber_tool.os.path.exists", side_effect=dir_exists_values)
    m_os_path_abspath = mocker.patch("p4_scrubber.p4_scrubber_tool.os.path.abspath", return_value='abs_path')
    m_load_server_config = mocker.patch("p4_scrubber.p4_scrubber_tool.load_server_config", return_value=config_values)
    m_read_json = mocker.patch("p4_scrubber.p4_scrubber_tool.read_json", return_value={'manifest': 'manifest'})
    m_write_json = mocker.patch("p4_scrubber.p4_scrubber_tool.write_json", return_value={'manifest': 'manifest'})
    m_os_path_dirname = mocker.patch("p4_scrubber.p4_scrubber_tool.os.path.dirname", return_value='a/dir/name/')
    m_os_chdir = mocker.patch("p4_scrubber.p4_scrubber_tool.os.chdir")
    m_run_scrubber = mocker.patch("p4_scrubber.p4_scrubber_tool.run_scrubber", return_value={'updated_manifest': 'updated_manifest'})
    m_setup_server_connection = mocker.patch("p4_scrubber.p4_scrubber_tool.setup_server_connection", return_value='p4_connection')
    if frozen:
        mocker.patch("p4_scrubber.p4_scrubber_tool.getattr", return_value=True)

    main()

    path_exists_calls = [
        mocker.call('abs_path'),
        mocker.call('abs_path')
    ]

    abspath_calls = [
        mocker.call('config'),
        mocker.call('manifest')
    ]

    read_json_calls = [
        mocker.call('config'),
        mocker.call('manifest')
    ]

    m_ArgumentParser.assert_called_once()
    m_os_path_abspath.assert_has_calls(abspath_calls, any_order=True)
    if dir_exists_values[0] and dir_exists_values[1]:
        m_os_path_exists.assert_has_calls(path_exists_calls, any_order=True)
        m_load_server_config.assert_called_once_with('abs_path')
        m_setup_server_connection.assert_called_once_with(port='test')
        m_read_json.asset_has_calls(read_json_calls, any_order=True)
        m_write_json.assert_called_once_with({'updated_manifest': 'updated_manifest'}, 'abs_path')
        
        m_run_scrubber.assert_called_once_with('p4_connection', {'manifest':'manifest'}, 0)
    elif not dir_exists_values[0] or dir_exists_values[1]:
        m_os_path_exists.assert_called_once_with('abs_path')
        m_load_server_config.assert_not_called()
    
    m_os_path_dirname.assert_called()
    m_os_chdir.assert_called_once()


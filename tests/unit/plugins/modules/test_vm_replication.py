# -*- coding: utf-8 -*-
# # Copyright: (c) 2022, XLAB Steampunk <steampunk@xlab.si>
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import sys

import pytest

from ansible_collections.scale_computing.hypercore.plugins.modules import (
    vm_replication,
)

pytestmark = pytest.mark.skipif(
    sys.version_info < (2, 7), reason="requires python2.7 or higher"
)


class TestEnabledOrReenabled:
    def test_ensure_enabled_or_reenabled_when_replication_not_exist(
        self, rest_client, create_module
    ):
        vm_dict = {
            "uuid": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "name": "XLAB_test_vm",
            "blockDevs": [],
            "netDevs": [],
            "stats": "bla",
            "tags": "XLAB,test",
            "description": "test vm",
            "mem": 23424234,
            "state": "RUNNING",
            "numVCPU": 2,
            "bootDevices": [],
            "operatingSystem": "windows",
        }
        replication_dict = {
            "uuid": "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab",
            "sourceDomainUUID": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "enable": True,
            "connectionUUID": "7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",
        }
        module = create_module(
            params=dict(
                cluster_instance=dict(
                    host="https://0.0.0.0",
                    username="admin",
                    password="admin",
                ),
                vm_name="XLAB_test_vm",
                remote_cluster="7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",  # TODO: change to cluster_name when cluster_info is implemented
                state="enabled",
            )
        )
        after = {
            "vm_name": "XLAB_test_vm",
            "remote_cluster": "7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",
            "state": "enabled",
        }
        rest_client.list_records.side_effect = [[vm_dict], [], [replication_dict]]
        rest_client.create_record.return_value = {"taskTag": "1234"}
        results = vm_replication.ensure_enabled_or_reenabled(module, rest_client)
        assert results == (True, after, {"before": None, "after": after})

    def test_ensure_enabled_or_reenabled_when_replication_exists_change_state(
        self, rest_client, create_module
    ):
        vm_dict = {
            "uuid": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "name": "XLAB_test_vm",
            "blockDevs": [],
            "netDevs": [],
            "stats": "bla",
            "tags": "XLAB,test",
            "description": "test vm",
            "mem": 23424234,
            "state": "RUNNING",
            "numVCPU": 2,
            "bootDevices": [],
            "operatingSystem": "windows",
        }
        replication_dict = {
            "uuid": "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab",
            "sourceDomainUUID": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "enable": False,
            "connectionUUID": "7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",
        }
        replication_dict_after = {
            "uuid": "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab",
            "sourceDomainUUID": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "enable": True,
            "connectionUUID": "7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",
        }
        after = {
            "vm_name": "XLAB_test_vm",
            "remote_cluster": "7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",
            "state": "enabled",
        }
        before = {
            "vm_name": "XLAB_test_vm",
            "remote_cluster": "7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",
            "state": "disabled",
        }
        module = create_module(
            params=dict(
                cluster_instance=dict(
                    host="https://0.0.0.0",
                    username="admin",
                    password="admin",
                ),
                vm_name="XLAB_test_vm",
                remote_cluster="7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",  # TODO: change to cluster_name when cluster_info is implemented
                state="enabled",
            )
        )
        rest_client.list_records.side_effect = [
            [vm_dict],
            [replication_dict],
            [replication_dict_after],
        ]
        rest_client.update_record.return_value = {"taskTag": "1234"}
        results = vm_replication.ensure_enabled_or_reenabled(module, rest_client)
        assert results == (True, after, {"before": before, "after": after})

    def test_ensure_enabled_or_reenabled_when_replication_exists_no_changes(
        self, rest_client, create_module
    ):
        vm_dict = {
            "uuid": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "name": "XLAB_test_vm",
            "blockDevs": [],
            "netDevs": [],
            "stats": "bla",
            "tags": "XLAB,test",
            "description": "test vm",
            "mem": 23424234,
            "state": "RUNNING",
            "numVCPU": 2,
            "bootDevices": [],
            "operatingSystem": "windows",
        }
        replication_dict = {
            "uuid": "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab",
            "sourceDomainUUID": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "enable": True,
            "connectionUUID": "7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",
        }
        module = create_module(
            params=dict(
                cluster_instance=dict(
                    host="https://0.0.0.0",
                    username="admin",
                    password="admin",
                ),
                vm_name="XLAB_test_vm",
                remote_cluster="7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",  # TODO: change to cluster_name when cluster_info is implemented
                state="enabled",
            )
        )
        rest_client.list_records.side_effect = [[vm_dict], [replication_dict]]
        rest_client.update_record.return_value = {"taskTag": ""}
        results = vm_replication.ensure_enabled_or_reenabled(module, rest_client)
        assert results == (False, None, {"before": None, "after": None})


class TestDisabled:
    def test_ensure_disabled_replication_not_exists(self, rest_client, create_module):
        vm_dict = {
            "uuid": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "name": "XLAB_test_vm",
            "blockDevs": [],
            "netDevs": [],
            "stats": "bla",
            "tags": "XLAB,test",
            "description": "test vm",
            "mem": 23424234,
            "state": "RUNNING",
            "numVCPU": 2,
            "bootDevices": [],
            "operatingSystem": "windows",
        }
        module = create_module(
            params=dict(
                cluster_instance=dict(
                    host="https://0.0.0.0",
                    username="admin",
                    password="admin",
                ),
                vm_name="XLAB_test_vm",
                remote_cluster="7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",  # TODO: change to cluster_name when cluster_info is implemented
                state="enabled",
            )
        )
        rest_client.list_records.side_effect = [[vm_dict], []]
        results = vm_replication.ensure_disabled(module, rest_client)
        assert results == (False, None, {"before": None, "after": None})

    def test_ensure_disabled_replication_exists_state_not_changed(
        self, rest_client, create_module
    ):
        vm_dict = {
            "uuid": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "name": "XLAB_test_vm",
            "blockDevs": [],
            "netDevs": [],
            "stats": "bla",
            "tags": "XLAB,test",
            "description": "test vm",
            "mem": 23424234,
            "state": "RUNNING",
            "numVCPU": 2,
            "bootDevices": [],
            "operatingSystem": "windows",
        }
        replication_dict = {
            "uuid": "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab",
            "sourceDomainUUID": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "enable": False,
            "connectionUUID": "7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",
        }
        module = create_module(
            params=dict(
                cluster_instance=dict(
                    host="https://0.0.0.0",
                    username="admin",
                    password="admin",
                ),
                vm_name="XLAB_test_vm",
                remote_cluster="7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",  # TODO: change to cluster_name when cluster_info is implemented
                state="disabled",
            )
        )
        rest_client.list_records.side_effect = [[vm_dict], [replication_dict]]
        results = vm_replication.ensure_disabled(module, rest_client)
        assert results == (False, None, {"before": None, "after": None})

    def test_ensure_disabled_replication_exists_state_changed(
        self, rest_client, create_module
    ):
        vm_dict = {
            "uuid": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "name": "XLAB_test_vm",
            "blockDevs": [],
            "netDevs": [],
            "stats": "bla",
            "tags": "XLAB,test",
            "description": "test vm",
            "mem": 23424234,
            "state": "RUNNING",
            "numVCPU": 2,
            "bootDevices": [],
            "operatingSystem": "windows",
        }
        replication_dict = {
            "uuid": "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab",
            "sourceDomainUUID": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "enable": True,
            "connectionUUID": "7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",
        }
        replication_dict_after = {
            "uuid": "6756f2hj-6u9a-90ff-6g91-7jeahgf47aab",
            "sourceDomainUUID": "7542f2gg-5f9a-51ff-8a91-8ceahgf47ghg",
            "enable": False,
            "connectionUUID": "7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",
        }
        after = {
            "vm_name": "XLAB_test_vm",
            "remote_cluster": "7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",
            "state": "disabled",
        }
        before = {
            "vm_name": "XLAB_test_vm",
            "remote_cluster": "7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",
            "state": "enabled",
        }
        module = create_module(
            params=dict(
                cluster_instance=dict(
                    host="https://0.0.0.0",
                    username="admin",
                    password="admin",
                ),
                vm_name="XLAB_test_vm",
                remote_cluster="7890f2ab-3r9a-89ff-5k91-3gdahgh47ghg",  # TODO: change to cluster_name when cluster_info is implemented
                state="disabled",
            )
        )
        rest_client.list_records.side_effect = [
            [vm_dict],
            [replication_dict],
            [replication_dict_after],
        ]
        rest_client.update_record.return_value = {"taskTag": "1234"}
        results = vm_replication.ensure_disabled(module, rest_client)
        assert results == (True, after, {"before": before, "after": after})

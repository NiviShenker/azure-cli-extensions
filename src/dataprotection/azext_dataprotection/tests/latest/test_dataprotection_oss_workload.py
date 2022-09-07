# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------
# pylint: disable=line-too-long
# pylint: disable=unused-import

import time
from datetime import datetime
from azure.cli.testsdk import ScenarioTest
from azure.cli.testsdk.scenario_tests import AllowLargeResponse

def setup(test):
    test.kwargs.update({
        "vaultname": "oss-clitest-vault",
        "rgname": "oss-clitest-rg",
        "ossserver": "oss-clitest-server",
        "ossdb": "postgres",
        "ossdbid": "/subscriptions/38304e13-357e-405e-9e9a-220351dcce8c/resourceGroups/oss-clitest-rg/providers/Microsoft.DBforPostgreSQL/servers/oss-clitest-server/databases/postgres",
        "policyid": "/subscriptions/38304e13-357e-405e-9e9a-220351dcce8c/resourceGroups/oss-clitest-rg/providers/Microsoft.DataProtection/backupVaults/oss-clitest-vault/backupPolicies/oss-clitest-policy",
        "secretstoreuri": "https://oss-clitest-keyvault.vault.azure.net/secrets/oss-clitest-secret",
        "keyvaultid":  "/subscriptions/38304e13-357e-405e-9e9a-220351dcce8c/resourceGroups/oss-clitest-rg/providers/Microsoft.KeyVault/vaults/oss-clitest-keyvault"
    })

def configure_backup(test):
    backup_instance_guid = "faec6818-0720-11ec-bd1b-c8f750f92764"
    backup_instance_json = test.cmd('az dataprotection backup-instance initialize --datasource-type AzureDatabaseForPostgreSQL'
                                    ' -l centraluseuap --policy-id "{policyid}" --datasource-id "{ossdbid}" --secret-store-type AzureKeyVault --secret-store-uri "{secretstoreuri}"').get_output_in_json()
    backup_instance_json["backup_instance_name"] = test.kwargs['ossserver'] + "-" + test.kwargs['ossdb'] + "-" + backup_instance_guid
    test.kwargs.update({
        "backup_instance_json": backup_instance_json,
        "backup_instance_name": backup_instance_json["backup_instance_name"]
    })

    # run only in record mode - grant permission
    # test.cmd('az dataprotection backup-instance update-msi-permissions --datasource-type AzureDatabaseForPostgreSQL --permissions-scope Resource -g "{rgname}" --vault-name "{vaultname}" --operation Backup --backup-instance "{backup_instance_json}" --keyvault-id "{keyvaultid}" --yes')

    time.sleep(60)

    test.cmd('az dataprotection backup-instance create -g "{rgname}" --vault-name "{vaultname}" --backup-instance "{backup_instance_json}"')

    backup_instance_res = test.cmd('az dataprotection backup-instance list -g "{rgname}" --vault-name "{vaultname}" --query "[0].properties.protectionStatus"').get_output_in_json()
    protection_status = backup_instance_res["status"]
    while protection_status != "ProtectionConfigured":
        time.sleep(10)
        backup_instance_res = test.cmd('az dataprotection backup-instance list -g "{rgname}" --vault-name "{vaultname}" --query "[0].properties.protectionStatus"').get_output_in_json()
        protection_status = backup_instance_res["status"]

    time.sleep(30)

def update_protection(test):
    test.kwargs.update({
        "newpolicyid": "/subscriptions/38304e13-357e-405e-9e9a-220351dcce8c/resourceGroups/oss-clitest-rg/providers/Microsoft.DataProtection/backupVaults/oss-clitest-vault/backupPolicies/oss-clitest-policy2"
    })
    backup_instance_res = test.cmd('az dataprotection backup-instance update-policy -g "{rgname}" --vault-name "{vaultname}" --backup-instance-name "{backup_instance_name}" --policy-id "{newpolicyid}" --query "properties.protectionStatus"').get_output_in_json()
    protection_status = backup_instance_res["status"]
    while protection_status != "ProtectionConfigured":
        time.sleep(10)
        backup_instance_res = test.cmd('az dataprotection backup-instance list -g "{rgname}" --vault-name "{vaultname}" --query "[0].properties.protectionStatus"').get_output_in_json()
        protection_status = backup_instance_res["status"]

    time.sleep(30)

def stop_resume_protection(test):
    test.cmd('az dataprotection backup-instance stop-protection -n "{backup_instance_name}" -g "{rgname}" --vault-name "{vaultname}"')

    test.cmd('az dataprotection backup-instance show -n "{backup_instance_name}" -g "{rgname}" --vault-name "{vaultname}"',checks=[
        test.check('properties.currentProtectionState','ProtectionStopped')
    ])

    test.cmd('az dataprotection backup-instance resume-protection -n "{backup_instance_name}" -g "{rgname}" --vault-name "{vaultname}"')

    test.cmd('az dataprotection backup-instance show -n "{backup_instance_name}" -g "{rgname}" --vault-name "{vaultname}"',checks=[
        test.check('properties.currentProtectionState','ProtectionConfigured')
    ])

    test.cmd('az dataprotection backup-instance suspend-backup -n "{backup_instance_name}" -g "{rgname}" --vault-name "{vaultname}"')

    test.cmd('az dataprotection backup-instance show -n "{backup_instance_name}" -g "{rgname}" --vault-name "{vaultname}"',checks=[
        test.check('properties.currentProtectionState','BackupsSuspended')
    ])

    test.cmd('az dataprotection backup-instance resume-protection -n "{backup_instance_name}" -g "{rgname}" --vault-name "{vaultname}"')

    test.cmd('az dataprotection backup-instance show -n "{backup_instance_name}" -g "{rgname}" --vault-name "{vaultname}"',checks=[
        test.check('properties.currentProtectionState','ProtectionConfigured')
    ])

def trigger_backup(test):
    response_json = test.cmd('az dataprotection backup-instance adhoc-backup -n "{backup_instance_name}" -g "{rgname}" --vault-name "{vaultname}" --rule-name BackupWeekly --retention-tag-override Weekly').get_output_in_json()
    job_status = None
    test.kwargs.update({"backup_job_id": response_json["jobId"]})
    while job_status != "Completed":
        time.sleep(10)
        job_response = test.cmd('az dataprotection job show --ids "{backup_job_id}"').get_output_in_json()
        job_status = job_response["properties"]["status"]
        if job_status not in ["Completed", "InProgress"]:
            raise Exception("Undefined job status received")

def trigger_restore(test):
    rp_json = test.cmd('az dataprotection recovery-point list --backup-instance-name "{backup_instance_name}" -g "{rgname}" --vault-name "{vaultname}"').get_output_in_json()
    test.kwargs.update({"rp_id": rp_json[0]["name"]})

    timestring = datetime.now().strftime("%d%m%Y_%H%M%S")
    test.kwargs.update({"targetossdbid": test.kwargs["ossdbid"] + "_restore_" + timestring})

    restore_json = test.cmd('az dataprotection backup-instance restore  initialize-for-data-recovery'
                            ' --datasource-type AzureDatabaseForPostgreSQL --restore-location centraluseuap --source-datastore VaultStore '
                            '--recovery-point-id "{rp_id}" --target-resource-id "{targetossdbid}" --secret-store-type AzureKeyVault --secret-store-uri "{secretstoreuri}"').get_output_in_json()
    test.kwargs.update({"restore_request": restore_json})
    test.cmd('az dataprotection backup-instance validate-for-restore -g "{rgname}" --vault-name "{vaultname}" -n "{backup_instance_name}" --restore-request-object "{restore_request}"')

    response_json = test.cmd('az dataprotection backup-instance restore trigger -g "{rgname}" --vault-name "{vaultname}"'
                             ' -n "{backup_instance_name}" --restore-request-object "{restore_request}"').get_output_in_json()
    job_status = None
    test.kwargs.update({"backup_job_id": response_json["jobId"]})
    while job_status != "Completed":
        time.sleep(10)
        job_response = test.cmd('az dataprotection job show --ids "{backup_job_id}"').get_output_in_json()
        job_status = job_response["properties"]["status"]
        if job_status not in ["Completed", "InProgress"]:
            raise Exception("Undefined job status received")

def trigger_restore_as_files(test):
    timestring = datetime.now().strftime("%d%m%Y_%H%M%S")
    test.kwargs.update({
        "targetblobcontainerurl": "https://ossclitestsa.blob.core.windows.net/oss-clitest-blob-container",
        "targetfile": "postgres_restore_" + timestring
    })

    restore_json = test.cmd('az dataprotection backup-instance restore  initialize-for-data-recovery-as-files'
                            ' --datasource-type AzureDatabaseForPostgreSQL --restore-location centraluseuap --source-datastore VaultStore '
                            '--recovery-point-id "{rp_id}" --target-blob-container-url "{targetblobcontainerurl}" --target-file-name "{targetfile}"').get_output_in_json()
    test.kwargs.update({"restore_request": restore_json})
    test.cmd('az dataprotection backup-instance validate-for-restore -g "{rgname}" --vault-name "{vaultname}" -n "{backup_instance_name}" --restore-request-object "{restore_request}"')

    response_json = test.cmd('az dataprotection backup-instance restore trigger -g "{rgname}" --vault-name "{vaultname}"'
                             ' -n "{backup_instance_name}" --restore-request-object "{restore_request}"').get_output_in_json()
    job_status = None
    test.kwargs.update({"backup_job_id": response_json["jobId"]})
    while job_status != "Completed":
        time.sleep(10)
        job_response = test.cmd('az dataprotection job show --ids "{backup_job_id}"').get_output_in_json()
        job_status = job_response["properties"]["status"]
        if job_status not in ["Completed", "InProgress"]:
            raise Exception("Undefined job status received")

def delete_backup(test):
    test.cmd('az dataprotection backup-instance delete -g "{rgname}" --vault-name "{vaultname}" -n "{backup_instance_name}" --yes')

@AllowLargeResponse()
def call_scenario(test):
    setup(test)
    try:
        configure_backup(test)
        update_protection(test)
        stop_resume_protection(test)
        trigger_backup(test)
        trigger_restore(test)
        trigger_restore_as_files(test)
        delete_backup(test)
    except Exception as e:
        raise e

# Test class for Scenario
class DataprotectionScenarioTest(ScenarioTest):
    def __init__(self, *args, **kwargs):
        super(DataprotectionScenarioTest, self).__init__(*args, **kwargs)

    def test_dataprotection_oss(self):
        call_scenario(self)

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
# pylint: disable=too-many-lines

from knack.util import CLIError
from azure.cli.core.util import sdk_no_wait


def dataprotection_backup_vault_show(client,
                                     resource_group_name,
                                     vault_name):
    return client.get(resource_group_name=resource_group_name,
                      vault_name=vault_name)


def dataprotection_backup_vault_create(client,
                                       resource_group_name,
                                       vault_name,
                                       storage_settings,
                                       e_tag=None,
                                       location=None,
                                       tags=None,
                                       type_=None,
                                       alerts_for_all_job_failures=None,
                                       no_wait=False):
    parameters = {}
    parameters['e_tag'] = e_tag
    parameters['location'] = location
    parameters['tags'] = tags
    parameters['identity'] = {}
    parameters['identity']['type'] = type_
    parameters['properties'] = {}
    parameters['properties']['storage_settings'] = storage_settings
    parameters['properties']['azure_monitor_alert_settings'] = {}
    parameters['properties']['azure_monitor_alert_settings']['alerts_for_all_job_failures'] = alerts_for_all_job_failures
    return sdk_no_wait(no_wait,
                       client.begin_create_or_update,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       parameters=parameters)


def dataprotection_backup_vault_update(client,
                                       resource_group_name,
                                       vault_name,
                                       tags=None,
                                       alerts_for_all_job_failures=None,
                                       type_=None,
                                       no_wait=False):
    parameters = {}
    parameters['tags'] = tags
    parameters['azure_monitor_alert_settings'] = {}
    parameters['azure_monitor_alert_settings']['alerts_for_all_job_failures'] = alerts_for_all_job_failures
    parameters['identity'] = {}
    parameters['identity']['type'] = type_
    return sdk_no_wait(no_wait,
                       client.begin_update,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       parameters=parameters)


def dataprotection_backup_vault_delete(client,
                                       resource_group_name,
                                       vault_name):
    return client.delete(resource_group_name=resource_group_name,
                         vault_name=vault_name)


def dataprotection_backup_policy_list(client,
                                      resource_group_name,
                                      vault_name):
    return client.list(resource_group_name=resource_group_name,
                       vault_name=vault_name)


def dataprotection_backup_policy_show(client,
                                      resource_group_name,
                                      vault_name,
                                      backup_policy_name):
    return client.get(resource_group_name=resource_group_name,
                      vault_name=vault_name,
                      backup_policy_name=backup_policy_name)


def dataprotection_backup_policy_create(client,
                                        resource_group_name,
                                        vault_name,
                                        backup_policy_name,
                                        backup_policy=None):
    all_properties = []
    if backup_policy is not None:
        all_properties.append(backup_policy)
    if len(all_properties) > 1:
        raise CLIError('at most one of  backup_policy is needed for properties!')
    properties = all_properties[0] if len(all_properties) == 1 else None
    parameters = {}
    parameters['properties'] = properties
    return client.create_or_update(resource_group_name=resource_group_name,
                                   vault_name=vault_name,
                                   backup_policy_name=backup_policy_name,
                                   parameters=parameters)


def dataprotection_backup_policy_delete(client,
                                        resource_group_name,
                                        vault_name,
                                        backup_policy_name):
    return client.delete(resource_group_name=resource_group_name,
                         vault_name=vault_name,
                         backup_policy_name=backup_policy_name)


def dataprotection_backup_instance_list(client,
                                        resource_group_name,
                                        vault_name):
    return client.list(resource_group_name=resource_group_name,
                       vault_name=vault_name)


def dataprotection_backup_instance_show(client,
                                        resource_group_name,
                                        vault_name,
                                        backup_instance_name):
    return client.get(resource_group_name=resource_group_name,
                      vault_name=vault_name,
                      backup_instance_name=backup_instance_name)


def dataprotection_backup_instance_create(client,
                                          resource_group_name,
                                          vault_name,
                                          backup_instance_name,
                                          tags=None,
                                          friendly_name=None,
                                          data_source_info=None,
                                          data_source_set_info=None,
                                          secret_store_based_auth_credentials=None,
                                          validation_type=None,
                                          object_type=None,
                                          policy_id=None,
                                          policy_parameters=None,
                                          no_wait=False):
    all_datasource_auth_credentials = []
    if secret_store_based_auth_credentials is not None:
        all_datasource_auth_credentials.append(secret_store_based_auth_credentials)
    if len(all_datasource_auth_credentials) > 1:
        raise CLIError('at most one of  secret_store_based_auth_credentials is needed for datasource_auth_credentials!')
    datasource_auth_credentials = all_datasource_auth_credentials[0] if len(all_datasource_auth_credentials) == 1 else \
        None
    parameters = {}
    parameters['tags'] = tags
    parameters['properties'] = {}
    parameters['properties']['friendly_name'] = friendly_name
    parameters['properties']['data_source_info'] = data_source_info
    parameters['properties']['data_source_set_info'] = data_source_set_info
    parameters['properties']['datasource_auth_credentials'] = datasource_auth_credentials
    parameters['properties']['validation_type'] = validation_type
    parameters['properties']['object_type'] = object_type
    parameters['properties']['policy_info'] = {}
    parameters['properties']['policy_info']['policy_id'] = policy_id
    parameters['properties']['policy_info']['policy_parameters'] = policy_parameters
    return sdk_no_wait(no_wait,
                       client.begin_create_or_update,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       backup_instance_name=backup_instance_name,
                       parameters=parameters)


def dataprotection_backup_instance_delete(client,
                                          resource_group_name,
                                          vault_name,
                                          backup_instance_name,
                                          no_wait=False):
    return sdk_no_wait(no_wait,
                       client.begin_delete,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       backup_instance_name=backup_instance_name)


def dataprotection_backup_instance_adhoc_backup(client,
                                                resource_group_name,
                                                vault_name,
                                                backup_instance_name,
                                                rule_name,
                                                retention_tag_override=None,
                                                no_wait=False):
    parameters = {}
    parameters['backup_rule_options'] = {}
    parameters['backup_rule_options']['rule_name'] = rule_name
    parameters['backup_rule_options']['trigger_option'] = {}
    parameters['backup_rule_options']['trigger_option']['retention_tag_override'] = retention_tag_override
    return sdk_no_wait(no_wait,
                       client.begin_adhoc_backup,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       backup_instance_name=backup_instance_name,
                       parameters=parameters)


def dataprotection_backup_instance_restore_trigger(client,
                                                   resource_group_name,
                                                   vault_name,
                                                   backup_instance_name,
                                                   parameters,
                                                   no_wait=False):
    return sdk_no_wait(no_wait,
                       client.begin_trigger_restore,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       backup_instance_name=backup_instance_name,
                       parameters=parameters)


def dataprotection_backup_instance_resume_protection(client,
                                                     resource_group_name,
                                                     vault_name,
                                                     backup_instance_name,
                                                     no_wait=False):
    return sdk_no_wait(no_wait,
                       client.begin_resume_protection,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       backup_instance_name=backup_instance_name)


def dataprotection_backup_instance_stop_protection(client,
                                                   resource_group_name,
                                                   vault_name,
                                                   backup_instance_name,
                                                   no_wait=False):
    return sdk_no_wait(no_wait,
                       client.begin_stop_protection,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       backup_instance_name=backup_instance_name)


def dataprotection_backup_instance_suspend_backup(client,
                                                  resource_group_name,
                                                  vault_name,
                                                  backup_instance_name,
                                                  no_wait=False):
    return sdk_no_wait(no_wait,
                       client.begin_suspend_backups,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       backup_instance_name=backup_instance_name)


def dataprotection_backup_instance_validate_for_backup(client,
                                                       resource_group_name,
                                                       vault_name,
                                                       data_source_info,
                                                       object_type,
                                                       policy_id,
                                                       friendly_name=None,
                                                       data_source_set_info=None,
                                                       secret_store_based_auth_credentials=None,
                                                       validation_type=None,
                                                       policy_parameters=None,
                                                       no_wait=False):
    all_datasource_auth_credentials = []
    if secret_store_based_auth_credentials is not None:
        all_datasource_auth_credentials.append(secret_store_based_auth_credentials)
    if len(all_datasource_auth_credentials) > 1:
        raise CLIError('at most one of  secret_store_based_auth_credentials is needed for datasource_auth_credentials!')
    datasource_auth_credentials = all_datasource_auth_credentials[0] if len(all_datasource_auth_credentials) == 1 else \
        None
    parameters = {}
    parameters['backup_instance'] = {}
    parameters['backup_instance']['friendly_name'] = friendly_name
    parameters['backup_instance']['data_source_info'] = data_source_info
    parameters['backup_instance']['data_source_set_info'] = data_source_set_info
    parameters['backup_instance']['datasource_auth_credentials'] = datasource_auth_credentials
    parameters['backup_instance']['validation_type'] = validation_type
    parameters['backup_instance']['object_type'] = object_type
    parameters['backup_instance']['policy_info'] = {}
    parameters['backup_instance']['policy_info']['policy_id'] = policy_id
    parameters['backup_instance']['policy_info']['policy_parameters'] = policy_parameters
    return sdk_no_wait(no_wait,
                       client.begin_validate_for_backup,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       parameters=parameters)


def dataprotection_backup_instance_validate_for_restore(client,
                                                        resource_group_name,
                                                        vault_name,
                                                        backup_instance_name,
                                                        restore_request_object,
                                                        no_wait=False):
    parameters = {}
    parameters['restore_request_object'] = restore_request_object
    return sdk_no_wait(no_wait,
                       client.begin_validate_for_restore,
                       resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       backup_instance_name=backup_instance_name,
                       parameters=parameters)


def dataprotection_recovery_point_list(client,
                                       resource_group_name,
                                       vault_name,
                                       backup_instance_name,
                                       filter_=None,
                                       skip_token=None):
    return client.list(resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       backup_instance_name=backup_instance_name,
                       filter=filter_,
                       skip_token=skip_token)


def dataprotection_recovery_point_show(client,
                                       resource_group_name,
                                       vault_name,
                                       backup_instance_name,
                                       recovery_point_id):
    return client.get(resource_group_name=resource_group_name,
                      vault_name=vault_name,
                      backup_instance_name=backup_instance_name,
                      recovery_point_id=recovery_point_id)


def dataprotection_job_list(client,
                            resource_group_name,
                            vault_name):
    return client.list(resource_group_name=resource_group_name,
                       vault_name=vault_name)


def dataprotection_job_show(client,
                            resource_group_name,
                            vault_name,
                            job_id):
    return client.get(resource_group_name=resource_group_name,
                      vault_name=vault_name,
                      job_id=job_id)


def dataprotection_restorable_time_range_find(client,
                                              resource_group_name,
                                              vault_name,
                                              backup_instance_name,
                                              source_data_store_type,
                                              start_time=None,
                                              end_time=None):
    parameters = {}
    parameters['source_data_store_type'] = source_data_store_type
    parameters['start_time'] = start_time
    parameters['end_time'] = end_time
    return client.find(resource_group_name=resource_group_name,
                       vault_name=vault_name,
                       backup_instance_name=backup_instance_name,
                       parameters=parameters)


def dataprotection_resource_guard_show(client,
                                       resource_group_name,
                                       resource_guards_name):
    return client.get(resource_group_name=resource_group_name,
                      resource_guards_name=resource_guards_name)


def dataprotection_resource_guard_create(client,
                                         resource_group_name,
                                         resource_guards_name,
                                         e_tag=None,
                                         location=None,
                                         tags=None,
                                         type_=None,
                                         vault_critical_operation_exclusion_list=None):
    parameters = {}
    parameters['e_tag'] = e_tag
    parameters['location'] = location
    parameters['tags'] = tags
    parameters['identity'] = {}
    parameters['identity']['type'] = type_
    parameters['properties'] = {}
    parameters['properties']['vault_critical_operation_exclusion_list'] = vault_critical_operation_exclusion_list
    return client.put(resource_group_name=resource_group_name,
                      resource_guards_name=resource_guards_name,
                      parameters=parameters)


def dataprotection_resource_guard_delete(client,
                                         resource_group_name,
                                         resource_guards_name):
    return client.delete(resource_group_name=resource_group_name,
                         resource_guards_name=resource_guards_name)

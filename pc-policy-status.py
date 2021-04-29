from __future__ import print_function
try:
    input = raw_input
except NameError:
    pass
from pc_lib_api import pc_api
import pc_lib_api
import pc_lib_general

# --Configuration-- #

parser = pc_lib_general.pc_arg_parser_defaults()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    '-t',
    '--policy_type',
    type=str,
    choices=['config', 'network', 'audit_event', 'anomaly', 'all'],
    help='Policies to enable or disable, by Policy type.')
group.add_argument(
    '-s',
    '--compliance_standard',
    type=str,
    help='Policies to enable or disable, by Compliance Standard.')
parser.add_argument(
    'status',
    type=str,
    choices=['enable', 'disable'],
    help='Policy status to set (enable or disable).')
args = parser.parse_args()

# --Initialize-- #

pc_lib_general.prompt_for_verification_to_continue(args.yes)
pc_settings = pc_lib_general.pc_settings_get(args.username, args.password, args.uiurl, args.config_file)
pc_api.configure(pc_settings['apiBase'], pc_settings['username'], pc_settings['password'])

# --Main-- #

# Transform the status argument for use with Python and the API.
specified_policy_status = True if args.status.lower() == 'enable' else False
specified_policy_status_string = str(specified_policy_status).lower()

policy_list_to_update = []

if args.policy_type is not None:
    policy_type = args.policy_type.lower()
    print('API - Getting list of Policies by Policy Type ...', end='')
    policy_list = pc_lib_api.api_policy_v2_list_get()
    print(' done.')
    print()
    for policy in policy_list:
        if policy['enabled'] is not specified_policy_status:
            if policy_type == 'all' or policy['policyType'] == policy_type:
                policy_list_to_update.append(policy)

if args.compliance_standard is not None:
    compliance_standard = args.compliance_standard
    print('API - Getting list of Policies by Compliance Standard ...', end='')
    policy_list = pc_lib_api.api_compliance_standard_policy_v2_list_get(compliance_standard)
    print(' done.')
    for policy in policy_list:
        if policy['enabled'] is not specified_policy_status:
            policy_list_to_update.append(policy)

print('API - Updating Policies ...')
for policy in policy_list_to_update:
    print('API - Updating Policy: %s' % policy['name'])
    pc_lib_api.api_policy_status_update(policy['policyId'], specified_policy_status_string)
print('Done.')
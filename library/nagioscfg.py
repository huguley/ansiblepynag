#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Russell Huguley <huguleyit@gmail.com>
#
# This is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: nagioscfg
version_added: "historical"
short_description: Manages nagios config files via ansible
description:
    - uses pynags Model to allow managing nagios config files
options:
  hostname:
    description:
      - hostname to use for querying the config files
    required: false
    default: null
    aliases: []

author:
    - "Russell Huguley"
notes:
   - Requires that pynag be installed
'''

EXAMPLES = '''

# Get the section for a host
- readhost:
    hostname: myhost
'''

RETURN = '''

'''

from pynag import Model
import os

# import module snippets
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pycompat24 import get_exception
from ansible.module_utils._text import to_bytes, to_native

def main():

    module = AnsibleModule(
        argument_spec = dict(
            configpath        = dict(required=True, type='str'),
            hostname          = dict(required=False, type='str'),
        ),
        add_file_common_args=True,
        supports_check_mode=True,
    )

    hostname = module.params['hostname']
    configpath = module.params['configpath']

    if not os.path.exists(configpath):
        module.fail_json(msg="Nagios config %s not found" % (configpath))

    changed = False

    host = Model.Host.objects.filter(host_name=hostname)
    response = {"host_name": host[0].host_name, "ip": host[0].address}

    if not module.check_mode:
        # Save here if not check mode
        pass

    module.exit_json(meta=response)

if __name__ == '__main__':
    main()

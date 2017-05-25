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
    - "copied from ansible project file module"
notes:
   - Requires that pynag be installed
'''

EXAMPLES = '''

# set the section for a host
- nagiosconfig:
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
            host_name         = dict(required=False, type='str'),
            service           = dict(required=False, type='str'),
            contact           = dict(required=False, type='str'),
            replace           = dict(required=False, default=False, type='bool'),
            values            = dict(required=True, type='dict'),
        ),
        add_file_common_args=True,
        supports_check_mode=True,
    )

    host_name = module.params['host_name']
    configpath = module.params['configpath']
    replaceall = module.params['replace']
    response = {}

    if not os.path.exists(configpath):
        module.fail_json(msg="Nagios config %s not found" % (configpath))

    Model.cfg_file = configpath

    changed = False
    curhost = None
    if host_name :
       host = Model.Host.objects.filter(host_name=host_name)
       if host and replaceall:
          curhost = host[0]
          for i in curhost.keys():
             if i not in ['meta','id']:
                curhost[i] = None
       else:
          curhost = Model.Host()
          curhost.use = 'New hosts go in a pynag/hosts folder need to fix this'
          
       for key, value in module.params['values'].iteritems():
          changed = True
          curhost[key] = value 
          pass
          
    if not module.check_mode:
        # Save here if not check mode
        curhost.save()
        pass

    module.exit_json(meta=response)

if __name__ == '__main__':
    main()

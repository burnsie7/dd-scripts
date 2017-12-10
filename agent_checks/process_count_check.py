init_config:

instances:
    - proc_name: gunicorn
      proc_num: 3
      tags: ['env:demo', 'app:django']

    - proc_name: python
      proc_num: 4
      tags: ['env:demo', 'app:django']


import commands

from checks import AgentCheck

class ProcessCheck(AgentCheck):

    def check(self, instance):
        proc_name = instance['proc_name']
        proc_num = instance['proc_num']
        tags = instance['tags']
        check_str = 'ps uaxw |grep ' + proc_name + ' |grep -c -v grep'
        output = commands.getoutput(check_str)
        current_procs = 0
        try:
            current_procs = int(output)
            proc_num = int(proc_num)
        except Exception as e:
            pass
        if current_procs >= proc_num:
            self.service_check('process_count.' + proc_name, AgentCheck.OK, tags=tags)
        else:
            self.service_check('process_count.' + proc_name, AgentCheck.CRITICAL, tags=tags)

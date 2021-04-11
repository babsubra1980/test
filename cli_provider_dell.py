from netmiko import ConnectHandler
import time
i = 0
delay_fact = 4
max_timeout_sec = 3000
while (i == 0):
   net_connect = ConnectHandler(device_type='dell_force10', host='100.104.45.125', username='roadmin', password='Dell@Force10', global_delay_factor=delay_fact)
   prompt_str = net_connect.find_prompt()
   try:
      output = net_connect.send_command(command_string="show interface", expect_string=prompt_str, delay_factor=delay_fact, auto_find_prompt=False, max_loops=(max_timeout_sec/delay_fact))
      print(output)
      output = net_connect.send_command(command_string="show interface port-channel summary", expect_string=prompt_str, delay_factor=delay_fact, auto_find_prompt=False, max_loops=(max_timeout_sec/delay_fact))
      print(output)
      output = net_connect.send_command(command_string="show running-configuration interface ethernet", expect_string=prompt_str, delay_factor=delay_fact, auto_find_prompt=False, max_loops=(max_timeout_sec/delay_fact))
      print(output)
      output = net_connect.send_command(command_string="show running-configuration interface port-channel", expect_string=prompt_str, delay_factor=delay_fact, auto_find_prompt=False, max_loops=(max_timeout_sec/delay_fact))
      print(output)
      output = net_connect.send_command(command_string="show lldp neighbors detail", expect_string=prompt_str, delay_factor=delay_fact, auto_find_prompt=False, max_loops=(max_timeout_sec/delay_fact))
      print(output)
      output = net_connect.send_command(command_string="show running-configuration vlt", expect_string=prompt_str, delay_factor=delay_fact, auto_find_prompt=False, max_loops=(max_timeout_sec/delay_fact))
      print(output)
   except:
      print("\n\nException raised\n\n")
      pass
   net_connect = net_connect.disconnect()
   #time.sleep(1)

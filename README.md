# libvirt_http_mc
A not so intelligent platform management interface for libvirt's VMs using HTTP

<h1>Foreword</h1>
<p>
This Management Controller is made to work hand in hand with libvirt's 'virsh' shell.
This virsh shell is used to manage the virtual machines assigned to libvirt.
It was designed to offer to the user the ability to control VMs as an IPMI tool would do.
If users would rather use the IPMI protocol, the author recommends using the ipmi_sim application, which is part of the OpenIPMI project.
Sadly, this tool those not allow for boot order manipulation out of the box, which was a requirement for the author's project.
Henceforth this tool was developed : it interfaces quite well with Mr-Provisioner, Linaro's Mr-Provisioner.
</p>
<h1>Installation Instruction</h1>
<p>
The tool obviously requires that libvirt and the virsh tool are installed on your system, as well as a few VMs to be connected to it.
It is entirely written in Python (python 3.5.3), and the HTTP daemon engine used is CherryPy.

<b>This tool has only been tested on Debian 9. It will probably work on any system supported by both CherryPy, Libvirt and Python.</b>

Consequently, cherrypy version 14.0.0 is required.
python 3.5.3 is also recommended, but the tool has been written with compatibilty in mind.
requests 2.12.4 (at least) is required.

Just git clone this repository, and run the libvirt_mc.py file as sudo.
Ensure that your firewall is correctly configured.
</p>
<h1>Usage</h1>
<p>
To use this tool you can use either a http requests library, or your browser.

This tool returns json formatted text on the information requests, and nothing (HTTP 200) on actions (this behaviour might be modified in the future).

With this tool you can:
- List the available machines with their names, ids and status : http://listeningip:listeningport/service/machine
- Return name, id and status of a specific machine : http://listeningip:listeningport/service/machinename
- Return the status of a specific machine : http://listeningip:listeningport/service/machinename/state_controller/status
- Power off or on a specific machine : http://listeningip:listeningport/service/machinename/state_controller/cyclepower
- Reboot a specific machine : http://listeningip:listeningport/service/machinename/state_controller/reboot
- Force Reset of a specific machine : http://listeningip:listeningport/service/machinename/force_reset
- Force a (graceful, i.e. no SIGKILL) of a specific machine :http://listeningip:listeningport/service/machinename/state_controller/force_off
- Do a PXE boot of a specific machine :http://listeningip:listeningport/service/machinename/state_controller/pxeboot
- Do a Disk boot of a specific machine : http://listeningip:listeningport/service/machinename/state_controller/diskboot
</p>
<h1>Additional Notes and known issues</h1> 
<p>
This tool will pxe boot/disk boot prioritizing the first network interface/disk it finds in the original bootorder. Then it will put all other network interfaces/disks following it in the new bootorder.

This tool backs up your VM's xml configuration before changing in, appending the date and 'backup' extension to it.
defaultboot is also a command, but it doesn't do anything at the moment. It might become the restore backup command in  the future.

Known issue :
- PXEbooting/Diskbooting a running machine will fail. Please insure the machine is shut off before pxe/disk booting it.
</p>
<h1>Future</h1>
<p>
In the future Digest Authentication should make be available, also PXEbooting should be fixed and maybe a consistent json text return for each action call.
</p>
<h1>Final word</h1>
<p>
If you find any issues with the app please send me an email or open an issue.
Pull requests are welcome !
If you have a working pxebooting version of ipmi_sim I will also be glad to look into it !
</p>

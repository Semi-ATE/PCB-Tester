<h1>PCB-Tester</h1>

<p>A <code>PCB-Tester</code> is a base setup that is used to test a PCB.</p>

<p>The tool is used by OEM's either in new production and/or repair.</p>

<p>The PCB-Tester project implements such a <code>PCB-Tester</code> in open source.</p>

<p>It consists out of the following components:</p>

<ul>
<li><a href="https://github.com/ate-org/PCB-Tester/tree/master/hardware/mechanics/solidworks/rack">Rack</a> ➜ 19", holds the 'instruments' of choice when implementing a <code>PCB-tester</code> for a specific PCB.</li>
<li><a href="https://github.com/ate-org/PCB-Tester/tree/master/hardware/mechanics/solidworks/housing">Housing</a> ➜ The 'box' that holds the PCB-Tester (1x <a href="https://github.com/ate-org/PCB-Tester/tree/master/hardware/electronics/altium/PCB-Tester-Board">PCB-Tester-Board</a> and 0 or more <a href="https://github.com/ate-org/PCB-Tester/tree/master/hardware/electronics/altium/PCB-Relay-Board">PCB-Relay-Boards</a>)</li>
<li><a href="https://github.com/ate-org/PCB-Tester/tree/master/hardware/mechanics/solidworks/fixture">Fixture</a> ➜ Mounted on the <code>Housing</code>, and implements the "moving parts".</li>
<li>JIG ➜ <strong>Not</strong> a part of this project, belongs to a specific implementation. (iow: 'needle-bed')</li>
<li><a href="https://github.com/ate-org/PCB-Tester/tree/master/software">The Software framework</a>.</li>
</ul>

<p>The whole thing looks like this:</p>

<p align="center">
  <img src="/media/documentation/pictures/PCB-Tester.png">
</p>

<h1>Wiki</h1>

<p>Further reading at the project's <a href="https://github.com/ate-org/PCB-Tester/wiki">wiki</a>.</p>

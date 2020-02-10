goworking-map
===

System to aid control of desks at Fábrica do Futuo's Go Working.  

Copyright (C) 2019-2020 Fábrica do Futuro  

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU General Public License as published by  
the Free Software Foundation, either version 3 of the License, or  
(at your option) any later version.  

This program is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  
GNU General Public License for more details.  

You should have received a copy of the GNU General Public License  
along with this program.  If not, see <http://www.gnu.org/licenses/>.  

i18n
---

* [English](./README.md)  
* [Português Brasileiro](./README.pt.md)  

---

RGSoC 2020
---

This project is part of Rails of Girls Summer of Code 2020. The offical 
page for this project is at the 
[RGSoC Teams App](https://teams.railsgirlssummerofcode.org/projects/366-improve-the-desks-control-system-for-the-coworking).  

### Description

The "Go Working Map" started as a web form to aid the control of the 
desks at 
[Fábrica do Futuro's Go Working](https://fabricadofuturo.com/en/#terreo). 
Then it evolved to a system where all inhabitants of 
[Fábrica do Futuro](https://fabricadofuturo/en/) could find information 
on each other's startup and business, effectively providing a virtual 
place as a means for exchanges.  

Because the project wasn't meant for this purpose, the code - 
originally a simple collection of Flask-WTF html forms - needs 
refactoring. The current code base is not suited for the stakeholder's 
demands on the project.  

Ideally the website should be able to include more information about 
[Fábrica do Futuro](https://fabricadofuturo.com/en/)'s inhabitants. 
People should be able to update their own information and share it with 
others, pretty much like a regular social network. End users should be 
able to request additional functionality and the scope of the project 
shall be easily expanded on demand.  

Since this is a Libre Software project, the team shall bear in mind 
that contributions to this project could and ideally would improve 
other co-workings worldwide. So that should be taken into account in 
the development process.  

[Fábrica do Futuro](https://fabricadofuturo.com/en/) has infrastructure 
at Porto Alegre - Brasil to house the team working on the project so 
the team will be directly affected by this project, at least 
temporarily - but you're welcome to stay here after the SoC! ;) - and 
we would expect from the team much feedback on the system and that you 
participate on defining it's scope and suggest new functionalities, 
even if they will have to be implemented by others.  

Team will have full access to the 
[Fábrica do Futuro's Go Working](https://fabricadofuturo.com/en/#terreo) 
as if they were inhabitants. This includes but is not limited to 
electrical and caffeine power, access to high speed wireless internet 
(and by July gigabit ethernet on all desks), bathrooms, showers, 
meditation room, call booths, meeting rooms, living spaces, a retro 
games emulator and happy smiles everywhere.  

### Tasks and features

Things that should be done:  

* The project needs someone  who can research and implement a proper 
[ACL](https://en.wikipedia.org/wiki/Access-control_list) which will be 
responsible to enforce the business rules to display information to 
logged in users;  
* Personal information of companies and individuals should be stored 
and used respecting the Brazilian pertinent legislation the 
[LGPD](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/L13709.htm). 
We have mentoring on that, you don't need to do legal research;  
* We currently only have a web interface built on Flask itself. It 
would be nice to have an Android/iOS application that we could provide 
to people who prefer that interface, but that's not the main goal;  
* Users requested some sort of job board so startups could advertise to 
each other (or maybe externally?) with what and how they need help. 
Perhaps you could help to make the very code that will help you find 
your next contractor or business partner ;)  

Don't worry about taking care of all these tasks. You may freely select 
which ones you feel more comfortable working on. You may even propose 
other tasks and if they make sense, we can change the scope of the 
project accordingly.  

### Requirements

The programming language of the project is Python since it's already 
written using the [Flask](https://flask.palletsproject.com) framework.  

For the optional Android/iOS app, you are free to choose the technology 
used.  

### Tags

Python, Flask, LGPD, Jinja, Bootstrap, MySQL, SQLAlchemy  

---

TODO: Translate to english the rest of the README  

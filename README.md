# miltonsthesis-client
# pre requisites
* install python with path setup
* install pip 
<br/><br/>

# make new directory
for installation first you need
make a new directory for run 

`mkdir <file-path>` <br/> on your command prompt
and make virtual environment to install virtual environment
for that 
# on windows
write your command prompt <br/>
`py -m pip install --user virtualenv` and `Enter`

then again run <br/>
`py -m venv env` 

# for mac or linux 
write<br/>`python3 -m pip install --user virtualenv` on your terminal
then run<br/>
`python3 -m venv env ` 
# active virtual environment
for active virtual environment run<br/>
`.\env\Scripts\activate` for Windows<br/>
`source env/bin/activate` for linux and mac <br/>
# clone repository
then you need to clone this repository 
for that run <br/>
`git clone https://github.com/ruhullahil/miltonsthesis-client.git`
on your cmd or terminal  <br/><br/>
# go directory
then goto directory `miltonsthesis-client` <br/>
run <br/> `cd miltonsthesis-client` <br/>
Then run <br/><br/>
`pip install -r requirement.txt` <br/><br/>
# run server
`python lib/server/server.py` 
<br/><br/>
# run client 
<br/> `python lib/client/client.py`


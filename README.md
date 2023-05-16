<h1> Dango TODO CBV </h1> 

a simple todo app using __django__

<hr>
    <h2>
        installation:
    </h2>
    <ol>
        <li>pull the project</li>
        <li>run docker compose up</li>
    </ol>
<hr>
<p>its a fullstack project however there is an api you can check with
http://127.0.0.1:8000/swagger
</p>
<p>
smtp4dev is also running on port 5000
</p>

there is a second docker-compose file called docker-compose-stage.yaml  
this one runs nginx instead of smtp4dev
  
<h4> if you want to use docker compose -f ./docker-compose-stage.yml up --build :</h4>
you need to specify following in the 'stage_variables'  file :

DEBUG = False   
SMTP_USERNAME= {{ your smtp username }}  
SMTP_PASSWORD=  {{ your smtp password }}  

<hr/>
this project will automatically check the tests before the merge to main and then push to server 
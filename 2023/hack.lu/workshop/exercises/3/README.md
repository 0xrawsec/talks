# Webshell Exercise

Apply the methodology we have found previously and build nice rules to detect 
webshells.

Bonus: try to make solid detection rules, not just to detect this particular
kind of webshell.

# Tip: Start the webshell

In a terminal run a PHP webshell
```bash
# unzip webshell (password: "infected")
7z x webshell.zip

# run the readymade docker container (replace $PATH_TO_WS with the 
# absolute path where the WS got unzipped)
sudo docker run -v $PATH_TO_WS:/var/www/html --net=internal -it --rm -p 127.0.0.1:8080:80 -h pwned php:apache
```

Open firefox and navigate to the webshell http://localhost:8080

Interact with the webshell

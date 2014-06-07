rube-mc-pi
==========

Infrastructure code needed to make the Manchester CoderDojo Rube Goldberg machine work.


For more info see: http://wiki.mcrcoderdojo.org.uk/index.php/Rube_Goldberg_Project



Coding Guidelines
=================

* Create a feature branch for your change
* Write a test that fails
* python setup.py test
* Write code to make the test pass
* Repeat until done
* Commit changes to branch
* pylint rube-mc-pi | less
* Fix lint issues
* python setup.py test
* If tests pass commit to branch
* Merge branch to master
* python setup.py test
* If tests pass commit to branch
* If you want to release to pypi...
* Ideally on a raspberry pi run python setup.py test  (this is to make sure the gpio code is tested)
* Edit setup.pi
* Change the version number following these guidelines http://apr.apache.org/versioning.html
* Commit to master
* git push origin master
* Publish with: python setup.py register sdist upload
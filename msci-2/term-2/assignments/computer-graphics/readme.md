# How to run
To allow textures to be accessed,
this must be run on a http server.
One way to do this is using the npm
package `http-server`. With
this package installed go to the root directory
of this folder and run the command
`http-server`.
The command-prompt should provide
information on which port number
it is running on, normally
accessed on http://localhost:8080.
Once the http-server is running,
the scene can be found at
http://localhost:8080/main.html.

# Moving the camera
The `A` and `D`
can be used to move the camera
(and the lighting direction).

# External resources
Textures are used and can be found
in the `texture.png` file, it is a 1024x1024
image which contains 16 256x256 images (but
not all of them are filled / used).
I also (clearly) use WebGL
and a matrix library `cuon-matrix.js`.
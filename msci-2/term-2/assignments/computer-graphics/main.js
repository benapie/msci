function loadTextureAndDraw() {
    this.gl.pixelStorei(this.gl.UNPACK_FLIP_Y_WEBGL, 1); // Flip the image's y axis

    // Enable texture unit0
    this.gl.activeTexture(this.gl.TEXTURE0);

    // Bind the texture object to the target
    this.gl.bindTexture(this.gl.TEXTURE_2D, this.texture);

    // Set the texture image
    this.gl.texImage2D(this.gl.TEXTURE_2D, 0, this.gl.RGB, this.gl.RGB, this.gl.UNSIGNED_BYTE, this.texture.image);
    this.gl.texParameteri(this.gl.TEXTURE_2D, this.gl.TEXTURE_MIN_FILTER, this.gl.LINEAR);

    this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);

    // Assign u_Sampler to TEXTURE0
    this.gl.uniform1i(this.u_Sampler, 0);

    // Enable texture mapping
    this.gl.uniform1i(this.u_UseTextures, true);

    this.draw();
}


class Main {
    initialiseShaders() {
        if (!initShaders(this.gl, VSHADER_SOURCE, FSHADER_SOURCE)) {
            console.log('Failed to intialize shaders.');

        }
    }

    getUniformLocations() {
        this.u_ModelMatrix = this.gl.getUniformLocation(this.gl.program, 'u_ModelMatrix');
        this.u_ViewMatrix = this.gl.getUniformLocation(this.gl.program, 'u_ViewMatrix');
        this.u_NormalMatrix = this.gl.getUniformLocation(this.gl.program, 'u_NormalMatrix');
        this.u_ProjMatrix = this.gl.getUniformLocation(this.gl.program, 'u_ProjMatrix');
        this.u_LightColor = this.gl.getUniformLocation(this.gl.program, 'u_LightColor');
        this.u_LightDirection = this.gl.getUniformLocation(this.gl.program, 'u_LightDirection');
        this.u_isLighting = this.gl.getUniformLocation(this.gl.program, 'u_isLighting');
        this.u_TexCoord = this.gl.getUniformLocation(this.gl.program, 'u_TexCoord');

        // Error checking
        if (!this.u_ModelMatrix) {
            console.log('Failed to get the address of u_ModelMatrix.');
            return;
        }
        if (!this.u_ViewMatrix) {
            console.log('Failed to get the address of u_ViewMatrix.');
            return;
        }
        if (!this.u_NormalMatrix) {
            console.log('Failed to get the address of u_NormalMatrix.');
            return;
        }
        if (!this.u_ProjMatrix) {
            console.log('Failed to get the address of u_ProjMatrix.');
            return;
        }
        if (!this.u_LightColor) {
            console.log('Failed to get the address of u_LightColor.');
            return;
        }
        if (!this.u_LightDirection) {
            console.log('Failed to get the address of u_LightDirection.');
            return;
        }
        if (!this.u_isLighting) {
            console.log('Failed to get the address of u_isLighting.');
            return;
        }
        if (!this.u_TexCoords) {
            console.log('Failed to get the address of u_isLighting.');

        }
    }

    initialiseVertexBuffer() {
        this.gl.uniform1i(this.u_isLighting, 0);

        var vertexArray = new Float32Array([
            0.5, 1.0, 0.5, -0.5, 1.0, 0.5, -0.5, 0.0, 0.5, 0.5, 0.0, 0.5,
            0.5, 1.0, 0.5, 0.5, 0.0, 0.5, 0.5, 0.0, -0.5, 0.5, 1.0, -0.5,
            0.5, 1.0, 0.5, 0.5, 1.0, -0.5, -0.5, 1.0, -0.5, -0.5, 1.0, 0.5,
            -0.5, 1.0, 0.5, -0.5, 1.0, -0.5, -0.5, 0.0, -0.5, -0.5, 0.0, 0.5,
            -0.5, 0.0, -0.5, 0.5, 0.0, -0.5, 0.5, 0.0, 0.5, -0.5, 0.0, 0.5,
            0.5, 0.0, -0.5, -0.5, 0.0, -0.5, -0.5, 1.0, -0.5, 0.5, 1.0, -0.5
        ]);

        var normalArray = new Float32Array([
            0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,
            1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
            -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0,
            0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0,
            0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0
        ]);

        var textureCoordinates = new Float32Array([
            1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
            0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
            1.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 1.0
        ]);

        var indexArray = new Uint8Array([
            0, 1, 2, 0, 2, 3,
            4, 5, 6, 4, 6, 7,
            8, 9, 10, 8, 10, 11,
            12, 13, 14, 12, 14, 15,
            16, 17, 18, 16, 18, 19,
            20, 21, 22, 20, 22, 23
        ]);


        // Write the vertex property to buffers (coordinates and normals)
        if (!this.initialiseArrayBuffer(this.gl, 'a_Position', vertexArray, this.gl.FLOAT, 3)) return -1;
        if (!this.initialiseArrayBuffer(this.gl, 'a_Normal', normalArray, this.gl.FLOAT, 3)) return -1;
        if (!this.initialiseArrayBuffer(this.gl, 'a_TexCoord', textureCoordinates, this.gl.FLOAT, 2)) return -1;

        // Unbind the buffer object
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, null);

        // Write the indices to the buffer object
        var indexBuffer = this.gl.createBuffer();
        if (!indexBuffer) {
            console.log('Failed to create the buffer object');
            return -1;
        }

        this.gl.bindBuffer(this.gl.ELEMENT_ARRAY_BUFFER, indexBuffer);
        this.gl.bufferData(this.gl.ELEMENT_ARRAY_BUFFER, indexArray, this.gl.STATIC_DRAW);

        return indexArray.length;
    }

    initialiseArrayBuffer(vertexColorArray, attribute, data, type, num) {
        var buffer = this.gl.createBuffer();
        if (!buffer) {
            console.log('Failed to create the buffer object');
            return false;
        }

        // Write date into the buffer object
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, buffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, data, this.gl.STATIC_DRAW);

        // Assign the buffer object to the attribute variable
        var a_attribute = this.gl.getAttribLocation(this.gl.program, attribute);
        if (a_attribute < 0) {
            console.log('Failed to get the storage location of ' + attribute);
            return false;
        }
        this.gl.vertexAttribPointer(a_attribute, num, type, false, 0, 0);

        // Enable the assignment of the buffer object to the attribute variable
        this.gl.enableVertexAttribArray(a_attribute);

        return true;
    }

    initialiseTextures(n) {
        this.n = n;
        this.texture = this.gl.createTexture();
        if (!this.texture) {
            console.log('Failed to create a texture object.');
            return false;
        }

        this.u_Sampler = this.gl.getUniformLocation(this.gl.program, 'u_Sampler');
        if (!this.u_Sampler) {
            console.log('Failed to get the storage location of u_Sampler.');
            return false;
        }

        this.texture.image = new Image();
        if (!this.texture.image) {
            console.log('Failed to create an image object.');
            return false;
        }

        this.texture.image.onload = loadTextureAndDraw.bind(this);

        this.texture.image.src = './texture.png';

        return true;
    }

    setTextureCoordinatesMatrix(index) {
        // 12 13 14 15
        // 8  9  10 11
        // 4  5  6  7
        // 0  1  2  3
        this.textureCoordinatesMatrix = new Float32Array([
            0.21, 0.0, 0.02 + 0.25 * (index % 4),
            0.0, 0.21, 0.02 + 0.25 * (Math.floor(index / 4)),
            0.0, 0.0, 1
        ]);
    }

    constructor(canvas) {
        this.modelMatrix = new Matrix4();
        this.viewMatrix = new Matrix4();
        this.projectionMatrix = new Matrix4();
        this.normalMatrix = new Matrix4();
        this.textureCoordinatesMatrix = new Float32Array();

        this.angleStep = 5.0;
        this.xAngle = 0.0;
        this.yAngle = 0.0;

        this.canvas = canvas;
        this.gl = getWebGLContext(canvas);
        if (!this.gl) {
            console.log('Failed to get rendering context for WebGL.');
            return;
        }

        this.initialiseShaders();
        var n = this.initialiseVertexBuffer();

        this.gl.clearColor(0.0, 0.0, 0.0, 1.0);
        this.gl.enable(this.gl.DEPTH_TEST);
        this.gl.enable(this.gl.BLEND);

        this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);


        this.getUniformLocations();

        // Initial lighting
        this.gl.uniform3f(this.u_LightColor, 1.0, 0.95, 0.89);
        var lightDirection = new Vector3([3.0, 2.0, 4.0]);
        lightDirection.normalize();
        this.gl.uniform3fv(this.u_LightDirection, lightDirection.elements);


        this.cameraAngle = 14;
        this.updateCamera();
        // Initialise view matrix
        // this.viewMatrix.setLookAt(12, 22, 22, 0, 0, 0, 0, 1, 5);
        // this.gl.uniformMatrix4fv(this.u_ViewMatrix, false, this.viewMatrix.elements);

        // Initialise projection matrix
        this.projectionMatrix.setPerspective(60, canvas.width / canvas.height, 1, 100);
        this.gl.uniformMatrix4fv(this.u_ProjMatrix, false, this.projectionMatrix.elements);

        // // Texture matrix
        // this.setTextureCoordinatesMatrix(0, 0, 1)
        // this.gl.uniformMatrix4fv(this.u_TexCoords, false, this.textureCoordinatesMatrix)

        // Animation parameters
        this.paintingAngle = 0;
        this.chairParameter = 0;
        this.cupParameter = 0;

        document.onkeydown = this.keyPressHandler;

        if (!this.initialiseTextures(n)) {
            console.log('Failed to initialise textures.');

        }

    }

    drawRotatedCuboidCustomOrigin(originArray, positionArray, dimensionArray, rotationArray, angle, textureID) {
        this.modelMatrix.setTranslate(
            positionArray[0] + originArray[0],
            positionArray[1] - (dimensionArray[1] / 2) + originArray[1],
            positionArray[2] + originArray[2]
        );
        this.modelMatrix.scale(
            dimensionArray[0],
            dimensionArray[1],
            dimensionArray[2]
        );
        this.modelMatrix.rotate(angle, rotationArray[0], rotationArray[1], rotationArray[2]);

        this.normalMatrix.setInverseOf(this.modelMatrix);
        this.normalMatrix.transpose();

        this.setTextureCoordinatesMatrix(textureID);

        // Set uniform matrices
        this.gl.uniformMatrix4fv(this.u_ModelMatrix, false, this.modelMatrix.elements);
        this.gl.uniformMatrix4fv(this.u_NormalMatrix, false, this.normalMatrix.elements);
        this.gl.uniformMatrix3fv(this.u_TexCoord, false, this.textureCoordinatesMatrix);

        // Draw
        this.gl.drawElements(this.gl.TRIANGLES, this.n, this.gl.UNSIGNED_BYTE, 0);
    }

    drawCuboid(positionArray, dimensionArray, textureID) {
        // Set model and normal matrix
        this.modelMatrix.setTranslate(
            positionArray[0],
            positionArray[1] - (dimensionArray[1] / 2),
            positionArray[2]
        );
        this.modelMatrix.scale(
            dimensionArray[0],
            dimensionArray[1],
            dimensionArray[2]
        );
        this.normalMatrix.setInverseOf(this.modelMatrix);
        this.normalMatrix.transpose();

        this.setTextureCoordinatesMatrix(textureID);

        // Set uniform matrices
        this.gl.uniformMatrix4fv(this.u_ModelMatrix, false, this.modelMatrix.elements);
        this.gl.uniformMatrix4fv(this.u_NormalMatrix, false, this.normalMatrix.elements);
        this.gl.uniformMatrix3fv(this.u_TexCoord, false, this.textureCoordinatesMatrix);


        // Draw
        this.gl.drawElements(this.gl.TRIANGLES, this.n, this.gl.UNSIGNED_BYTE, 0);
    }

    drawCuboidCustomOrigin(originArray, positionArray, dimensionArray, textureID) {
        this.drawCuboid(
            [
                positionArray[0] + originArray[0],
                positionArray[1] + originArray[1],
                positionArray[2] + originArray[2]
            ],
            [
                dimensionArray[0],
                dimensionArray[1],
                dimensionArray[2]
            ],
            textureID
        );
    }

    drawChairBase(originArray, textureID) {
        // Legs
        this.drawCuboidCustomOrigin(originArray, [0.5, 0.5, 0.75], [0.25, 0.25, 1.5], textureID);
        this.drawCuboidCustomOrigin(originArray, [-0.5, 0.5, 0.75], [0.25, 0.25, 1.5], textureID);
        this.drawCuboidCustomOrigin(originArray, [-0.5, -0.5, 0.75], [0.25, 0.25, 1.5], textureID);
        this.drawCuboidCustomOrigin(originArray, [0.5, -0.5, 0.75], [0.25, 0.25, 1.5], textureID);
        // Seat
        this.drawCuboidCustomOrigin(originArray, [0, 0, 1.5], [1.5, 1.5, 0.25], textureID);
    }

    drawChair(originArray, textureID) {
        this.drawChairBase(originArray, textureID);
        // Back
        this.drawCuboidCustomOrigin(
            originArray,
            [0, -0.625, 2.75],
            [1.5, 0.25, 2.5],
            textureID
        );
    }

    drawChairRotate90(originArray, textureID) {
        this.drawChairBase(originArray, textureID);
        // Back
        this.drawCuboidCustomOrigin(originArray, [0.625, 0, 2.75], [0.25, 1.5, 2.5], textureID);
    }

    drawChairRotate180(originArray, textureID) {
        this.drawChairBase(originArray, textureID);
        // Back
        this.drawCuboidCustomOrigin(originArray, [0, 0.625, 2.75], [1.5, 0.25, 2.5], textureID);
    }

    drawChairRotate270(originArray, textureID) {
        this.drawChairBase(originArray, textureID);
        // Back
        this.drawCuboidCustomOrigin(originArray, [-0.625, 0, 2.75], [0.25, 1.5, 2.5], textureID);
    }

    drawFloor(textureID) {
        var x_pos;
        var y_pos;
        for (var i = 0; i < this.floor_size ** 2; i++) {
            x_pos = this.tile_size
                * ((this.floor_size / 2)
                    - (i % this.floor_size))
                - this.tile_size / 2;
            y_pos = this.tile_size
                * ((this.floor_size / 2)
                    - (Math.floor(i / this.floor_size)))
                - this.tile_size / 2;
            this.drawCuboid(
                [x_pos, y_pos, -0.5],
                [this.tile_size, this.tile_size, 1],
                textureID
            );
        }
    }

    drawTable(originArray, textureID) {
        this.drawCuboidCustomOrigin(
            originArray,
            [2, 2, 1.25],
            [0.25, 0.25, 2.5],
            textureID
        );
        this.drawCuboidCustomOrigin(
            originArray,
            [2, -2, 1.25],
            [0.25, 0.25, 2.5],
            textureID
        );
        this.drawCuboidCustomOrigin(
            originArray,
            [-2, 2, 1.25],
            [0.25, 0.25, 2.5],
            textureID
        );
        this.drawCuboidCustomOrigin(
            originArray,
            [-2, -2, 1.25],
            [0.25, 0.25, 2.5],
            textureID
        );
        this.drawCuboidCustomOrigin(
            originArray,
            [0, 0, 2.5],
            [4.5, 4.5, 0.25],
            textureID
        );
    }

    chairContour(parameter) {
        if (parameter % 60 < 30) {
            return (parameter % 60) / 15;
        } else {
            return 4 - ((parameter % 60) / 15);
        }
    }

    drawTableAndChairs(originArray, textureID) {
        this.drawTable([originArray[0], originArray[1], originArray[2]], textureID);
        this.drawChair([originArray[0], originArray[1] - 2.5, originArray[2]], textureID);
        this.drawChairRotate90([originArray[0] + 2.5, originArray[1], originArray[2]], textureID);
        this.drawChairRotate180([originArray[0], originArray[1] + 2.5 + this.chairContour(this.chairParameter), originArray[2]], textureID);
        this.drawChairRotate270([originArray[0] - 2.5, originArray[1], originArray[2]], textureID);
    }

    drawCoffeeTable(originArray, textureID) {
        this.drawCuboidCustomOrigin(originArray, [0, 0, 2.25], [5, 5, 1], textureID);
        this.drawCuboidCustomOrigin(originArray, [2, 2, 1.25], [0.5, 0.5, 2], textureID);
        this.drawCuboidCustomOrigin(originArray, [2, -2, 1.25], [0.5, 0.5, 2], textureID);
        this.drawCuboidCustomOrigin(originArray, [-2, 2, 1.25], [0.5, 0.5, 2], textureID);
        this.drawCuboidCustomOrigin(originArray, [-2, -2, 1.25], [0.5, 0.5, 2], textureID);
    }

    drawWalls(textureIDA, textureIDB) {
        var pos;
        for (var i = 0; i < this.floor_size; i++) {
            pos = this.tile_size
                * ((this.floor_size / 2)
                    - (i % this.floor_size))
                - this.tile_size / 2;

            this.drawCuboid(
                [(-1) * this.floor_size * this.tile_size * 0.5, pos, this.tile_size * 0.5 + 1],
                [0.25, this.tile_size, this.tile_size + 2],
                textureIDA
            );

            this.drawCuboid(
                [pos, (-1) * this.floor_size * this.tile_size * 0.5, this.tile_size * 0.5 + 1],
                [this.tile_size, 0.25, this.tile_size + 2],
                textureIDB
            );
        }
    }

    drawSofa(originArray, textureID) {
        this.drawCuboidCustomOrigin(originArray, [0, 0, 0.5], [7, 3, 1], textureID);
        this.drawCuboidCustomOrigin(originArray, [3, 0, 1.5], [1, 3, 1], textureID);
        this.drawCuboidCustomOrigin(originArray, [-3, 0, 1.5], [1, 3, 1], textureID);
        this.drawCuboidCustomOrigin(originArray, [0, -1.0, 1.5], [7, 1, 1], textureID);

    }

    drawSofaRotate90(originArray, textureID) {
        this.drawCuboidCustomOrigin(originArray, [0, 0, 0.5], [3, 7, 1], textureID);
        this.drawCuboidCustomOrigin(originArray, [0, 3, 1.5], [3, 1, 1], textureID);
        this.drawCuboidCustomOrigin(originArray, [0, -3, 1.5], [3, 1, 1], textureID);
        this.drawCuboidCustomOrigin(originArray, [-1, 0, 1.5], [1, 7, 1], textureID);
    }

    cupContour(parameter) {
        parameter = parameter % 360;
        parameter = (parameter * Math.PI) / 180;
        return [Math.cos(parameter), Math.sin(parameter)];
    }

    drawCup(originArray, textureID) {
        // Base
        this.drawCuboidCustomOrigin(
            originArray,
            [0.1, 0.3, 0.35],
            [0.75, 0.75, 0.1],
            textureID
        );
        // Walls
        this.drawCuboidCustomOrigin(
            originArray,
            [0.5, 0.325, 0.9],
            [0.1, 0.75, 1.2],
            textureID
        );
        this.drawCuboidCustomOrigin(
            originArray,
            [-0.2, 0.25, 0.9],
            [0.1, 0.75, 1.2],
            textureID
        );
        this.drawCuboidCustomOrigin(
            originArray,
            [0.17, -0.07, 0.9],
            [0.75, 0.1, 1.2],
            textureID
        );
        this.drawCuboidCustomOrigin(
            originArray,
            [0.12, 0.65, 0.9],
            [0.75, 0.1, 1.2],
            textureID
        );
    }

    drawPainting(originArray, textureID) {
        let actualAngle;
        if (this.paintingAngle % 100 < 50) {
            actualAngle = -115 + (this.paintingAngle % 50)
        } else {
            actualAngle = -65 - (this.paintingAngle % 50)
        }
        this.drawRotatedCuboidCustomOrigin(originArray, [0, 0, 0], [0, 4.2, 4.2], [1, 0, 0], actualAngle, textureID);
        this.drawRotatedCuboidCustomOrigin(originArray, [0.1, 0, 0], [0, 4, 4], [1, 0, 0], actualAngle, 9)
    }

    draw() {
        this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT);

        this.floor_size = 4;
        this.tile_size = 6;
        this.drawFloor(13);
        this.drawWalls(11, 10);

        this.drawTableAndChairs([8, -8, 0], 4);
        this.drawSofa([-4.5, -10, 0], 8);
        this.drawSofaRotate90([-10, -4.5, 0], 8);
        this.drawPainting([-11.86, 8, 6], 13);

        this.drawCoffeeTable([8, 8, 0], 12);
        let cupPosition = this.cupContour(this.cupParameter);
        this.drawCup([8 + cupPosition[0], 8 + cupPosition[1], 2.5], 5)

    }

    animate() {
        this.paintingAngle++;
        this.chairParameter++;
        this.cupParameter += 3;
        this.draw();
    }

    updateCamera() {
        let angle = (this.cameraAngle * 4 * Math.PI) / 180;
        let mod = 31;

        this.viewMatrix.setLookAt(
            mod * Math.cos(angle),
            mod * Math.sin(angle),
            22,
            0,
            0,
            0,
            0,
            1,
            5
        );


        var lightDirection = new Vector3([
            mod * Math.cos(angle),
            mod * Math.sin(angle),
            22]
        );
        lightDirection.normalize();
        this.gl.uniform3fv(this.u_LightDirection, lightDirection.elements);
        this.gl.uniformMatrix4fv(this.u_ViewMatrix, false, this.viewMatrix.elements);
    }

    keyPressHandler(key) {
        switch (key.keyCode) {
            case 65:  // a
                obj.cameraAngle--;
                obj.updateCamera();
                break;
            case 68:  // d
                obj.cameraAngle++;
                obj.updateCamera();
                break;
        }
    }
}


obj = new Main(document.getElementById('webgl'));

function animate() {
    obj.animate();
}

function main() {
    setInterval(animate, 50);
}

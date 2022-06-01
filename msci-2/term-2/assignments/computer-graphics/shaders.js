var VSHADER_SOURCE = `
attribute vec4 a_Position;
attribute vec4 a_Normal;
attribute vec2 a_TexCoord;

uniform mat4 u_ModelMatrix;
uniform mat4 u_NormalMatrix;
uniform mat4 u_ViewMatrix;
uniform mat4 u_ProjMatrix;
uniform vec3 u_LightColor;
uniform vec3 u_LightDirection;
uniform mat3 u_TexCoord;

varying vec3 v_Light;
varying vec2 v_TexCoord;

void main() {
    gl_Position = u_ProjMatrix * u_ViewMatrix * u_ModelMatrix * a_Position;

    vec3 normal = normalize((u_NormalMatrix * a_Normal).xyz);
    float nDotL = max(dot(normal, u_LightDirection), 0.3);

    v_Light = u_LightColor * nDotL;

    vec3 temp1 = vec3(a_TexCoord.x, a_TexCoord.y, 1) * u_TexCoord;
    v_TexCoord = vec2(temp1.x, temp1.y);
}
`;

var FSHADER_SOURCE = `
#ifdef GL_ES
precision mediump float;
#endif

uniform sampler2D u_Sampler;

varying vec3 v_Light;
varying vec2 v_TexCoord;

void main() {
    gl_FragColor = vec4(texture2D(u_Sampler, v_TexCoord).rgb * v_Light * 1.25, 1.0);
}
`;
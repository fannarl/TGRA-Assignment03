
from OpenGL.GL import *
from math import * # trigonometry

import sys

from Base3DObjects import *

class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc			= glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        ## ADD CODE HERE ##
        self.normalLoc			= glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        self.modelMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.ViewMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        # self.colorLoc               = glGetUniformLocation(self.renderingProgramID, "u_color")
        self.eyePosLoc               = glGetUniformLocation(self.renderingProgramID, "u_eye_position")

        self.lightPosLoc               = glGetUniformLocation(self.renderingProgramID, "u_pointLights[0].position")
        self.lightDiffuseLoc               = glGetUniformLocation(self.renderingProgramID, "u_pointLights[0].diffuse")
        self.lightSpecularLoc               = glGetUniformLocation(self.renderingProgramID, "u_pointLights[0].specular")

        self.lightPosLocEye               = glGetUniformLocation(self.renderingProgramID, "u_pointLights[1].position")
        self.lightDiffuseLocEye               = glGetUniformLocation(self.renderingProgramID, "u_pointLights[1].diffuse")
        self.lightSpecularLocEye               = glGetUniformLocation(self.renderingProgramID, "u_pointLights[1].specular")

        self.materialDiffuseLoc               = glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")
        self.materialSpecularLoc               = glGetUniformLocation(self.renderingProgramID, "u_mat_specular")
        self.materialShininessLoc               = glGetUniformLocation(self.renderingProgramID, "u_mat_shininess")

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.ViewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    # def set_solid_color(self, red, green, blue):
    #     glUniform4f(self.colorLoc, red, green, blue, 1.0)

    def set_eye_position(self, pos):
        glUniform3f(self.eyePosLoc, pos.x, pos.y, pos.z)

    def set_light_position(self, pos):
        glUniform3f(self.lightPosLoc, pos.x, pos.y, pos.z)

    def set_light_position_eye(self, pos):
        glUniform3f(self.lightPosLocEye, pos.x, pos.y, pos.z)

    def set_light_diffuse(self, red, green, blue):
        glUniform3f(self.lightDiffuseLoc, red, green, blue)

    def set_light_diffuse_eye(self, red, green, blue):
        glUniform3f(self.lightDiffuseLocEye, red, green, blue)

    def set_light_specular(self, red, green, blue):
        glUniform3f(self.lightSpecularLoc, red, green, blue)

    def set_light_specular_eye(self, red, green, blue):
        glUniform3f(self.lightSpecularLocEye, red, green, blue)

    def set_material_diffuse(self, red, green, blue):
        glUniform3f(self.materialDiffuseLoc, red, green, blue)

    def set_material_specular(self, red, green, blue):
        glUniform3f(self.materialSpecularLoc, red, green, blue)

    def set_material_shininess(self, shininess):
        glUniform1f(self.materialShininessLoc, shininess)

    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    ## ADD CODE HERE ##
    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)

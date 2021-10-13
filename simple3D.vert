attribute vec3 a_position;
// attribute vec3 a_normal;

// uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

attribute vec4 u_color;
varying vec4 v_color;  //Leave the varying variables alone to begin with

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	// vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	// local coordinates
	// position = u_model_matrix * position;
	// normal = u_model_matrix * normal;	

	// global coordinates
	// float light_factor_1 = max(dot(normalize(normal), normalize(vec4(1, 2, 3, 0))), 0.0);
	// float light_factor_2 = max(dot(normalize(normal), normalize(vec4(-3, -2, -1, 0))), 0.0);
	// v_color = (light_factor_1 + light_factor_2) * u_color; // ### --- Change this vector (pure white) to color variable --- #####
	v_color = u_color; // ### --- Change this vector (pure white) to color variable --- #####

    // v_color = u_color;

	position = u_view_matrix * position;
	// eye coordinates
	position = u_projection_matrix * position;
	// clip coordinates

	gl_Position = position;
}


// layout (location = 0) in vec3 aPos;
// void main()
// {
//    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
// }
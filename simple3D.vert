#version 150

attribute vec3 a_position;
attribute vec3 a_normal;

varying vec3 FragPos;
varying vec3 Normal;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

void main()
{
    FragPos = vec3(u_model_matrix * vec4(a_position, 1.0));
    Normal = mat3(transpose(inverse(u_model_matrix))) * a_normal;  
    
    gl_Position = u_projection_matrix * u_view_matrix * vec4(FragPos, 1.0);
}

// struct PointLight {    
//     vec4 position;
    
//     vec4 diffuse;
//     vec4 specular;
// }; 

// attribute vec4 a_position;
// //## ADD CODE HERE ##
// attribute vec4 a_normal;

// attribute vec4 FragPos;

// uniform mat4 u_model_matrix;
// uniform mat4 u_view_matrix;
// uniform mat4 u_projection_matrix;

// // uniform vec4 u_color;
// uniform vec4 u_eye_position;

// uniform PointLight u_point_light[2];

// // varying vec4 v_color;  //Leave the varying variables alone to begin with
// varying vec4 v_normal;
// varying vec4 v_s;
// varying vec4 v_h;


// void main(void)
// {
// 	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
// 	//## ADD CODE HERE ##
// 	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

// 	// local coordinates

// 	position = u_model_matrix * position;
// 	//## ADD CODE HERE ##
// 	v_normal = normalize(u_model_matrix * normal);	

// 	vec4 v = normalize(u_eye_position - position);

// 	vec4 result = vec4(0);

// 	// for(int i = 0; i < 2; i++)
// 	// {
// 	// 	// global coordinates
// 	// 	v_s += normalize(u_point_light[i].position - position);

// 	// 	v_h += normalize(v_s + v);
// 	// 	result += CalcPointLight(u_point_light[i], v_normal, FragPos, u_eye_position)
// 	// }



// 	// float light_factor_1 = max(dot(normalize(normal), normalize(vec4(1, 2, 3, 0))), 0.0);
// 	// float light_factor_2 = max(dot(normalize(normal), normalize(vec4(-3, -2, -1, 0))), 0.0);
// 	// v_color = (light_factor_1 + light_factor_2) * u_color; // ### --- Change this vector (pure white) to color variable --- #####



// 	// ### --- Change the projection_view_matrix to separate view and projection matrices --- ### 
// 	position = u_view_matrix * position;
// 	// eye coordinates
	
// 	position = u_projection_matrix * position;
// 	// clip coordinates

// 	gl_Position = position;
// }
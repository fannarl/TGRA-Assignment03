// uniform vec4 u_light_diffuse;
// uniform vec4 u_light_specular;
struct PointLight {    
    vec3 position;
    
    vec3 diffuse;
    vec3 specular;
}; 

uniform vec3 u_mat_diffuse;
uniform vec3 u_mat_specular;
uniform float u_mat_shininess;

// varying vec4 v_normal;
// varying vec4 v_s;
// varying vec4 v_h;

varying vec3 FragPos;
varying vec3 Normal;

uniform vec3 u_eye_position;
uniform PointLight u_pointLights[2];

vec3 CalcPointLight(PointLight light, vec3 normal, vec3 fragPos, vec3 viewDir)
{
    vec3 lightDir = normalize(light.position - fragPos);
    // diffuse shading
    float diff = max(dot(normal, lightDir), 0.0);
    // specular shading
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), u_mat_shininess);
    // attenuation
    float distance    = length(light.position - fragPos);
    float attenuation = 1.0 / (1.0 + 0.09 * distance + 0.032 * (distance * distance));    
    // combine results
    vec3 ambient  = vec3(0.2) * u_mat_diffuse;
    vec3 diffuse  = light.diffuse  * diff * u_mat_diffuse;
    vec3 specular = light.specular * spec * u_mat_specular;
    ambient  *= attenuation;
    diffuse  *= attenuation;
    specular *= attenuation;
    return (ambient + diffuse + specular);
} 

void main(void)
{    // properties
    vec3 norm = normalize(Normal);
    vec3 viewDir = normalize(u_eye_position - FragPos);
    
    // == =====================================================
    // Our lighting is set up in 3 phases: directional, point lights and an optional flashlight
    // For each phase, a calculate function is defined that calculates the corresponding color
    // per lamp. In the main() function we take all the calculated colors and sum them up for
    // this fragment's final color.
    // == =====================================================
    // phase 1: directional lighting
    vec3 result = vec3(0.0, 0.0, 0.0);
    // phase 2: point lights
    // for(int i = 0; i < 2; i++)
    result += CalcPointLight(u_pointLights[0], norm, FragPos, viewDir);    
    result += CalcPointLight(u_pointLights[1], norm, FragPos, viewDir);   
    // phase 3: spot light
    // result += CalcSpotLight(spotLight, norm, FragPos, viewDir);    
    
    gl_FragColor = vec4(result, 1.0);
	// float lambert = max(dot(v_normal, v_s), 0);
	// float phong = max(dot(v_normal, v_h), 0);

	// for(int i = 0; i < 2; i++)
	// {
	// 	// global coordinates
	// 	v_s += normalize(u_point_light[i].position - position);

	// 	v_h += normalize(v_s + v);
	// 	result += CalcPointLight(u_point_light[i], v_normal, FragPos, u_eye_position)
	// }

	// // gl_FragColor = u_light_diffuse * u_mat_diffuse * lambert
	// // 		+ u_light_specular * u_mat_specular * pow(phong, u_mat_shininess) + (u_mat_diffuse * 0.2);
    // gl_FragColor = vec4(result, 1.0);
}
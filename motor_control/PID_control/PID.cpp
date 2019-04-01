#include <iostream>
#include "PID.h"

PID::PID(double kp, double ki, double kd, double max, double min)
	:m_kp(kp), m_ki(ki), m_kd(kd), m_max(max), m_min(min) 
{}
PID::~PID()
{}
PID::double getError(double heading){
	double error;
	if(m_set_heading > heading){
		error = m_set_heading - heading;
		if(error > 180)
			error = -(360-error);
		return error;
	}
	else{
		error = heading - m_set_heading;
	       	if(error > 180)	
			error = 360-error;
		else
			error = -error;
		return error;
	}
}
PID::void setHeading(double set)
{
	if( (set<360) && (set>0) )
		m_set_heading = set;
	else
		cout<<"error input(wrong desired heading)!!!\n";
}
PID::double controller(double error)
{
	//proportional term 
	double p = m_kp * error;

	//integral term 
	m_I_error += error;
	double i = m_ki * m_I_error; 

	//derivative term
	if(m_first_exe)
		m_last_error = error;
	else{
		double d = m_kd * (error-m_last_error);
		m_last_error = error;
		m_first_exe = false;
	}

	//output voltage 
	double output = p + i + d;
	if(output < min)
		output = min;
	else if(output > max)
		output = max;
	return output;
}

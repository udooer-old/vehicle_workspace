#ifndef PID_HEADER
#define PID_HEADER

class PID
{
	public:
		PID(double kp, double ki, double kd, double max, double min);
		~PID();
	public:
		double getError(double);
	    void setConfig(double, double, double, int, int);
        void setHeading(double);
		double controller(double);
	private:
		double m_set_heading{0};
		double m_kp{1};
		double m_ki{1};
		double m_kd{1};
		double m_max{5};
		double m_min{2};
		double m_I_error{0};
		double m_last_error{0};
		bool m_first_exe{true};
	
};
#endif

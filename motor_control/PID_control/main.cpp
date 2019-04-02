#include "PID.h"
#include <iostream>
#include <vector>
#include <thread>
#include <unistd.h>

void loop(bool&);
using namespace std;
void writeLog(vector<double>, vector<double>);
void sleepInSecond(double);
string getCurrentDateTime(string);

int main(int argc, char* argv[])
{
    if(argc != 5){
        cout<<"Wrong Command!!!\n";
        cout<<"[.o] [kp] [ki] [kd] [desired heading]\n";
        return 1;
    }
    double kp = atof(argv[1]);
    double ki = atof(argv[2]);
    double kd = atof(argv[3]);
    double desired_heading = atof(argv[4]);
    //set pid config and desired heading
    PID pid(kp, ki, kd, 100000, 0);
    pid.setHeading(desired_heading);
    

    //control until error < 10^-1
    double error;
    double now_heading = 0;
    double output;
    struct report{
    vector<double> error_log;
    vector<double> output_log;
    }PID_report;
    PID_report.error_log.clear();
    PID_report.output_log.clear();
    
    bool stop = false;
    thread t(loop, ref(stop));
    t.detach();
    do{
        error = pid.getError(now_heading);
        output = pid.controller(error);
        PID_report.error_log.push_back(error);
        PID_report.output_log.push_back(output);
        cout<<"-------------------------\n";
        cout<<"error: "<<error<<'\n';
        cout<<"output: "<<output<<'\n';
        cout<<"-------------------------\n";
        sleepInSecond(0.01);
    }
    while(abs(error) > 10^-1 && !stop);
    cout<<"Making LOG file ...\n";
    writeLog(PID_report.error_log, PID_report.output_log);
    return 0;
}

void writeLog(vector<double> error, vector<double> output)
{
    string s = "LOG_"+getCurrentDateTime("now");
    string m = "mkdir " + s;
    system(m.c_str());
    chdir(s.c_str());
    s = s + "_report.txt";
    freopen(s.c_str(),"w",stdout);
    for(int i=0;i<error.size();i++)
        cout << error.at(i) << "    " << output.at(i) << '\n';
}

string getCurrentDateTime(string s)
{
    time_t now = time(0);
    struct tm tstruct;
    char buf[80];
    tstruct = *localtime(&now);
    if(s=="now")
        strftime(buf, sizeof(buf), "%Y%m%d_%X", &tstruct);
    else if (s=="date")
        strftime(buf, sizeof(buf), "%Y%m%d", &tstruct);
    return string(buf);
}

void sleepInSecond(double s)
{
    std::clock_t start = std::clock();
    while(1)
        if((std::clock()-start)/(double)CLOCKS_PER_SEC > s)
            break;
}

void loop(bool& stop)
{
    cin.get();
    stop = true;
}

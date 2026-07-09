#include<bits/stdc++.h>
using namespace std;
class Student
{
    string name;
    string rollno;
    string department;
    float cgpa;

    void store(){
        cout<<"Enter Name: ";
        cin>>this->name;
        cout<<endl<<"Enter Roll Number: ";
        cin>>this->rollno;
        cout<<endl<<"Enter Department: ";
        cin>>this->department;
        cout<<endl<<"Enter CGPA: ";
        cin>>this->cgpa;
    }
    void display(){
        cout<<"Name: "<<this->name;
        cout<<"Roll No: "<<this->rollno;
        cout<<"Department: "<<this->department;
        cout<<"CGPA: "<<this->cgpa<<endl;
    }
};

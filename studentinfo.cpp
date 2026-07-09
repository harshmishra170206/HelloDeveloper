#include<bits/stdc++.h>
using namespace std;
class Student
{
    public:
        string name;
        string rollno;
        string department;
        float cgpa;

        void store(){
            cout<<"Enter Name: ";
            getline(cin,name);
            cout<<endl<<"Enter Roll Number: ";
            cin>>rollno;
            cout<<endl<<"Enter Department: ";
            cin>>department;
            cout<<endl<<"Enter CGPA: ";
            cin>>cgpa;
            cin.ignore();
        }
        void display() const{
            cout<<"Name: "<<name;
            cout<<endl<<"Roll No: "<<rollno;
            cout<<endl<<"Department: "<<department;
            cout<<endl<<"CGPA: "<<cgpa<<endl;
        }
};

vector<Student> vec;
int main()
{
    
    while(true)
    {
        char op;
        cout<<"Store Details(s)/ View List(v)/ Exit(any key): ";
        cin>>op;
        cin.ignore();
        if(op=='s')
        {
            Student s;
            s.store();
            vec.push_back(s);
        }
        else if(op=='v')
        {
            for (const Student &v:vec){
                v.display();
            }
        }
        else{
            cout<<"Exit Successful!!!";
            break;
        }
    }
    return 0;
}

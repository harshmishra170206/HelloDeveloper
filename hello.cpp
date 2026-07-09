#include<iostream>
#include<chrono>
#include<format>
using namespace std;
void display(){
    cout<<"Name: Harsh Mishra\nRegister Number: 24MIS0206\nDepartment: Software Engineering(SCORE)"<<endl;
    auto now= chrono::current_zone()->to_local(chrono::system_clock::now());
    cout<<format("Current Date and Time : {:%Y-%m-%d %X}\n",now);
}
int main(){
    display();
    return 0;
}
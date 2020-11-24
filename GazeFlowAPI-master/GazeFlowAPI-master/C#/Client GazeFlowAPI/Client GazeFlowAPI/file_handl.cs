string line="";
int counter=0;;
System.IO.StreamReader file =   
    new System.IO.StreamReader(@"k.txt");  
System.IO.StreamWriter file1 =   
    new System.IO.StreamWriter(@"k1.txt"); 
while((line = file.ReadLine()) != null)  
{  
    System.Console.WriteLine(line);
    int i=0;
    for( i=0;i<line.Length;i++)
    {
        if(line[i]==' ')
        break;
    }  
    // line[i]=',';
    string new_lin=line.Replace(' ',',');
    
    System.Console.WriteLine(new_lin+'#');
    file1.WriteLine(new_lin);
    counter++;  
}  
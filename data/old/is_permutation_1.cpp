// Source - https://codereview.stackexchange.com/q
// Posted by Steephen, modified by community. See post 'Timeline' for change history
// Retrieved 2025-11-29, License - CC BY-SA 3.0

#include<iostream>
#include<algorithm>
#include<unordered_map>
#include<array>
template <typename T1, std::size_t N>
std::unordered_map<int,int> make_unordered_map(std::array<T1,N> & array)
{
    std::unordered_map<int,int> temp_unordered_map;
    auto temp_unordered_map_end = temp_unordered_map.end();
    for( auto &x: array)
    {
        auto it_temp_unordered_map = temp_unordered_map.find(x);
        if( it_temp_unordered_map == temp_unordered_map_end)
        {
            temp_unordered_map.insert(std::pair<T1,int>(x,1));                       
        }
        else
        {
            ++(it_temp_unordered_map->second);
        }
    }
    return temp_unordered_map;
}

template <typename T1, std::size_t N1, std::size_t N2>
bool is_permutation(std::array<T1,N1> & array1, std::array<T1,N2>&  array2)
{       
    if( N1  != N2)
       return false;
    else
    {
        std::unordered_map<int,int> first_map = make_unordered_map(array1);        
        std::unordered_map<int,int> second_map = make_unordered_map(array2);

        std::pair<std::unordered_map<int,int>::iterator,std::unordered_map<int,int>::iterator> myPair=
                std::mismatch(first_map.begin(),first_map.end(),second_map.begin(), 
                [](std::pair<const int,int>& seed1, std::pair<const int,int> & seed2) 
                  { return seed1.second == seed2.second;}
            );

        if(( myPair.first == first_map.end()) && (myPair.second == second_map.end()))
            return true;
        else      
            return false;    
    }
}


int main()
{     
    std::array<int,5> array1 {{1,3,1,4,5}};
    std::array<int,4> array2 {{1,1,4,3}};

    if(::is_permutation<int,array1.size(), array2.size()>(array1, array2))
        std::cout<< " Arrays are permutation of each other\n"; 
    else
        std::cout<< " Arrays are not permutation of each other\n";

    return 0;
}
